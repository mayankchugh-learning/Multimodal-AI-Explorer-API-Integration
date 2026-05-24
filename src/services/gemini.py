"""Shared Google Gemini client (google-genai SDK)."""

from google import genai
from google.genai import types

from src.config import ProviderKeys
from src.types import GenerationOptions

GEMINI_MODEL = "gemini-2.0-flash"


def get_client(keys: ProviderKeys) -> genai.Client:
    if not keys.has_google():
        raise ValueError("Google API key is not set.")
    return genai.Client(api_key=keys.google)


def _gen_config(options: GenerationOptions) -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        temperature=options.temperature,
        max_output_tokens=options.max_tokens,
    )


def generate_text(
    prompt: str, keys: ProviderKeys, options: GenerationOptions
) -> tuple[str, str]:
    client = get_client(keys)
    model = options.resolved_model(GEMINI_MODEL)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=_gen_config(options),
    )
    return response.text or "", model


def analyze_image_bytes(
    image_bytes: bytes,
    prompt: str,
    keys: ProviderKeys,
    options: GenerationOptions,
    mime_type: str = "image/jpeg",
) -> tuple[str, str]:
    client = get_client(keys)
    model = options.resolved_model(GEMINI_MODEL)
    response = client.models.generate_content(
        model=model,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt,
        ],
        config=_gen_config(options),
    )
    return response.text or "", model


def transcribe_audio_bytes(
    audio_bytes: bytes,
    mime_type: str,
    keys: ProviderKeys,
    options: GenerationOptions,
) -> tuple[str, str]:
    client = get_client(keys)
    model = options.resolved_model(GEMINI_MODEL)
    response = client.models.generate_content(
        model=model,
        contents=[
            types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
            "Transcribe this audio accurately. Return only the transcript.",
        ],
        config=_gen_config(options),
    )
    return response.text or "", model


def describe_images(
    prompt: str,
    image_bytes_list: list[bytes],
    keys: ProviderKeys,
    options: GenerationOptions,
) -> tuple[str, str]:
    client = get_client(keys)
    model = options.resolved_model(GEMINI_MODEL)
    parts: list = [prompt]
    for frame in image_bytes_list:
        parts.append(types.Part.from_bytes(data=frame, mime_type="image/jpeg"))
    response = client.models.generate_content(
        model=model,
        contents=parts,
        config=_gen_config(options),
    )
    return response.text or "", f"{model} (frame sampling)"
