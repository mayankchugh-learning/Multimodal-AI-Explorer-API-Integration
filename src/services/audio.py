"""Text → Audio and Audio → Text."""

import tempfile
from pathlib import Path

from openai import OpenAI

from src.config import ProviderKeys
from src.services import huggingface as hf_svc
from src.services.gemini import transcribe_audio_bytes
from src.types import GenerationOptions

TTS_MODEL = "tts-1"
TTS_VOICE = "alloy"
WHISPER_MODEL = "whisper-1"


def generate_speech(
    text: str, provider: str, keys: ProviderKeys, options: GenerationOptions
) -> tuple[bytes, str]:
    provider = provider.lower()

    if provider == "openai":
        if not keys.has_openai():
            raise ValueError("OpenAI API key is not set.")
        client = OpenAI(api_key=keys.openai)
        response = client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=text,
        )
        return response.content, f"{TTS_MODEL} ({TTS_VOICE})"

    raise ValueError(
        f"Speech generation is only supported via OpenAI (selected: {provider})."
    )


def transcribe_audio(
    audio_bytes: bytes,
    filename: str,
    provider: str,
    keys: ProviderKeys,
    options: GenerationOptions,
) -> tuple[str, str]:
    provider = provider.lower()
    suffix = Path(filename).suffix or ".wav"

    if provider == "openai":
        if not keys.has_openai():
            raise ValueError("OpenAI API key is not set.")
        client = OpenAI(api_key=keys.openai)
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        try:
            with open(tmp_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model=WHISPER_MODEL,
                    file=audio_file,
                )
            return transcript.text, WHISPER_MODEL
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    if provider == "google":
        mime_map = {
            ".wav": "audio/wav",
            ".mp3": "audio/mp3",
            ".m4a": "audio/mp4",
            ".ogg": "audio/ogg",
            ".webm": "audio/webm",
        }
        mime = mime_map.get(suffix.lower(), "audio/mpeg")
        return transcribe_audio_bytes(audio_bytes, mime, keys, options)

    if provider == "huggingface":
        return hf_svc.transcribe_audio_bytes(audio_bytes, keys, options)

    raise ValueError(f"Transcription not supported for provider: {provider}")
