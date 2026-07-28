from __future__ import annotations

from pathlib import Path

from app.analysis.safety import is_sensitive_path, safe_relative_path


class DirectoryTreeService:
    """Build safe directory inventories for connected repositories."""

    def build_tree(self, repo_path: Path, max_files: int = 5_000) -> list[str]:
        """Return non-sensitive file paths below a repository root."""
        root = repo_path.resolve()
        paths: list[str] = []
        for path in root.rglob("*"):
            if len(paths) >= max_files:
                break
            if path.is_file() and not is_sensitive_path(path):
                paths.append(safe_relative_path(root, path))
        return sorted(paths)


class TreeSitterAstService:
    """Parse source files into lightweight AST availability summaries."""

    SUPPORTED_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java"}

    def summarize_parse_targets(self, repo_path: Path) -> dict[str, str]:
        """Return source files eligible for Tree-sitter parsing.

        Grammar packages are language-specific, so Phase 2 records deterministic
        parse targets. Phase 4 agent tools can add installed grammars without
        changing the service contract.
        """
        root = repo_path.resolve()
        summary: dict[str, str] = {}
        for path in root.rglob("*"):
            if (
                path.is_file()
                and path.suffix in self.SUPPORTED_SUFFIXES
                and not is_sensitive_path(path)
            ):
                summary[safe_relative_path(root, path)] = "parse_target"
        return summary

