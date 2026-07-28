from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.ai.base import BaseAIProvider
from app.ai.errors import ProviderResponseError
from app.ai.schemas import AIMessage, AIRequest

StructuredT = TypeVar("StructuredT", bound=BaseModel)

STRICT_JSON_INSTRUCTION = (
    "Return only valid JSON matching the requested schema. "
    "Do not include markdown, prose, comments, or trailing commas."
)


async def parse_json_with_retry(
    provider: BaseAIProvider,
    request: AIRequest,
    schema: type[StructuredT],
    max_attempts: int = 2,
) -> StructuredT:
    """Generate JSON, validate it with Pydantic, and retry malformed output."""
    current_request = request
    last_error: Exception | None = None
    for attempt in range(max_attempts):
        response = await provider.generate(current_request)
        try:
            return schema.model_validate_json(response.content)
        except ValidationError as exc:
            last_error = exc
            if attempt + 1 >= max_attempts:
                break
            current_request = _with_stricter_instruction(current_request)
    raise ProviderResponseError("Structured output validation failed.") from last_error


def _with_stricter_instruction(request: AIRequest) -> AIRequest:
    """Return a copy of the request with stricter JSON instructions."""
    messages = [
        AIMessage(role="system", content=STRICT_JSON_INSTRUCTION),
        *request.messages,
    ]
    return request.model_copy(update={"messages": messages})

