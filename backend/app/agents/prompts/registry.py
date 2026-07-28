from __future__ import annotations

import string
from pathlib import Path
from typing import Any

from app.core.errors import ApiError


class PromptRegistry:
    """Versioned prompt template registry for agent modules."""

    def __init__(self, templates_dir: Path | None = None) -> None:
        if templates_dir is None:
            templates_dir = Path(__file__).parent / "templates"
        self.templates_dir = templates_dir.resolve()

    def get_prompt(
        self,
        prompt_id: str,
        version: str = "v1",
        **kwargs: Any,
    ) -> str:
        """Load a versioned prompt template and format it with provided variables."""
        template_file = self.templates_dir / f"{prompt_id}_{version}.txt"
        if not template_file.exists():
            raise ApiError(
                f"Prompt template '{prompt_id}_{version}' not found in registry.",
                404,
            )

        template_text = template_file.read_text(encoding="utf-8")
        required_vars = self._extract_variables(template_text)

        missing = [var for var in required_vars if var not in kwargs]
        if missing:
            vars_str = ", ".join(missing)
            raise ValueError(
                f"Prompt '{prompt_id}_{version}' missing required variables: {vars_str}"
            )

        formatted_kwargs = {
            k: (str(v) if not isinstance(v, str) else v) for k, v in kwargs.items()
        }
        return template_text.format(**formatted_kwargs)

    def _extract_variables(self, template_text: str) -> set[str]:
        """Extract formatting placeholders from template string."""
        formatter = string.Formatter()
        return {
            field_name
            for _, field_name, _, _ in formatter.parse(template_text)
            if field_name is not None
        }


prompt_registry = PromptRegistry()
