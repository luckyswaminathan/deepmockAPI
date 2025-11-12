from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

from sqlalchemy.engine import make_url


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SQLITE_PATH = (BACKEND_ROOT / "deepmock.db").resolve()
SQLITE_CONTAINER_MOUNT = "/workspace/sqlite-db"


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


def _resolve_sqlite_path(url: str) -> Path:
    parsed = make_url(url)
    if not parsed.drivername.startswith("sqlite"):
        raise ValueError("Database URL is not using the SQLite driver.")
    database = parsed.database
    if not database or database == ":memory:":
        raise ValueError("SQLite database URL must reference a file on disk.")
    host_path = Path(database)
    if not host_path.is_absolute():
        host_path = (REPO_ROOT / host_path).resolve()
    return host_path


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
        description="Launch a per-API generation container wired up to a database (SQLite by default)."
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
        "--database-backend",
        choices=("sqlite", "postgres"),
        default="sqlite",
        help="Backend to use when no database URL is provided. Defaults to SQLite.",
    )
    parser.add_argument(
        "--keep-resources",
        action="store_true",
        help="Skip cleanup to allow manual inspection (transient containers/networks stay alive).",
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
    sqlite_host_path: Path | None = None

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
        
        mounts: list[tuple[Path, str]] = []

        if not database_url:
            if args.database_backend == "postgres":
                print("[run_generation_job] No database URL provided. Creating transient PostgreSQL container...")
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
                sqlite_host_path = DEFAULT_SQLITE_PATH
                sqlite_host_path.parent.mkdir(parents=True, exist_ok=True)
                sqlite_host_path.touch(exist_ok=True)
                database_url = f"sqlite:///{sqlite_host_path}"
                print(f"[run_generation_job] No database URL provided. Using SQLite at {sqlite_host_path}")

        if database_url.startswith("sqlite"):
            try:
                sqlite_host_path = _resolve_sqlite_path(database_url)
            except ValueError as exc:
                raise RuntimeError(f"Invalid SQLite database URL: {exc}") from exc
            sqlite_host_path.parent.mkdir(parents=True, exist_ok=True)
            sqlite_host_path.touch(exist_ok=True)

            sqlite_mount = (sqlite_host_path.parent, SQLITE_CONTAINER_MOUNT)
            if sqlite_mount not in mounts:
                mounts.append(sqlite_mount)
            database_url = f"sqlite:///{SQLITE_CONTAINER_MOUNT}/{sqlite_host_path.name}"
            print(
                f"[run_generation_job] Using SQLite database at {sqlite_host_path} "
                f"(mounted to {SQLITE_CONTAINER_MOUNT}/{sqlite_host_path.name})"
            )
        else:
            # For Docker containers, localhost needs to be replaced with host.docker.internal (Mac/Windows)
            # or the actual host IP
            if database_url and ("localhost" in database_url or "127.0.0.1" in database_url):
                import platform

                if platform.system() in ("Darwin", "Windows"):
                    database_url = database_url.replace("localhost", "host.docker.internal").replace(
                        "127.0.0.1", "host.docker.internal"
                    )
                    print("[run_generation_job] Updated database URL to use host.docker.internal for Docker networking")

            db_info = database_url.split("@")[-1] if "@" in database_url else database_url
            print(f"[run_generation_job] Using existing database: {db_info}")
            env_db_url = os.getenv("_DATABASE_URL") or os.getenv("DATABASE_URL")
            if env_db_url:
                source = "DATABASE_URL" if os.getenv("DATABASE_URL") else "_DATABASE_URL"
                print(f"[run_generation_job] Source: Environment variable ({source})")
            elif args.shared_database_url:
                print("[run_generation_job] Source: --shared-database-url argument")

        command = args.command or []
        if command[:1] == ["--"]:
            command = command[1:]
        if not command:
            if manifest:
                command = ["reverse-generate", "--api-slug", args.api_slug, "--plan-json", "/workspace/manifest.yaml"]
            else:
                command = ["reverse-generate", "--api-slug", args.api_slug]

        # Prepare volume mounts
        if manifest:
            mounts.append((manifest, "/workspace/manifest.yaml"))
        
        # Mount output directory if provided
        generated_output_dir_env = None
        if args.output_dir:
            output_dir = args.output_dir.resolve()
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Determine if output_dir points to generated_output root or a subdirectory
            # If output_dir ends with api_slug, it's a subdirectory, otherwise it's the root
            if output_dir.name == args.api_slug:
                # output_dir is ./generated_output/stripe - mount parent as generated_output
                generated_output_root = output_dir.parent
                # Also need to mount for code generation (reverse/generated/)
                code_gen_dir = generated_output_root.parent / "backend" / "reverse" / "generated"
                code_gen_dir.mkdir(parents=True, exist_ok=True)
                mounts.append((code_gen_dir, "/app/reverse/generated"))
                print(f"[run_generation_job] Mounting code generation directory: {code_gen_dir} -> /app/reverse/generated")
            else:
                # output_dir is ./generated_output - use it as generated_output root
                generated_output_root = output_dir
                # Also mount backend/reverse/generated for code generation
                code_gen_dir = generated_output_root.parent / "backend" / "reverse" / "generated"
                code_gen_dir.mkdir(parents=True, exist_ok=True)
                mounts.append((code_gen_dir, "/app/reverse/generated"))
                print(f"[run_generation_job] Mounting code generation directory: {code_gen_dir} -> /app/reverse/generated")
            
            # Mount generated_output for standalone API files (main.py, runtime.py, etc.)
            generated_output_root.mkdir(parents=True, exist_ok=True)
            mounts.append((generated_output_root, "/app/generated_output"))
            print(f"[run_generation_job] Mounting generated_output: {generated_output_root} -> /app/generated_output")
            # Set environment variable so sync_standalone_api knows where to write
            generated_output_dir_env = "/app/generated_output"

        docker_env = {
            "_DATABASE_URL": database_url,
            "API_SLUG": args.api_slug,
            "API_MANIFEST": "/workspace/manifest.yaml",
        }
        if generated_output_dir_env:
            docker_env["GENERATED_OUTPUT_DIR"] = generated_output_dir_env

        run_cmd = _build_docker_run_command(
            image=args.image,
            container_name=job_container,
            network=network_name,
            env=docker_env,
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
            status = "running" if created_postgres else "not created (SQLite or external DB)"
            print(f"[run_generation_job] Resources kept alive. Network={network_name} Postgres={status}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
