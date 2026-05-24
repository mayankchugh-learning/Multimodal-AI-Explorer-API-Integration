"""Provider and model recommendations per modality."""

from dataclasses import dataclass
from typing import Literal

from src.config import ProviderKeys

Rating = Literal["best", "good", "supported", "unsupported"]

RATING_LABEL = {
    "best": "⭐ Best",
    "good": "✓ Good",
    "supported": "○ Supported",
    "unsupported": "— N/A",
}


@dataclass(frozen=True)
class ModelRecommendation:
    provider: str
    model: str
    rating: Rating
    note: str

    @property
    def provider_label(self) -> str:
        labels = {
            "openai": "OpenAI",
            "google": "Google Gemini",
            "groq": "Groq",
            "openrouter": "OpenRouter",
            "anthropic": "Anthropic",
            "huggingface": "Hugging Face",
            "ollama": "Ollama (local)",
        }
        return labels.get(self.provider, self.provider.title())


@dataclass(frozen=True)
class ModalityInfo:
    id: str
    label: str
    description: str
    models: tuple[ModelRecommendation, ...]

    def best_options(self) -> list[ModelRecommendation]:
        return [m for m in self.models if m.rating == "best"]

    def supported_providers(self) -> list[str]:
        return [m.provider for m in self.models if m.rating != "unsupported"]


def _provider_ready(provider: str, keys: ProviderKeys) -> bool:
    checks = {
        "openai": keys.has_openai,
        "google": keys.has_google,
        "groq": keys.has_groq,
        "openrouter": keys.has_openrouter,
        "anthropic": keys.has_anthropic,
        "huggingface": keys.has_huggingface,
        "ollama": keys.has_ollama,
    }
    check = checks.get(provider)
    return check() if check else False


MODALITIES: dict[str, ModalityInfo] = {
    "text_to_text": ModalityInfo(
        id="text_to_text",
        label="Text → Text",
        description="General chat, Q&A, reasoning, and writing.",
        models=(
            ModelRecommendation("openai", "gpt-4o-mini", "best", "Balanced quality, cost, and reliability"),
            ModelRecommendation("google", "gemini-2.0-flash", "best", "Fast responses; strong multimodal stack"),
            ModelRecommendation("groq", "llama-3.3-70b-versatile", "best", "Very fast inference; great for demos"),
            ModelRecommendation("openrouter", "openai/gpt-4o-mini", "best", "Same model family; 100+ alternatives via one key"),
            ModelRecommendation("openrouter", "anthropic/claude-3.5-sonnet", "good", "Higher quality when you need stronger reasoning"),
            ModelRecommendation("anthropic", "claude-3-5-sonnet-20241022", "best", "Top-tier reasoning and writing quality"),
            ModelRecommendation("anthropic", "claude-3-5-haiku-20241022", "good", "Faster, lower-cost Claude variant"),
            ModelRecommendation("huggingface", "meta-llama/Meta-Llama-3-8B-Instruct", "best", "Open models via Inference API"),
            ModelRecommendation("huggingface", "mistralai/Mistral-7B-Instruct-v0.3", "good", "Lightweight HF chat model"),
            ModelRecommendation("ollama", "llama3.1:8b", "best", "Free, private, offline — run locally with Ollama"),
            ModelRecommendation("ollama", "mistral:7b", "good", "Lighter local model for quick tests"),
        ),
    ),
    "text_to_image": ModalityInfo(
        id="text_to_image",
        label="Text → Image",
        description="Generate images from a text prompt.",
        models=(
            ModelRecommendation("openai", "dall-e-3", "best", "Highest quality image generation in this app"),
            ModelRecommendation("huggingface", "stabilityai/stable-diffusion-xl-base-1.0", "best", "SDXL via HF Inference API"),
            ModelRecommendation("google", "—", "unsupported", "Imagen requires Vertex AI (not wired here)"),
            ModelRecommendation("anthropic", "—", "unsupported", "No image generation API"),
            ModelRecommendation("groq", "—", "unsupported", "No image generation API"),
            ModelRecommendation("openrouter", "—", "unsupported", "Use OpenAI or Hugging Face here"),
            ModelRecommendation("ollama", "—", "unsupported", "No image generation in Ollama chat API"),
        ),
    ),
    "image_to_text": ModalityInfo(
        id="image_to_text",
        label="Image → Text",
        description="Describe images or answer questions about them.",
        models=(
            ModelRecommendation("google", "gemini-2.0-flash", "best", "Strong native vision; fast and cost-effective"),
            ModelRecommendation("openai", "gpt-4o-mini", "best", "Reliable vision via GPT-4o mini"),
            ModelRecommendation("anthropic", "claude-3-5-sonnet-20241022", "best", "Excellent vision + reasoning"),
            ModelRecommendation("huggingface", "Salesforce/blip-image-captioning-large", "best", "Captioning via HF Inference"),
            ModelRecommendation("huggingface", "Salesforce/blip-vqa-base", "good", "Visual Q&A for custom questions"),
            ModelRecommendation("openrouter", "openai/gpt-4o-mini", "good", "Vision via OpenRouter routing"),
            ModelRecommendation("openrouter", "google/gemini-2.0-flash-001", "good", "Gemini vision through OpenRouter"),
            ModelRecommendation("ollama", "llava", "good", "Popular local vision model — `ollama pull llava`"),
            ModelRecommendation("ollama", "llama3.2-vision", "good", "Newer local vision model when available"),
            ModelRecommendation("groq", "—", "unsupported", "No vision on Groq in this app"),
        ),
    ),
    "text_to_audio": ModalityInfo(
        id="text_to_audio",
        label="Text → Audio",
        description="Convert text to natural-sounding speech.",
        models=(
            ModelRecommendation("openai", "tts-1 (voice: alloy)", "best", "Only provider wired for TTS in this app"),
            ModelRecommendation("openai", "tts-1-hd", "good", "Higher fidelity speech (set as model override)"),
            ModelRecommendation("google", "—", "unsupported", "Gemini TTS not integrated here"),
            ModelRecommendation("anthropic", "—", "unsupported", "No TTS API"),
            ModelRecommendation("huggingface", "—", "unsupported", "No TTS in this app (use OpenAI)"),
            ModelRecommendation("groq", "—", "unsupported", "No TTS API"),
            ModelRecommendation("openrouter", "—", "unsupported", "No TTS via chat API"),
            ModelRecommendation("ollama", "—", "unsupported", "No TTS in Ollama API"),
        ),
    ),
    "audio_to_text": ModalityInfo(
        id="audio_to_text",
        label="Audio → Text",
        description="Transcribe uploaded or recorded audio.",
        models=(
            ModelRecommendation("openai", "whisper-1", "best", "Industry-standard accuracy for transcription"),
            ModelRecommendation("google", "gemini-2.0-flash", "good", "Multimodal transcription via Gemini"),
            ModelRecommendation("huggingface", "openai/whisper-large-v3", "good", "Whisper via HF Inference API"),
            ModelRecommendation("anthropic", "—", "unsupported", "No STT API"),
            ModelRecommendation("groq", "—", "unsupported", "No Whisper endpoint in this app"),
            ModelRecommendation("openrouter", "—", "unsupported", "Use OpenAI, Gemini, or Hugging Face"),
            ModelRecommendation("ollama", "—", "unsupported", "No audio STT in Ollama chat API"),
        ),
    ),
    "video_to_text": ModalityInfo(
        id="video_to_text",
        label="Video → Text",
        description="Summarize video using extracted key frames + vision.",
        models=(
            ModelRecommendation("google", "gemini-2.0-flash", "best", "Excellent at multi-image / scene understanding"),
            ModelRecommendation("openai", "gpt-4o-mini", "best", "Solid frame-based video summaries"),
            ModelRecommendation("anthropic", "claude-3-5-sonnet-20241022", "best", "Multi-image Claude summaries"),
            ModelRecommendation("huggingface", "Salesforce/blip-image-captioning-large", "good", "Per-frame captions + LLM summary"),
            ModelRecommendation("openrouter", "google/gemini-2.0-flash-001", "good", "Gemini vision via OpenRouter"),
            ModelRecommendation("openrouter", "openai/gpt-4o-mini", "good", "GPT vision via OpenRouter"),
            ModelRecommendation("ollama", "llava", "good", "Local frame analysis — slower on CPU"),
            ModelRecommendation("groq", "—", "unsupported", "No vision API on Groq here"),
        ),
    ),
    "text_to_video": ModalityInfo(
        id="text_to_video",
        label="Text → Video",
        description="Video generation APIs (informational in this app).",
        models=(
            ModelRecommendation("openai", "sora (preview)", "good", "When you have API access"),
            ModelRecommendation("google", "veo (Vertex)", "good", "Enterprise video generation"),
            ModelRecommendation("openrouter", "—", "unsupported", "No video gen route"),
            ModelRecommendation("anthropic", "—", "unsupported", "No video gen"),
            ModelRecommendation("huggingface", "—", "unsupported", "No video gen in this app"),
            ModelRecommendation("groq", "—", "unsupported", "No video gen"),
            ModelRecommendation("ollama", "—", "unsupported", "No video gen"),
        ),
    ),
}


def get_modality(modality_id: str) -> ModalityInfo:
    if modality_id not in MODALITIES:
        raise KeyError(f"Unknown modality: {modality_id}")
    return MODALITIES[modality_id]


def list_modalities() -> list[ModalityInfo]:
    return list(MODALITIES.values())


def best_for_modality(modality_id: str, keys: ProviderKeys) -> ModelRecommendation | None:
    """First best-rated option that has credentials configured."""
    modality = get_modality(modality_id)
    for option in modality.best_options():
        if _provider_ready(option.provider, keys):
            return option
    for option in modality.models:
        if option.rating in ("best", "good") and _provider_ready(option.provider, keys):
            return option
    return None
