from __future__ import annotations

from pathlib import Path

from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError


class GitHistoryService:
    """Read compact git history metadata without exposing full commit bodies."""

    def latest_commits(self, repo_path: Path, limit: int = 25) -> list[dict[str, str]]:
        """Return a compact list of recent commits."""
        try:
            repo = Repo(repo_path)
            commits: list[dict[str, str]] = []
            for commit in repo.iter_commits(max_count=limit):
                commits.append(
                    {
                        "sha": commit.hexsha,
                        "author": str(commit.author.name or "Unknown"),
                        "summary": str(commit.summary)[:300],
                        "committed_at": commit.committed_datetime.isoformat(),
                    }
                )
            return commits
        except (InvalidGitRepositoryError, NoSuchPathError):
            return []

