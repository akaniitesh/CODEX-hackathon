from __future__ import annotations

import time
from collections import defaultdict
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.errors import ApiError


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware enforcing secure HTTP headers (Helmet equivalent)."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


class RateLimiter:
    """Sliding window token bucket rate limiter per client IP."""

    def __init__(self, requests_per_minute: int = 120) -> None:
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60.0
        self.clients: dict[str, list[float]] = defaultdict(list)

    def check_rate_limit(self, client_ip: str) -> None:
        """Check client request count and raise 429 if limit exceeded."""
        now = time.time()
        window_start = now - self.window_seconds
        timestamps = [t for t in self.clients[client_ip] if t > window_start]
        self.clients[client_ip] = timestamps

        if len(timestamps) >= self.requests_per_minute:
            raise ApiError(
                "Rate limit exceeded. Please wait before retrying.", status_code=429
            )

        self.clients[client_ip].append(now)


rate_limiter = RateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware applying the shared API rate limiter to inbound requests."""

    def __init__(
        self,
        app: ASGIApp,
        limiter: RateLimiter = rate_limiter,
    ) -> None:
        super().__init__(app)
        self.limiter = limiter

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        client_ip = self._client_ip(request)
        try:
            self.limiter.check_rate_limit(client_ip)
        except ApiError as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.message, "code": "api_error"},
            )
        return await call_next(request)

    def _client_ip(self, request: Request) -> str:
        """Resolve a stable client IP, honoring the first forwarded address."""
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",", maxsplit=1)[0].strip()
        if request.client is None:
            return "unknown"
        return request.client.host
