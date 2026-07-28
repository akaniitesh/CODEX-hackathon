from __future__ import annotations

import ast
from pathlib import Path

from app.analysis.safety import is_sensitive_path, safe_relative_path


class ImportGraphService:
    """Extract deterministic Python import and symbol summaries."""

    def build_python_graph(self, repo_path: Path) -> dict[str, list[str]]:
        """Return Python module imports by file."""
        root = repo_path.resolve()
        graph: dict[str, list[str]] = {}
        for path in root.rglob("*.py"):
            if is_sensitive_path(path):
                continue
            tree = self._parse_python(path)
            if tree is None:
                graph[safe_relative_path(root, path)] = []
                continue
            imports = sorted(self._imports_from_tree(tree))
            graph[safe_relative_path(root, path)] = imports
        return graph

    def collect_python_symbols(self, repo_path: Path) -> dict[str, list[str]]:
        """Return function signatures, class names, and docstring presence."""
        root = repo_path.resolve()
        symbols: dict[str, list[str]] = {}
        for path in root.rglob("*.py"):
            if is_sensitive_path(path):
                continue
            tree = self._parse_python(path)
            if tree is None:
                symbols[safe_relative_path(root, path)] = ["syntax_error"]
                continue
            file_symbols: list[str] = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    doc = "docstring" if ast.get_docstring(node) else "no_docstring"
                    file_symbols.append(f"{node.name}({', '.join(args)}):{doc}")
                elif isinstance(node, ast.ClassDef):
                    doc = "docstring" if ast.get_docstring(node) else "no_docstring"
                    file_symbols.append(f"class {node.name}:{doc}")
            symbols[safe_relative_path(root, path)] = sorted(file_symbols)
        return symbols

    def _parse_python(self, path: Path) -> ast.AST | None:
        """Parse Python source and tolerate malformed repository files."""
        try:
            return ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            return None

    def _imports_from_tree(self, tree: ast.AST) -> set[str]:
        """Extract imported top-level module names from a Python AST."""
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".", maxsplit=1)[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".", maxsplit=1)[0])
        return imports
