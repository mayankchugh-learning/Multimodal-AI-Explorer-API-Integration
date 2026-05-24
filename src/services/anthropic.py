"""Anthropic Claude API — text and vision."""

import base64

import anthropic

from src.config import ProviderKeys
from src.types import GenerationOptions

DEFAULT_MODEL = "claude-3-5-sonnet-20241022"


def _client(keys: ProviderKeys) -> anthropic.Anthropic:
    if not keys.has_anthropic():
        raise ValueError("ANTHROPIC_API_KEY is not set.")
    return anthropic.Anthropic(api_key=keys.anthropic)


def generate_text(
    prompt: str, keys: ProviderKeys, options: GenerationOptions
) -> tuple[str, str]:
    client = _client(keys)
    model = options.resolved_model(DEFAULT_MODEL)
    message = client.messages.create(
        model=model,
        max_tokens=options.max_tokens,
        temperature=options.temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    text = _extract_text(message)
    return text, model


def analyze_image_bytes(
    image_bytes: bytes,
    prompt: str,
    keys: ProviderKeys,
    options: GenerationOptions,
    media_type: str = "image/jpeg",
) -> tuple[str, str]:
    client = _client(keys)
    model = options.resolved_model(DEFAULT_MODEL)
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    message = client.messages.create(
        model=model,
        max_tokens=options.max_tokens,
        temperature=options.temperature,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    return _extract_text(message), model


def describe_images(
    prompt: str,
    image_bytes_list: list[bytes],
    keys: ProviderKeys,
    options: GenerationOptions,
) -> tuple[str, str]:
    client = _client(keys)
    model = options.resolved_model(DEFAULT_MODEL)
    content: list[dict] = []
    for frame in image_bytes_list:
        b64 = base64.standard_b64encode(frame).decode("utf-8")
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": b64,
                },
            }
        )
    content.append({"type": "text", "text": prompt})
    message = client.messages.create(
        model=model,
        max_tokens=options.max_tokens,
        temperature=options.temperature,
        messages=[{"role": "user", "content": content}],
    )
    return _extract_text(message), f"{model} (frame sampling)"


def _extract_text(message: anthropic.types.Message) -> str:
    parts: list[str] = []
    for block in message.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    return "".join(parts)
