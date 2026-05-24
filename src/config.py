"""API key and provider configuration."""

import os
from dataclasses import dataclass, replace

from dotenv import load_dotenv

load_dotenv()

DEFAULT_OLLAMA_BASE = "http://localhost:11434/v1"


@dataclass(frozen=True)
class ProviderKeys:
    openai: str | None = None
    google: str | None = None
    groq: str | None = None
    openrouter: str | None = None
    anthropic: str | None = None
    huggingface: str | None = None
    ollama_base_url: str = DEFAULT_OLLAMA_BASE

    def has_openai(self) -> bool:
        return bool(self.openai)

    def has_google(self) -> bool:
        return bool(self.google)

    def has_groq(self) -> bool:
        return bool(self.groq)

    def has_openrouter(self) -> bool:
        return bool(self.openrouter)

    def has_anthropic(self) -> bool:
        return bool(self.anthropic)

    def has_huggingface(self) -> bool:
        return bool(self.huggingface)

    def has_ollama(self) -> bool:
        return bool(self.ollama_base_url)

    def available_providers(self) -> list[str]:
        providers: list[str] = []
        if self.has_openai():
            providers.append("openai")
        if self.has_google():
            providers.append("google")
        if self.has_groq():
            providers.append("groq")
        if self.has_openrouter():
            providers.append("openrouter")
        if self.has_anthropic():
            providers.append("anthropic")
        if self.has_huggingface():
            providers.append("huggingface")
        if self.has_ollama():
            providers.append("ollama")
        return providers


def get_keys() -> ProviderKeys:
    return ProviderKeys(
        openai=os.getenv("OPENAI_API_KEY"),
        google=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"),
        groq=os.getenv("GROQ_API_KEY"),
        openrouter=os.getenv("OPENROUTER_API_KEY"),
        anthropic=os.getenv("ANTHROPIC_API_KEY"),
        huggingface=(
            os.getenv("HUGGINGFACE_API_KEY")
            or os.getenv("HUGGINGFACEHUB_API_TOKEN")
            or os.getenv("HF_TOKEN")
        ),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE),
    )


def merge_keys(env: ProviderKeys, overrides: dict[str, str | None]) -> ProviderKeys:
    """Apply BYOK overrides; non-empty session values win over .env."""

    def pick(name: str, current: str | None) -> str | None:
        value = overrides.get(name)
        if value and str(value).strip():
            return str(value).strip()
        return current

    return replace(
        env,
        openai=pick("openai", env.openai),
        google=pick("google", env.google),
        groq=pick("groq", env.groq),
        openrouter=pick("openrouter", env.openrouter),
        anthropic=pick("anthropic", env.anthropic),
        huggingface=pick("huggingface", env.huggingface),
        ollama_base_url=pick("ollama_base_url", env.ollama_base_url) or DEFAULT_OLLAMA_BASE,
    )
