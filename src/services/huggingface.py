"""Hugging Face Inference API — chat, vision, image gen, audio."""

import io
from typing import Any

from huggingface_hub import InferenceClient

from src.config import ProviderKeys
from src.types import GenerationOptions

CHAT_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
CAPTION_MODEL = "Salesforce/blip-image-captioning-large"
VQA_MODEL = "Salesforce/blip-vqa-base"
IMAGE_GEN_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
ASR_MODEL = "openai/whisper-large-v3"


def _client(keys: ProviderKeys) -> InferenceClient:
    if not keys.has_huggingface():
        raise ValueError("HUGGINGFACE_API_KEY or HF_TOKEN is not set.")
    return InferenceClient(token=keys.huggingface)


def generate_text(
    prompt: str, keys: ProviderKeys, options: GenerationOptions
) -> tuple[str, str]:
    client = _client(keys)
    model = options.resolved_model(CHAT_MODEL)
    response = client.chat_completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=options.max_tokens,
        temperature=options.temperature,
    )
    text = _chat_text(response)
    return text, model


def analyze_image_bytes(
    image_bytes: bytes,
    prompt: str,
    keys: ProviderKeys,
    options: GenerationOptions,
) -> tuple[str, str]:
    client = _client(keys)
    is_caption_task = (
        not prompt.strip()
        or "describe this image" in prompt.lower()
    )
    if is_caption_task:
        model = options.resolved_model(CAPTION_MODEL)
        result = client.image_to_text(image=image_bytes, model=model)
        text = result if isinstance(result, str) else str(result)
        return text, model

    model = options.resolved_model(VQA_MODEL)
    result = client.visual_question_answering(
        image=image_bytes,
        question=prompt,
        model=model,
    )
    if isinstance(result, dict):
        text = result.get("answer") or result.get("generated_text") or str(result)
    else:
        text = str(result)
    return text, model


def generate_image_bytes(
    prompt: str, keys: ProviderKeys, options: GenerationOptions
) -> tuple[bytes, str]:
    client = _client(keys)
    model = options.resolved_model(IMAGE_GEN_MODEL)
    image = client.text_to_image(prompt=prompt, model=model)
    if isinstance(image, bytes):
        return image, model
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue(), model


def transcribe_audio_bytes(
    audio_bytes: bytes, keys: ProviderKeys, options: GenerationOptions
) -> tuple[str, str]:
    client = _client(keys)
    model = options.resolved_model(ASR_MODEL)
    result = client.automatic_speech_recognition(audio=audio_bytes, model=model)
    if isinstance(result, dict):
        text = result.get("text", "")
    else:
        text = str(result)
    return text, model


def describe_images(
    prompt: str,
    image_bytes_list: list[bytes],
    keys: ProviderKeys,
    options: GenerationOptions,
) -> tuple[str, str]:
    captions: list[str] = []
    caption_model = options.resolved_model(CAPTION_MODEL)
    client = _client(keys)
    for i, frame in enumerate(image_bytes_list, 1):
        cap = client.image_to_text(image=frame, model=caption_model)
        captions.append(f"Frame {i}: {cap if isinstance(cap, str) else str(cap)}")
    combined = "\n".join(captions)
    summary_prompt = f"{prompt}\n\nFrame captions:\n{combined}"
    return generate_text(summary_prompt, keys, options)


def _chat_text(response: Any) -> str:
    if isinstance(response, str):
        return response
    if isinstance(response, dict):
        choices = response.get("choices", [])
        if choices:
            msg = choices[0].get("message", {})
            return msg.get("content", "") or ""
        return response.get("generated_text", "") or str(response)
    if hasattr(response, "choices"):
        return response.choices[0].message.content or ""
    return str(response)
