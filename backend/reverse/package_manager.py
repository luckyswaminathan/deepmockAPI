from __future__ import annotations

import shutil
from pathlib import Path
from reverse.storage import api_root, ensure_dir


def packages_root() -> Path:
    root = Path(__file__).resolve().parent.parent / "generated_apis"
    ensure_dir(root)
    init_file = root / "__init__.py"
    if not init_file.exists():
        init_file.write_text('"""Versioned packages for reverse-generated APIs."""\n\n__all__: list[str] = []\n', encoding="utf-8")
    return root


def sync_generated_package(api_slug: str) -> Path:
    source_root = api_root(api_slug)
    code_src = source_root / "code"
    tests_src = source_root / "tests"

    if not code_src.exists():
        raise FileNotFoundError(f"Generated code not found for API slug '{api_slug}'. Run /reverse/generate first.")

    root = packages_root()
    dest = root / api_slug

    if dest.exists():
        shutil.rmtree(dest)

    shutil.copytree(code_src, dest)
    _ensure_package(dest)

    if tests_src.exists():
        shutil.copytree(tests_src, dest / "tests")
        _ensure_package(dest / "tests")

    _update_package_index()
    return dest


def list_packages() -> list[str]:
    root = packages_root()
    return sorted(
        [
            entry.name
            for entry in root.iterdir()
            if entry.is_dir() and not entry.name.startswith("_")
        ]
    )


def remove_generated_package(api_slug: str) -> None:
    dest = packages_root() / api_slug
    if dest.exists():
        shutil.rmtree(dest)
        _update_package_index()


def _ensure_package(path: Path) -> None:
    ensure_dir(path)
    init_file = path / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")


def _update_package_index() -> None:
    root = packages_root()
    slugs = list_packages()
    init_file = root / "__init__.py"
    content_lines = [
        '"""Versioned packages for reverse-generated APIs."""',
        "",
        "__all__ = [",
    ]
    for slug in slugs:
        content_lines.append(f'    "{slug}",')
    content_lines.append("]")
    content_lines.append("")
    init_file.write_text("\n".join(content_lines), encoding="utf-8")
