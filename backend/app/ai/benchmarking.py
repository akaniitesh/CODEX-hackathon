from __future__ import annotations

import time
from typing import Any

from pydantic import BaseModel

from app.ai.base import BaseAIProvider
from app.ai.schemas import AIMessage, AIRequest, ProviderName


class BenchmarkResult(BaseModel):
    """Result metrics from benchmarking a provider against golden test cases."""

    provider: ProviderName
    latency_ms: float
    tokens_consumed: int
    cost_usd: float
    quality_score: float  # 0.0 to 1.0 based on keyword & structural coverage
    composite_rank_score: float


class ProviderBenchmarkEngine:
    """Benchmark engine comparing AI providers for quality, cost, and latency."""

    def __init__(self, providers: list[BaseAIProvider]) -> None:
        self.providers = providers

    async def benchmark_provider(
        self,
        provider: BaseAIProvider,
        golden_case: dict[str, Any],
    ) -> BenchmarkResult:
        """Run golden test evaluation against a specific AI provider."""
        start_time = time.perf_counter()
        repo_name = golden_case["repo_name"]
        request = AIRequest(
            messages=[
                AIMessage(
                    role="user",
                    content=f"Analyze repo {repo_name} and generate plan.",
                )
            ],
            run_id="benchmark-run",
            user_id="benchmark-user",
        )

        response = await provider.generate(request)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        keywords: list[str] = golden_case.get("expected_plan_keywords", [])
        matched = sum(1 for kw in keywords if kw.lower() in response.content.lower())
        quality_score = matched / len(keywords) if keywords else 1.0

        tokens = response.usage.total_tokens if response.usage else 50
        cost = tokens * 0.000002  # Approximate cost per token USD

        # Composite score weighting: 50% Quality, 30% Latency, 20% Cost
        latency_penalty = min(elapsed_ms / 2000.0, 1.0)
        cost_penalty = min(cost / 0.01, 1.0)
        composite_score = (
            (quality_score * 0.5)
            + ((1.0 - latency_penalty) * 0.3)
            + ((1.0 - cost_penalty) * 0.2)
        )

        return BenchmarkResult(
            provider=provider.name,
            latency_ms=elapsed_ms,
            tokens_consumed=tokens,
            cost_usd=cost,
            quality_score=quality_score,
            composite_rank_score=composite_score,
        )
