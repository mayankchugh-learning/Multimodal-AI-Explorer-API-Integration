"""Provider clients and default models."""

from openai import OpenAI
from groq import Groq

from src.config import ProviderKeys

DEFAULT_MODELS: dict[str, str] = {
    "openai": "gpt-4o-mini",
    "google": "gemini-2.0-flash",
    "groq": "llama-3.3-70b-versatile",
    "openrouter": "openai/gpt-4o-mini",
    "anthropic": "claude-3-5-sonnet-20241022",
    "huggingface": "meta-llama/Meta-Llama-3-8B-Instruct",
    "ollama": "llama3.1:8b",
}

OPENROUTER_BASE = "https://openrouter.ai/api/v1"

VISION_PROVIDERS = frozenset(
    {"openai", "google", "openrouter", "ollama", "anthropic", "huggingface"}
)


def default_model(provider: str) -> str:
    return DEFAULT_MODELS.get(provider.lower(), "gpt-4o-mini")


def openai_client(provider: str, keys: ProviderKeys) -> OpenAI:
    provider = provider.lower()
    if provider == "openai":
        if not keys.has_openai():
            raise ValueError("OpenAI API key is not set.")
        return OpenAI(api_key=keys.openai)
    if provider == "openrouter":
        if not keys.has_openrouter():
            raise ValueError("OpenRouter API key is not set.")
        return OpenAI(base_url=OPENROUTER_BASE, api_key=keys.openrouter)
    if provider == "ollama":
        return OpenAI(base_url=keys.ollama_base_url.rstrip("/"), api_key="ollama")
    raise ValueError(f"Provider {provider} is not OpenAI-compatible.")


def groq_client(keys: ProviderKeys) -> Groq:
    if not keys.has_groq():
        raise ValueError("Groq API key is not set.")
    return Groq(api_key=keys.groq)


def uses_openai_chat_api(provider: str) -> bool:
    return provider.lower() in ("openai", "openrouter", "ollama")


def supports_vision(provider: str) -> bool:
    return provider.lower() in VISION_PROVIDERS
