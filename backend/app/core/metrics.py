from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram

# HTTP Request Metrics
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests processed",
    ["method", "endpoint", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)

# Agent & LLM Observability Metrics
AGENT_TOKEN_USAGE_TOTAL = Counter(
    "agent_token_usage_total",
    "Total LLM tokens consumed by agents",
    ["provider", "model", "user_id"],
)

AGENT_COST_USD_TOTAL = Counter(
    "agent_cost_usd_total",
    "Total LLM cost accrued in USD",
    ["provider", "model", "user_id"],
)

CIRCUIT_BREAKER_STATE = Gauge(
    "circuit_breaker_state",
    "Circuit breaker status (0=CLOSED, 1=OPEN, 2=HALF_OPEN)",
    ["provider"],
)

CIRCUIT_BREAKER_FAILURES_TOTAL = Counter(
    "circuit_breaker_failures_total",
    "Total circuit breaker failure trips",
    ["provider"],
)

GUARDRAIL_VIOLATIONS_TOTAL = Counter(
    "guardrail_violations_total",
    "Total guardrail rule violations detected",
    ["violation_type"],
)

HALLUCINATION_VERIFICATIONS_TOTAL = Counter(
    "hallucination_verifications_total",
    "Diff verification results for agent claimed file edits",
    ["status"],  # verified / hallucinated
)

PROVIDER_FALLBACK_EVENTS_TOTAL = Counter(
    "provider_fallback_events_total",
    "Total provider fallback switch events",
    ["from_provider", "to_provider"],
)

AGENT_EXECUTION_DURATION_SECONDS = Histogram(
    "agent_execution_duration_seconds",
    "Agent execution time per node step",
    ["agent_name"],
)
