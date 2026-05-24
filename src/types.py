"""Shared request types."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GenerationOptions:
    temperature: float = 0.7
    max_tokens: int = 1024
    model: str | None = None

    def resolved_model(self, default: str) -> str:
        return self.model.strip() if self.model and self.model.strip() else default
