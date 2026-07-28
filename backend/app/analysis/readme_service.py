from __future__ import annotations

from pathlib import Path

from app.analysis.safety import is_sensitive_path


class ReadmeService:
    """Collect bounded README content for repository summaries."""

    def read_readmes(self, repo_path: Path, max_chars: int = 20_000) -> dict[str, str]:
        """Return bounded README text keyed by filename."""
        readmes: dict[str, str] = {}
        for path in repo_path.resolve().glob("README*"):
            if path.is_file() and not is_sensitive_path(path):
                readmes[path.name] = path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )[:max_chars]
        return readmes

