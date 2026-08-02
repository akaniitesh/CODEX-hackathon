from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from app.ai.schemas import AIRequest, AIResponse, ProviderName, StreamResult

StructuredT = TypeVar("StructuredT", bound=BaseModel)


class BaseAIProvider(ABC):
    """Provider interface used by all AI model integrations."""

    name: ProviderName

    def __init__(self, name: ProviderName) -> None:
        self.name = name

    @abstractmethod
    async def generate(self, request: AIRequest) -> AIResponse:
        """Generate a complete model response."""

    @abstractmethod
    def stream(self, request: AIRequest) -> StreamResult:
        """Stream model response chunks."""

    @abstractmethod
    async def structured_output(
        self,
        request: AIRequest,
        schema: type[StructuredT],
    ) -> StructuredT:
        """Generate and validate a structured response."""

