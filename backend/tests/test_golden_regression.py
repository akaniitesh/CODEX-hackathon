from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.ai.benchmarking import ProviderBenchmarkEngine
from app.ai.schemas import AIResponse, ProviderName, TokenUsage
from tests.test_ai_provider_abstraction import MockProvider


@pytest.mark.asyncio
async def test_golden_set_regression_verification() -> None:
    """Golden regression test catches prompt/output quality regressions."""
    golden_path = Path(__file__).parent / "golden" / "golden_repo_v1.json"
    assert golden_path.exists()

    golden_data = json.loads(golden_path.read_text(encoding="utf-8"))
    assert golden_data["repo_name"] == "sample-python-app"

    mock_response = AIResponse(
        provider=ProviderName.GROQ,
        model="mock",
        content=(
            "Execution plan includes architectural analysis, analyzer tools, "
            "and security scans."
        ),
        usage=TokenUsage(total_tokens=100),
    )

    provider = MockProvider(ProviderName.GROQ, [mock_response])
    engine = ProviderBenchmarkEngine([provider])

    result = await engine.benchmark_provider(provider, golden_data)
    assert result.provider == ProviderName.GROQ
    assert result.quality_score == 1.0
    assert result.composite_rank_score > 0.5
