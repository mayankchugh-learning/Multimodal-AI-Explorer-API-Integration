"""Text → Text across all providers."""

from groq import Groq

from src.config import ProviderKeys
from src.providers import (
    default_model,
    groq_client,
    openai_client,
    uses_openai_chat_api,
)
from src.services import anthropic as anthropic_svc
from src.services import huggingface as hf_svc
from src.services.errors import format_provider_error
from src.services.gemini import generate_text as gemini_generate_text
from src.types import GenerationOptions


def chat_completion(
    prompt: str,
    provider: str,
    keys: ProviderKeys,
    options: GenerationOptions,
) -> tuple[str, str]:
    provider = provider.lower()
    model = options.resolved_model(default_model(provider))

    if provider == "google":
        return gemini_generate_text(prompt, keys, options)

    if provider == "anthropic":
        return anthropic_svc.generate_text(prompt, keys, options)

    if provider == "huggingface":
        return hf_svc.generate_text(prompt, keys, options)

    if provider == "groq":
        client = groq_client(keys)
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=options.temperature,
                max_tokens=options.max_tokens,
            )
        except Exception as exc:
            raise ValueError(format_provider_error("groq", exc)) from exc
        text = response.choices[0].message.content or ""
        return text, model

    if uses_openai_chat_api(provider):
        client = openai_client(provider, keys)
        kwargs: dict = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": options.temperature,
            "max_tokens": options.max_tokens,
        }
        if provider == "openrouter":
            kwargs["extra_headers"] = {
                "HTTP-Referer": "https://github.com/multimodal-ai-explorer",
                "X-Title": "Multimodal AI Explorer",
            }
        response = client.chat.completions.create(**kwargs)
        text = response.choices[0].message.content or ""
        return text, model

    raise ValueError(f"Unknown provider: {provider}")
