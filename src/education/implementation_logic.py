"""Step-by-step implementation logic for each modality (teaching)."""

from __future__ import annotations

MODALITY_LOGIC: dict[str, list[str]] = {
    "text_to_text": [
        "1. Read user text prompt from UI (Streamlit `text_area`).",
        "2. Load API key from `.env` or BYOK session state (`ProviderKeys`).",
        "3. Build `GenerationOptions` (temperature, max_tokens, model).",
        "4. Route to provider adapter in `src/services/text.py` → `chat_completion()`.",
        "5. Provider calls remote API (OpenAI-compatible, Groq, Gemini, or Anthropic).",
        "6. Parse response text and display in UI with model name metadata.",
    ],
    "text_to_image": [
        "1. Read image description prompt from UI.",
        "2. Validate provider supports image gen (OpenAI DALL-E or HF SDXL).",
        "3. Call `generate_image()` in `src/services/image.py`.",
        "4. OpenAI: `images.generate` → download URL bytes via HTTP.",
        "5. Hugging Face: `InferenceClient.text_to_image()` → PNG bytes.",
        "6. Render image in Streamlit with `st.image()`.",
    ],
    "image_to_text": [
        "1. Upload image file → read bytes in memory.",
        "2. Optional: user question; else default caption prompt.",
        "3. Route to vision path in `analyze_image()`.",
        "4. Gemini/Anthropic/OpenAI: send image + text in one multimodal request.",
        "5. Hugging Face: BLIP caption or BLIP-VQA for custom questions.",
        "6. Return description markdown to UI.",
    ],
    "text_to_audio": [
        "1. Read text to synthesize.",
        "2. Use OpenAI Audio API (`audio.speech.create`).",
        "3. Model `tts-1`, voice `alloy` → MP3 bytes.",
        "4. Stream audio in UI via `st.audio()`.",
    ],
    "audio_to_text": [
        "1. Upload or record audio → bytes + filename.",
        "2. OpenAI: temp file → Whisper `transcriptions.create`.",
        "3. Google: Gemini multimodal with audio `Part.from_bytes`.",
        "4. Hugging Face: `automatic_speech_recognition` with Whisper model.",
        "5. Show transcript in `st.text_area`.",
    ],
    "video_to_text": [
        "1. Upload video file → bytes.",
        "2. OpenCV extracts N key frames (evenly spaced).",
        "3. Each frame JPEG-encoded for vision APIs.",
        "4. Vision model summarizes frames + user focus prompt.",
        "5. HF path: caption each frame with BLIP, then LLM summary chain.",
        "6. Display narrative summary.",
    ],
    "text_to_video": [
        "1. Educational placeholder — production needs Runway/Veo/Sora APIs.",
        "2. Typical flow: text prompt → video model → poll job → MP4 URL.",
        "3. LangChain would wrap tool/agent calling external video API.",
    ],
}

PROVIDER_LOGIC: dict[str, dict[str, str]] = {
    "openai": {
        "text_to_text": "SDK: `openai.OpenAI().chat.completions.create(messages=...)`",
        "text_to_image": "SDK: `client.images.generate(model='dall-e-3', prompt=...)`",
        "image_to_text": "Chat Completions with `image_url` base64 content block.",
        "text_to_audio": "SDK: `client.audio.speech.create(model='tts-1', ...)`",
        "audio_to_text": "SDK: `client.audio.transcriptions.create(model='whisper-1', file=...)`",
        "video_to_text": "Multi-image message in chat completion (frame sampling).",
    },
    "google": {
        "text_to_text": "SDK: `google.genai.Client().models.generate_content()`",
        "image_to_text": "Gemini `Part.from_bytes` + text in `generate_content`.",
        "audio_to_text": "Audio bytes as multimodal `Part` + transcript instruction.",
        "video_to_text": "Multiple image parts + summary prompt.",
    },
    "anthropic": {
        "text_to_text": "SDK: `anthropic.Anthropic().messages.create()`",
        "image_to_text": "Messages API with base64 image block + text block.",
        "video_to_text": "Multiple image blocks in one Claude message.",
    },
    "groq": {
        "text_to_text": "SDK: `groq.Groq().chat.completions.create()` — OpenAI-compatible.",
    },
    "openrouter": {
        "text_to_text": "OpenAI client with `base_url='https://openrouter.ai/api/v1'`.",
        "image_to_text": "Same client; model slug e.g. `openai/gpt-4o-mini`.",
        "video_to_text": "Vision via OpenRouter-routed multimodal models.",
    },
    "huggingface": {
        "text_to_text": "`InferenceClient.chat_completion(model=..., messages=...)`.",
        "text_to_image": "`InferenceClient.text_to_image(model='stabilityai/stable-diffusion-xl-base-1.0')`.",
        "image_to_text": "`image_to_text` or `visual_question_answering` on Inference API.",
        "audio_to_text": "`automatic_speech_recognition` with Whisper model id.",
        "video_to_text": "Per-frame `image_to_text` then chat summary.",
    },
    "ollama": {
        "text_to_text": "OpenAI-compatible client → `base_url=http://localhost:11434/v1`.",
        "image_to_text": "Local vision model (llava) via chat completions + image_url.",
        "video_to_text": "Frame sampling + local vision model.",
    },
}


def get_logic_steps(modality_id: str) -> list[str]:
    return MODALITY_LOGIC.get(modality_id, ["No logic documented for this modality."])


def get_provider_note(modality_id: str, provider: str) -> str:
    provider = provider.lower()
    return PROVIDER_LOGIC.get(provider, {}).get(
        modality_id,
        f"No provider-specific note for **{provider}** on this modality.",
    )
