"""Text → Video (placeholder) and Video → Text via frame sampling + vision."""

import base64
import io
import tempfile
from pathlib import Path

import cv2
from PIL import Image

from src.config import ProviderKeys
from src.providers import default_model, openai_client, uses_openai_chat_api
from src.services import anthropic as anthropic_svc
from src.services import huggingface as hf_svc
from src.services.gemini import describe_images
from src.types import GenerationOptions

MAX_FRAMES = 6


def _extract_frames(video_bytes: bytes, max_frames: int = MAX_FRAMES) -> list[bytes]:
    suffix = ".mp4"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(video_bytes)
        tmp_path = tmp.name

    frames: list[bytes] = []
    try:
        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            raise ValueError("Could not read video file.")

        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
        step = max(total // max_frames, 1)
        index = 0
        captured = 0

        while captured < max_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ok, frame = cap.read()
            if not ok:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=85)
            frames.append(buf.getvalue())
            index += step
            captured += 1
        cap.release()
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    if not frames:
        raise ValueError("No frames could be extracted from the video.")
    return frames


def describe_video(
    video_bytes: bytes,
    prompt: str,
    provider: str,
    keys: ProviderKeys,
    options: GenerationOptions,
) -> tuple[str, str]:
    provider = provider.lower()
    default_prompt = (
        "Summarize this video based on the key frames. Describe actions, "
        "setting, people or objects, and the overall narrative."
    )
    user_prompt = prompt.strip() or default_prompt
    frames = _extract_frames(video_bytes)
    model = options.resolved_model(default_model(provider))

    if provider == "google":
        return describe_images(user_prompt, frames, keys, options)

    if provider == "anthropic":
        return anthropic_svc.describe_images(user_prompt, frames, keys, options)

    if provider == "huggingface":
        return hf_svc.describe_images(user_prompt, frames, keys, options)

    if uses_openai_chat_api(provider):
        client = openai_client(provider, keys)
        content: list[dict] = [{"type": "text", "text": user_prompt}]
        for frame in frames:
            b64 = base64.standard_b64encode(frame).decode("utf-8")
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                }
            )
        kwargs: dict = {
            "model": model,
            "messages": [{"role": "user", "content": content}],
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
        return text, f"{model} (frame sampling)"

    raise ValueError(f"Video description not supported for provider: {provider}")


def generate_video_placeholder(prompt: str) -> tuple[str, str]:
    message = (
        f'Video generation requested for: "{prompt}"\n\n'
        "Full Text → Video APIs (Runway, Luma, OpenAI Sora) require separate "
        "credentials. Alternatives:\n"
        "1. Use OpenAI or a video API when you have access.\n"
        "2. Use image sequence tools (e.g. Stable Video Diffusion on Replicate).\n"
        "3. For class demo, show a pre-rendered sample clip in outputs/."
    )
    return message, "placeholder (configure Runway/Luma/Replicate for production)"
