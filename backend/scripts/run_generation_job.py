from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path


def _slugify(value: str) -> str:
    sanitized = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in value.lower())
    while "--" in sanitized:
        sanitized = sanitized.replace("--", "-")
    result = sanitized.strip("-_")
    return result or "api"


def _run(cmd: list[str], *, check: bool = True, capture_output: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        check=check,
        capture_output=capture_output,
        text=True,
    )


def _ensure_network(name: str) -> bool:
    """Ensure network exists, creating it if necessary. Returns True if created, False if already existed."""
    inspect = _run(["docker", "network", "inspect", name], check=False, capture_output=True)
    if inspect.returncode == 0:
        return False
    # Network doesn't exist, create it
    create_result = _run(["docker", "network", "create", name], check=False, capture_output=True)
    if create_result.returncode != 0:
        raise RuntimeError(
            f"Failed to create Docker network '{name}': {create_result.stderr}"
        )
    # Verify it was created
    verify = _run(["docker", "network", "inspect", name], check=False, capture_output=True)
    if verify.returncode != 0:
        raise RuntimeError(
            f"Network '{name}' was created but cannot be inspected. Docker daemon may be having issues."
        )
    return True


def _start_postgres(
    *,
    container_name: str,
    network: str,
    image: str,
    user: str,
    password: str,
    database: str,
) -> None:
    env_flags = [
        "-e",
        f"POSTGRES_USER={user}",
        "-e",
        f"POSTGRES_PASSWORD={password}",
        "-e",
        f"POSTGRES_DB={database}",
        "-e",
        "PGDATA=/var/lib/postgresql/data/pgdata",
    ]
    run_cmd = [
        "docker",
        "run",
        "--rm",
        "-d",
        "--name",
        container_name,
        "--network",
        network,
    ]
    run_cmd.extend(env_flags)
    run_cmd.append(image)
    _run(run_cmd)


def _wait_for_postgres(
    *,
    network: str,
    host: str,
    port: int,
    user: str,
    password: str,
    timeout: int,
    image: str,
) -> None:
    check_cmd = [
        "docker",
        "run",
        "--rm",
        "--network",
        network,
        "-e",
        f"PGPASSWORD={password}",
        image,
        "pg_isready",
        "-h",
        host,
        "-p",
        str(port),
        "-U",
        user,
    ]
    deadline = time.time() + timeout
    while time.time() < deadline:
        probe = _run(check_cmd, check=False, capture_output=True)
        if probe.returncode == 0:
            return
        time.sleep(1)
    raise RuntimeError(f"Postgres container '{host}' did not become ready within {timeout} seconds.")


def _build_docker_run_command(
    *,
    image: str,
    container_name: str,
    network: str,
    env: dict[str, str],
    mounts: list[tuple[Path, str]],
    command: list[str],
) -> list[str]:
    cmd = [
        "docker",
        "run",
        "--rm",
        "--name",
        container_name,
        "--network",
        network,
    ]
    for key, value in env.items():
        cmd.extend(["-e", f"{key}={value}"])
    for host_path, container_path in mounts:
        cmd.extend(["-v", f"{host_path}:{container_path}"])
    cmd.append(image)
    cmd.extend(command)
    return cmd


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Launch a per-API generation container wired up to a PostgreSQL instance."
    )
    parser.add_argument("--api-slug", required=True, help="Slug for the generated API job.")
    parser.add_argument(
        "--manifest",
        type=Path,
        required=False,
        help="Optional path to the job manifest or plan assets mounted into the container. If not provided, the plan will be regenerated.",
    )
    parser.add_argument(
        "--image",
        default="deepmock-backend:latest",
        help="Container image that hosts the generator runtime.",
    )
    parser.add_argument(
        "--postgres-image",
        default="postgres:16-alpine",
        help="Container image to use for the transient PostgreSQL instance.",
    )
    parser.add_argument(
        "--postgres-user",
        default="deepmock",
        help="PostgreSQL user for transient databases.",
    )
    parser.add_argument(
        "--postgres-password",
        default="deepmock",
        help="PostgreSQL password for transient databases.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=45,
        help="Seconds to wait for PostgreSQL readiness before failing.",
    )
    parser.add_argument(
        "--shared-database-url",
        help="If provided, skip launching PostgreSQL and use this DSN inside the container.",
    )
    parser.add_argument(
        "--keep-resources",
        action="store_true",
        help="Skip cleanup to allow manual inspection (PostgreSQL container and network stay alive).",
    )
    parser.add_argument(
        "--network-name",
        help="Optional explicit Docker network name. Defaults to deepmock-gen-<slug>.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Host directory to mount for generated files. If not provided, generated files will only exist in the container.",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Optional command to execute inside the generator container. Defaults to reverse-generate.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    manifest = args.manifest.resolve() if args.manifest else None
    if manifest and not manifest.exists():
        raise FileNotFoundError(f"Manifest path '{manifest}' does not exist.")

    slug_fragment = _slugify(args.api_slug)
    network_name = args.network_name or f"deepmock-gen-{slug_fragment}"
    job_container = f"deepmock-job-{slug_fragment}"
    pg_container = f"deepmock-pg-{slug_fragment}"
    pg_db_name = f"deepmock_{slug_fragment}"
    pg_port = 5432

    created_network = False
    created_postgres = False

    try:
        created_network = _ensure_network(network_name)
        
        # Verify network exists before proceeding
        verify_network = _run(["docker", "network", "inspect", network_name], check=False, capture_output=True)
        if verify_network.returncode != 0:
            raise RuntimeError(
                f"Network '{network_name}' does not exist and could not be created. "
                f"Docker daemon may be unavailable or there may be permission issues."
            )

        # Check for _DATABASE_URL or DATABASE_URL environment variable first
        # Prioritize: --shared-database-url > _DATABASE_URL > DATABASE_URL
        env_db_url = os.getenv("_DATABASE_URL") or os.getenv("DATABASE_URL")
        database_url = args.shared_database_url or env_db_url
        
        if env_db_url:
            print(f"[run_generation_job] Found database URL in environment: {'_DATABASE_URL' if os.getenv('_DATABASE_URL') else 'DATABASE_URL'}")
        
        if not database_url:
            print(f"[run_generation_job] No database URL provided. Creating transient PostgreSQL container...")
            _start_postgres(
                container_name=pg_container,
                network=network_name,
                image=args.postgres_image,
                user=args.postgres_user,
                password=args.postgres_password,
                database=pg_db_name,
            )
            created_postgres = True
            _wait_for_postgres(
                network=network_name,
                host=pg_container,
                port=pg_port,
                user=args.postgres_user,
                password=args.postgres_password,
                timeout=args.timeout,
                image=args.postgres_image,
            )
            database_url = (
                f"postgresql+psycopg://{args.postgres_user}:{args.postgres_password}"
                f"@{pg_container}:{pg_port}/{pg_db_name}"
            )
        else:
            # For Docker containers, localhost needs to be replaced with host.docker.internal (Mac/Windows)
            # or the actual host IP
            if database_url and ("localhost" in database_url or "127.0.0.1" in database_url):
                # Replace localhost with host.docker.internal for Mac/Windows
                # For Linux, might need to use host gateway IP or host network mode
                import platform
                if platform.system() in ("Darwin", "Windows"):
                    database_url = database_url.replace("localhost", "host.docker.internal").replace("127.0.0.1", "host.docker.internal")
                    print(f"[run_generation_job] Updated database URL to use host.docker.internal for Docker networking")
            
            db_info = database_url.split('@')[-1] if '@' in database_url else database_url
            print(f"[run_generation_job] Using existing database: {db_info}")
            env_db_url = os.getenv("_DATABASE_URL") or os.getenv("DATABASE_URL")
            if env_db_url:
                print(f"[run_generation_job] Source: Environment variable ({'DATABASE_URL' if os.getenv('DATABASE_URL') else '_DATABASE_URL'})")
            elif args.shared_database_url:
                print(f"[run_generation_job] Source: --shared-database-url argument")

        command = args.command or []
        if command[:1] == ["--"]:
            command = command[1:]
        if not command:
            if manifest:
                command = ["reverse-generate", "--api-slug", args.api_slug, "--plan-json", "/workspace/manifest.yaml"]
            else:
                command = ["reverse-generate", "--api-slug", args.api_slug]

        # Prepare volume mounts
        mounts = []
        if manifest:
            mounts.append((manifest, "/workspace/manifest.yaml"))
        
        # Mount output directory if provided
        if args.output_dir:
            output_dir = args.output_dir.resolve()
            output_dir.mkdir(parents=True, exist_ok=True)
            # Mount to the generated directory inside container
            mounts.append((output_dir, "/app/reverse/generated"))
            print(f"[run_generation_job] Mounting output directory: {output_dir} -> /app/reverse/generated")

        run_cmd = _build_docker_run_command(
            image=args.image,
            container_name=job_container,
            network=network_name,
            env={
                "_DATABASE_URL": database_url,
                "API_SLUG": args.api_slug,
                "API_MANIFEST": "/workspace/manifest.yaml",
            },
            mounts=mounts,
            command=command,
        )
        print(f"[run_generation_job] Executing: {' '.join(shlex.quote(part) for part in run_cmd)}")
        _run(run_cmd)
    except Exception as exc:
        print(f"[run_generation_job] Error: {exc}", file=sys.stderr)
        return 1
    finally:
        if not args.keep_resources:
            if created_postgres:
                _run(["docker", "stop", pg_container], check=False)
            if created_network:
                _run(["docker", "network", "rm", network_name], check=False)
        else:
            print(
                f"[run_generation_job] Resources kept alive. Network={network_name} "
                f"Postgres={'running' if created_postgres else 'not created'}."
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
