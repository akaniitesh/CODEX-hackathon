from __future__ import annotations

from typing import Annotated, Any, TypedDict

from pydantic import BaseModel, Field


def add_messages(
    left: list[dict[str, Any]], right: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Reducer to append new chat messages to graph state."""
    return left + right


def add_errors(left: list[str], right: list[str]) -> list[str]:
    """Reducer to append new error strings to graph state."""
    return left + right


class AutonomousAgentState(TypedDict, total=False):
    """Shared state dictionary passed across LangGraph agent nodes."""

    run_id: str
    repository_id: str
    repo_path: str
    commit_sha: str
    current_step: str
    step_count: int
    repo_summary: dict[str, Any]
    execution_plan: dict[str, Any] | None
    architecture_analysis: dict[str, Any] | None
    code_review: dict[str, Any] | None
    generated_tests: dict[str, Any] | None
    security_findings: list[dict[str, Any]]
    documentation: dict[str, Any] | None
    pr_proposal: dict[str, Any] | None
    human_approved: bool
    human_feedback: str | None
    errors: Annotated[list[str], add_errors]
    messages: Annotated[list[dict[str, Any]], add_messages]


class PromptMetadata(BaseModel):
    """Metadata describing a prompt template in the registry."""

    prompt_id: str
    version: str
    template: str
    required_variables: list[str] = Field(default_factory=list)


class ToolPermissionRule(BaseModel):
    """Declarative permission entry mapping an agent to allowed tools."""

    agent_name: str
    allowed_tools: list[str]
