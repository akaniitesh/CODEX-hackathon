from __future__ import annotations

from app.core.errors import ApiError


class ToolPermissionDeniedError(ApiError):
    """Exception raised when an agent attempts to call an unauthorized tool."""

    def __init__(self, agent_name: str, tool_name: str) -> None:
        message = (
            f"Agent '{agent_name}' is not authorized to execute tool '{tool_name}'."
        )
        super().__init__(message, status_code=403)


AGENT_TOOL_ALLOWLIST: dict[str, set[str]] = {
    "planner": {"summarize_repo", "read_readme"},
    "repo_analyzer": {"tree_inventory", "python_imports", "python_symbols"},
    "architecture_agent": {"python_imports", "python_symbols"},
    "code_reviewer": {"run_static_analysis"},
    "test_generator": {"run_sandbox_tests"},
    "security_auditor": {"run_sandbox_security"},
    "documentation_agent": {"read_readme", "python_symbols"},
    "pr_generator": {"verify_diff_against_edits"},
    "deployment_validator": {"check_deployment_readiness"},
    "memory_manager": {"read_run_memory", "write_run_memory"},
}


class ToolPermissionManager:
    """Central declarative permission enforcer for agent tool calls."""

    def __init__(self, allowlist: dict[str, set[str]] | None = None) -> None:
        self.allowlist = allowlist if allowlist is not None else AGENT_TOOL_ALLOWLIST

    def check_permission(self, agent_name: str, tool_name: str) -> bool:
        """Return True if agent is allowed to invoke tool_name."""
        allowed = self.allowlist.get(agent_name, set())
        return tool_name in allowed

    def enforce(self, agent_name: str, tool_name: str) -> None:
        """Raise ToolPermissionDeniedError if agent is unauthorized."""
        if not self.check_permission(agent_name, tool_name):
            raise ToolPermissionDeniedError(agent_name, tool_name)


permission_manager = ToolPermissionManager()
