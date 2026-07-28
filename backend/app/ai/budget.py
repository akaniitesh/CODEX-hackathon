from __future__ import annotations

from dataclasses import dataclass

from app.ai.errors import TokenBudgetExceededError
from app.ai.schemas import TokenUsage


@dataclass
class BudgetState:
    """Token and cost state for a run or user."""

    token_limit: int
    cost_limit_usd: float
    tokens_used: int = 0
    cost_used_usd: float = 0.0
    tripped: bool = False


class TokenBudgetManager:
    """Per-run and per-user token/cost circuit breaker."""

    def __init__(
        self,
        default_run_token_limit: int,
        default_user_token_limit: int,
        default_run_cost_limit_usd: float,
        default_user_cost_limit_usd: float,
    ) -> None:
        self.default_run_token_limit = default_run_token_limit
        self.default_user_token_limit = default_user_token_limit
        self.default_run_cost_limit_usd = default_run_cost_limit_usd
        self.default_user_cost_limit_usd = default_user_cost_limit_usd
        self._runs: dict[str, BudgetState] = {}
        self._users: dict[str, BudgetState] = {}

    def ensure_allowed(self, run_id: str | None, user_id: str | None) -> None:
        """Refuse calls once a run or user budget is tripped."""
        for label, state in self._states(run_id, user_id):
            if state.tripped:
                raise TokenBudgetExceededError(f"{label} token budget is exceeded.")

    def reserve(self, run_id: str | None, user_id: str | None, tokens: int) -> None:
        """Reserve requested max tokens before making a provider call."""
        for label, state in self._states(run_id, user_id):
            if state.tokens_used + tokens > state.token_limit:
                state.tripped = True
                raise TokenBudgetExceededError(f"{label} token budget is exceeded.")

    def record_usage(
        self,
        run_id: str | None,
        user_id: str | None,
        usage: TokenUsage,
    ) -> None:
        """Record actual provider usage and trip budgets when exceeded."""
        for label, state in self._states(run_id, user_id):
            state.tokens_used += usage.total_tokens
            state.cost_used_usd += usage.estimated_cost_usd
            if (
                state.tokens_used > state.token_limit
                or state.cost_used_usd > state.cost_limit_usd
            ):
                state.tripped = True
                raise TokenBudgetExceededError(f"{label} token budget is exceeded.")

    def _states(
        self,
        run_id: str | None,
        user_id: str | None,
    ) -> list[tuple[str, BudgetState]]:
        """Return budget states that apply to a request."""
        states: list[tuple[str, BudgetState]] = []
        if run_id:
            states.append(("Run", self._run_state(run_id)))
        if user_id:
            states.append(("User", self._user_state(user_id)))
        return states

    def _run_state(self, run_id: str) -> BudgetState:
        """Return or create a run budget state."""
        return self._runs.setdefault(
            run_id,
            BudgetState(
                token_limit=self.default_run_token_limit,
                cost_limit_usd=self.default_run_cost_limit_usd,
            ),
        )

    def _user_state(self, user_id: str) -> BudgetState:
        """Return or create a user budget state."""
        return self._users.setdefault(
            user_id,
            BudgetState(
                token_limit=self.default_user_token_limit,
                cost_limit_usd=self.default_user_cost_limit_usd,
            ),
        )

