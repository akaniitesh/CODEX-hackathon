from __future__ import annotations

import asyncio
from pathlib import Path


class StaticAnalysisService:
    """Run deterministic static analysis tools with bounded execution."""

    async def run_all(self, repo_path: Path) -> dict[str, dict[str, object]]:
        """Run configured static analyzers and return compact results."""
        tools = {
            "ruff": ["ruff", "check", "--output-format=json", "."],
            "pyright": ["pyright", "--outputjson"],
            "bandit": ["bandit", "-r", ".", "-f", "json"],
            "semgrep": ["semgrep", "--json", "."],
            "radon": ["radon", "cc", ".", "--json"],
        }
        results = await asyncio.gather(
            *(
                self._run_tool(name, command, repo_path)
                for name, command in tools.items()
            )
        )
        return dict(results)

    async def _run_tool(
        self,
        name: str,
        command: list[str],
        repo_path: Path,
    ) -> tuple[str, dict[str, object]]:
        """Run one static analyzer without shell access."""
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=60)
        except (FileNotFoundError, TimeoutError) as exc:
            return name, {"available": False, "error": type(exc).__name__}
        return (
            name,
            {
                "available": True,
                "exit_code": process.returncode,
                "stdout": stdout.decode("utf-8", errors="ignore")[:50_000],
                "stderr": stderr.decode("utf-8", errors="ignore")[:10_000],
            },
        )

