from __future__ import annotations

from datetime import datetime
from pathlib import Path

from reverse.models import PreviewEntry, PreviewResponse
from reverse.storage import api_root, list_generated_files


def preview(api_slug: str) -> PreviewResponse:
    files = []
    root = api_root(api_slug)
    for file_path in list_generated_files(api_slug):
        stats = file_path.stat()
        files.append(
            PreviewEntry(
                path=str(file_path.relative_to(root)),
                size_bytes=stats.st_size,
                updated_at=datetime.fromtimestamp(stats.st_mtime),
            )
        )
    return PreviewResponse(api_slug=api_slug, files=sorted(files, key=lambda entry: entry.path))
