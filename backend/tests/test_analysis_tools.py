from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from app.analysis.import_graph import ImportGraphService
from app.analysis.safety import is_sensitive_path, safe_relative_path
from app.analysis.static_tools import StaticAnalysisService
from app.analysis.summarizer import RepositorySummarizer
from app.analysis.tree_service import DirectoryTreeService, TreeSitterAstService
from app.core.config import Settings


def test_is_sensitive_path() -> None:
    """Detect sensitive secret files and extensions."""
    assert is_sensitive_path(Path(".env")) is True
    assert is_sensitive_path(Path(".env.local")) is True
    assert is_sensitive_path(Path("id_rsa")) is True
    assert is_sensitive_path(Path("private.pem")) is True
    assert is_sensitive_path(Path("server.key")) is True
    assert is_sensitive_path(Path("main.py")) is False
    assert is_sensitive_path(Path("README.md")) is False


def test_safe_relative_path(tmp_path: Path) -> None:
    """Relative paths stay contained within repository root."""
    file_path = tmp_path / "src" / "app.py"
    file_path.parent.mkdir(parents=True)
    file_path.write_text("print('hello')", encoding="utf-8")

    rel = safe_relative_path(tmp_path, file_path)
    assert rel == "src/app.py"

    outside = tmp_path.parent / "outside.py"
    with pytest.raises(ValueError, match="escapes repository root"):
        safe_relative_path(tmp_path, outside)


def test_directory_tree_service_excludes_sensitive(tmp_path: Path) -> None:
    """Directory tree index ignores secret files."""
    (tmp_path / "main.py").write_text("import sys", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=123", encoding="utf-8")
    (tmp_path / "key.pem").write_text("PEM_DATA", encoding="utf-8")

    service = DirectoryTreeService()
    tree = service.build_tree(tmp_path)

    assert tree == ["main.py"]


def test_tree_sitter_ast_service_targets(tmp_path: Path) -> None:
    """Identify parse-eligible source code files."""
    (tmp_path / "app.py").write_text("def run(): pass", encoding="utf-8")
    (tmp_path / "script.ts").write_text("console.log('hi');", encoding="utf-8")
    (tmp_path / "data.csv").write_text("a,b,c", encoding="utf-8")

    service = TreeSitterAstService()
    targets = service.summarize_parse_targets(tmp_path)

    assert "app.py" in targets
    assert "script.ts" in targets
    assert "data.csv" not in targets


def test_import_graph_service(tmp_path: Path) -> None:
    """Extract Python imports and function/class symbols."""
    code = '''"""Module docstring."""
import os
from math import sqrt

def calculate(x: int) -> float:
    """Calculate sqrt."""
    return sqrt(x)

class Service:
    pass
'''
    (tmp_path / "calc.py").write_text(code, encoding="utf-8")

    service = ImportGraphService()
    graph = service.build_python_graph(tmp_path)
    symbols = service.collect_python_symbols(tmp_path)

    assert graph["calc.py"] == ["math", "os"]
    assert any("calculate(x):docstring" in item for item in symbols["calc.py"])
    assert any("class Service:no_docstring" in item for item in symbols["calc.py"])


@pytest.mark.asyncio
async def test_static_analysis_service_handles_missing_tools(tmp_path: Path) -> None:
    """Static analysis service returns graceful error payloads for missing CLI tools."""
    service = StaticAnalysisService()
    results = await service.run_all(tmp_path)

    assert "ruff" in results
    assert "pyright" in results
    assert "bandit" in results
    assert "semgrep" in results
    assert "radon" in results


@pytest.mark.asyncio
async def test_repository_summarizer_cache_hit_and_miss(tmp_path: Path) -> None:
    """Summarizer uses Redis cache keyed by commit SHA."""
    (tmp_path / "main.py").write_text("print('hello')", encoding="utf-8")

    redis_mock = AsyncMock()
    redis_mock.get.return_value = None  # Cache miss first

    settings = Settings()
    summarizer = RepositorySummarizer(redis_mock, settings)

    summary1 = await summarizer.summarize(tmp_path, commit_sha="commit-sha-1")
    assert summary1["commit_sha"] == "commit-sha-1"
    tree = summary1["directory_tree"]
    assert isinstance(tree, list)
    assert "main.py" in tree
    redis_mock.setex.assert_called_once()
