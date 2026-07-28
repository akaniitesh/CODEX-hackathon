from __future__ import annotations

import pytest

from app.agents.graph import build_graph_skeleton
from app.agents.permissions import ToolPermissionDeniedError, ToolPermissionManager
from app.agents.prompts.registry import PromptRegistry
from app.agents.schemas import AutonomousAgentState, add_errors, add_messages
from app.core.errors import ApiError


def test_agent_state_reducers() -> None:
    """Test state reducer functions for messages and errors."""
    msgs1 = [{"role": "user", "content": "hello"}]
    msgs2 = [{"role": "assistant", "content": "hi"}]
    assert add_messages(msgs1, msgs2) == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi"},
    ]

    errs1 = ["err1"]
    errs2 = ["err2"]
    assert add_errors(errs1, errs2) == ["err1", "err2"]


def test_prompt_registry_formatting() -> None:
    """Prompt registry loads templates and injects variables."""
    registry = PromptRegistry()

    prompt = registry.get_prompt(
        "planner",
        "v1",
        repo_path="/path/to/repo",
        commit_sha="commit123",
        repo_summary="Test Summary",
    )
    assert "/path/to/repo" in prompt
    assert "commit123" in prompt
    assert "Test Summary" in prompt


def test_prompt_registry_missing_variable() -> None:
    """Prompt registry raises ValueError when required variables are missing."""
    registry = PromptRegistry()
    with pytest.raises(ValueError, match="missing required variables"):
        registry.get_prompt("planner", "v1", repo_path="/path/to/repo")


def test_prompt_registry_nonexistent_template() -> None:
    """Prompt registry raises 404 ApiError for missing template files."""
    registry = PromptRegistry()
    with pytest.raises(ApiError) as exc_info:
        registry.get_prompt("nonexistent_agent", "v99")
    assert exc_info.value.status_code == 404


def test_tool_permission_manager() -> None:
    """Tool permission manager permits authorized calls and rejects disallowed calls."""
    manager = ToolPermissionManager()

    assert manager.check_permission("planner", "summarize_repo") is True
    assert manager.check_permission("planner", "run_sandbox_tests") is False

    manager.enforce("planner", "summarize_repo")  # Should not raise

    with pytest.raises(ToolPermissionDeniedError) as exc_info:
        manager.enforce("planner", "run_sandbox_tests")
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_graph_skeleton_execution() -> None:
    """Graph skeleton executes through all state graph nodes from START to END."""
    graph = build_graph_skeleton()
    initial_state: AutonomousAgentState = {
        "run_id": "run-001",
        "repository_id": "repo-001",
        "repo_path": "/test/repo",
        "commit_sha": "abc1234",
        "step_count": 0,
    }

    final_state = await graph.ainvoke(initial_state)

    assert final_state["current_step"] == "human_approval"
    assert final_state["step_count"] == 9
