"""Text → Image and Image → Text."""

import base64

import httpx
from openai import OpenAI

from src.config import ProviderKeys
from src.providers import default_model, openai_client, uses_openai_chat_api
from src.services import anthropic as anthropic_svc
from src.services import huggingface as hf_svc
from src.services.gemini import analyze_image_bytes
from src.types import GenerationOptions

DALLE_MODEL = "dall-e-3"


def generate_image(
    prompt: str, provider: str, keys: ProviderKeys, options: GenerationOptions
) -> tuple[bytes, str]:
    provider = provider.lower()

    if provider == "openai":
        if not keys.has_openai():
            raise ValueError("OpenAI API key is not set.")
        client = OpenAI(api_key=keys.openai)
        result = client.images.generate(
            model=DALLE_MODEL,
            prompt=prompt,
            size="1024x1024",
            n=1,
        )
        image_url = result.data[0].url
        if not image_url:
            raise RuntimeError("No image URL returned from DALL-E.")
        response = httpx.get(image_url, timeout=60)
        response.raise_for_status()
        return response.content, DALLE_MODEL

    if provider == "huggingface":
        return hf_svc.generate_image_bytes(prompt, keys, options)

    if provider in ("google", "groq", "openrouter", "anthropic", "ollama"):
        raise ValueError(
            f"{provider} image generation is not wired here. Use **openai** or **huggingface**."
        )

    raise ValueError(f"Image generation not supported for provider: {provider}")


def analyze_image(
    image_bytes: bytes,
    prompt: str,
    provider: str,
    keys: ProviderKeys,
    options: GenerationOptions,
) -> tuple[str, str]:
    provider = provider.lower()
    default_prompt = (
        "Describe this image in detail. Include objects, colors, setting, and mood."
    )
    user_prompt = prompt.strip() or default_prompt
    model = options.resolved_model(default_model(provider))

    if provider == "google":
        return analyze_image_bytes(image_bytes, user_prompt, keys, options)

    if provider == "anthropic":
        return anthropic_svc.analyze_image_bytes(image_bytes, user_prompt, keys, options)

    if provider == "huggingface":
        return hf_svc.analyze_image_bytes(image_bytes, user_prompt, keys, options)

    if uses_openai_chat_api(provider):
        client = openai_client(provider, keys)
        b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
        kwargs: dict = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                        },
                    ],
                }
            ],
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

    raise ValueError(f"Image analysis not supported for provider: {provider}")
