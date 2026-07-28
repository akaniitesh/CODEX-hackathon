from __future__ import annotations

import hashlib
import json
from pathlib import Path

from redis.asyncio import Redis

from app.analysis.git_history import GitHistoryService
from app.analysis.import_graph import ImportGraphService
from app.analysis.readme_service import ReadmeService
from app.analysis.tree_service import DirectoryTreeService, TreeSitterAstService
from app.core.config import Settings


class RepositorySummarizer:
    """Compress deterministic repository analysis into bounded context."""

    def __init__(self, redis: Redis, settings: Settings) -> None:
        self.redis = redis
        self.settings = settings
        self.tree = DirectoryTreeService()
        self.ast = TreeSitterAstService()
        self.imports = ImportGraphService()
        self.readmes = ReadmeService()
        self.history = GitHistoryService()

    async def summarize(self, repo_path: Path, commit_sha: str) -> dict[str, object]:
        """Return cached summary, invalidated by commit SHA."""
        cache_key = f"repo-summary:{commit_sha}:{self._root_hash(repo_path)}"
        cached = await self.redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            if isinstance(data, dict):
                return data

        summary: dict[str, object] = {
            "commit_sha": commit_sha,
            "directory_tree": self.tree.build_tree(repo_path),
            "parse_targets": self.ast.summarize_parse_targets(repo_path),
            "python_import_graph": self.imports.build_python_graph(repo_path),
            "python_symbols": self.imports.collect_python_symbols(repo_path),
            "readmes": self.readmes.read_readmes(repo_path),
            "recent_commits": self.history.latest_commits(repo_path),
        }
        await self.redis.setex(
            cache_key,
            self.settings.analysis_cache_ttl_seconds,
            json.dumps(summary),
        )
        return summary

    def _root_hash(self, repo_path: Path) -> str:
        """Hash the repository root path to avoid leaking local paths in Redis keys."""
        return hashlib.sha256(str(repo_path.resolve()).encode("utf-8")).hexdigest()[:16]

