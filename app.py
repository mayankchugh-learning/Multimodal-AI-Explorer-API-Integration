"""
Multimodal AI Explorer — Streamlit web application.

Supports text, image, audio, and video inputs with AI-powered outputs.
Providers: OpenAI, Gemini, Groq, OpenRouter, Anthropic, Hugging Face, Ollama.
"""

import io
import sys
from pathlib import Path

import streamlit as st
from PIL import Image

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import get_keys, merge_keys
from src.providers import default_model
from src.ui_api_keys import render_api_key_tables
from src.ui_education import render_learning_panel
from src.ui_recommendations import render_modality_recommendations, render_sidebar_modality_picker
from src.services import (
    analyze_image,
    chat_completion,
    describe_video,
    generate_image,
    generate_speech,
    generate_video_placeholder,
    transcribe_audio,
)
from src.services.connectivity import test_groq
from src.types import GenerationOptions

st.set_page_config(
    page_title="Multimodal AI Explorer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-header { font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem; }
    .sub-header { color: #6b7280; margin-bottom: 1.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="main-header">Multimodal AI Explorer</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">OpenAI · Gemini · Groq · OpenRouter · Anthropic · Hugging Face · Ollama</p>',
    unsafe_allow_html=True,
)


def _show_error(exc: Exception) -> None:
    msg = str(exc)
    if "**" in msg:
        st.markdown(msg)
    else:
        st.error(msg)


def _byok_overrides() -> dict[str, str | None]:
    return {
        "openai": st.session_state.get("byok_openai"),
        "google": st.session_state.get("byok_google"),
        "groq": st.session_state.get("byok_groq"),
        "openrouter": st.session_state.get("byok_openrouter"),
        "anthropic": st.session_state.get("byok_anthropic"),
        "huggingface": st.session_state.get("byok_huggingface"),
        "ollama_base_url": st.session_state.get("byok_ollama_url"),
    }


def _init_session() -> None:
    defaults = {
        "byok_openai": "",
        "byok_google": "",
        "byok_groq": "",
        "byok_openrouter": "",
        "byok_anthropic": "",
        "byok_huggingface": "",
        "byok_ollama_url": "",
        "temperature": 0.7,
        "max_tokens": 1024,
        "model_override": "",
        "provider": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


_init_session()
env_keys = get_keys()
keys = merge_keys(env_keys, _byok_overrides())

with st.sidebar:
    st.header("Settings")

    with st.expander("🔑 Bring Your Own Key (BYOK)", expanded=False):
        st.caption(
            "Optional session keys override `.env`. Keys stay in this browser tab only "
            "and are never saved to disk."
        )
        st.text_input(
            "OpenAI API key",
            type="password",
            placeholder="sk-...",
            key="byok_openai",
        )
        st.text_input(
            "Google / Gemini API key",
            type="password",
            placeholder="AIza...",
            key="byok_google",
        )
        st.text_input(
            "Groq API key",
            type="password",
            placeholder="gsk_...",
            key="byok_groq",
        )
        st.text_input(
            "OpenRouter API key",
            type="password",
            placeholder="sk-or-...",
            key="byok_openrouter",
        )
        st.text_input(
            "Anthropic API key",
            type="password",
            placeholder="sk-ant-...",
            key="byok_anthropic",
        )
        st.text_input(
            "Hugging Face token",
            type="password",
            placeholder="hf_...",
            key="byok_huggingface",
        )
        st.text_input(
            "Ollama base URL",
            placeholder=env_keys.ollama_base_url,
            key="byok_ollama_url",
        )

    with st.expander("📋 API keys → `.env` variable names", expanded=False):
        render_api_key_tables()

    keys = merge_keys(env_keys, _byok_overrides())

    def status(has: bool) -> str:
        return "✅" if has else "❌"

    st.markdown("**Provider status**")
    st.markdown(
        f"- OpenAI: {status(keys.has_openai())}\n"
        f"- Google Gemini: {status(keys.has_google())}\n"
        f"- Groq: {status(keys.has_groq())}\n"
        f"- OpenRouter: {status(keys.has_openrouter())}\n"
        f"- Anthropic: {status(keys.has_anthropic())}\n"
        f"- Hugging Face: {status(keys.has_huggingface())}\n"
        f"- Ollama: {status(keys.has_ollama())} (`{keys.ollama_base_url}`)"
    )

    provider_options = keys.available_providers()
    if "ollama" not in provider_options:
        provider_options.append("ollama")

    if not provider_options:
        st.error("Add API keys in BYOK above or in a `.env` file.")
        st.stop()

    if not st.session_state.provider or st.session_state.provider not in provider_options:
        recommended = None
        try:
            from src.modality_catalog import best_for_modality

            recommended = best_for_modality("text_to_text", keys)
        except Exception:
            pass
        st.session_state.provider = (
            recommended.provider if recommended else provider_options[0]
        )

    provider = st.selectbox("Provider", provider_options, key="provider")

    if provider == "groq" and keys.has_groq():
        if st.button("Test Groq connection", key="test_groq_conn", width="stretch"):
            with st.spinner("Calling Groq API..."):
                ok, msg = test_groq(keys)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
                st.caption(
                    "403 often means your network blocks api.groq.com. Try hotspot, "
                    "disable VPN, or use OpenRouter instead."
                )

    st.divider()
    render_sidebar_modality_picker(keys, provider)

    st.divider()
    st.subheader("Generation")
    st.slider("Temperature", min_value=0.0, max_value=2.0, step=0.1, key="temperature")
    st.number_input(
        "Max tokens",
        min_value=64,
        max_value=8192,
        step=64,
        key="max_tokens",
    )
    st.text_input(
        "Model override (optional)",
        placeholder=default_model(provider),
        help="Leave blank to use the provider default model.",
        key="model_override",
    )

    gen_options = GenerationOptions(
        temperature=float(st.session_state.temperature),
        max_tokens=int(st.session_state.max_tokens),
        model=st.session_state.model_override.strip() or None,
    )

    st.caption(f"Active: **{provider}** → `{gen_options.resolved_model(default_model(provider))}`")

    st.divider()
    active_modality = st.session_state.get("sidebar_modality", "text_to_text")
    render_learning_panel(
        active_modality,
        provider,
        gen_options.model,
        key_prefix="sidebar_learn",
    )

tab_text, tab_image, tab_audio, tab_video = st.tabs(
    ["📝 Text", "🖼️ Image", "🎵 Audio", "🎬 Video"]
)

# --- Text tab ---
with tab_text:
    render_modality_recommendations("text_to_text", keys, provider, key_prefix="tab_t2t")
    render_learning_panel("text_to_text", provider, gen_options.model, key_prefix="learn_t2t")

    st.subheader("Text → Text")
    st.caption("Chat completion with temperature and max tokens from the sidebar.")
    text_prompt = st.text_area(
        "Your message",
        placeholder="Explain how transformers work in simple terms.",
        height=120,
        key="text_prompt",
    )
    if st.button("Generate response", key="btn_text", type="primary"):
        if not text_prompt.strip():
            st.warning("Enter a message first.")
        else:
            with st.spinner("Generating..."):
                try:
                    result, model = chat_completion(
                        text_prompt, provider, keys, gen_options
                    )
                    st.success(f"Model: `{model}` · temp={gen_options.temperature}")
                    st.markdown(result)
                except Exception as exc:
                    _show_error(exc)

    st.divider()
    render_modality_recommendations("text_to_image", keys, provider, key_prefix="tab_t2i")
    render_learning_panel("text_to_image", provider, gen_options.model, key_prefix="learn_t2i")

    st.subheader("Text → Image")
    st.caption("OpenAI DALL-E 3 or Hugging Face Stable Diffusion XL.")
    image_prompt = st.text_input(
        "Image description",
        placeholder="A watercolor painting of a robot reading in a library.",
        key="image_gen_prompt",
    )
    img_provider = st.selectbox(
        "Image provider",
        [p for p in ("openai", "huggingface") if getattr(keys, f"has_{p}")()],
        key="text_to_image_provider",
    ) if (keys.has_openai() or keys.has_huggingface()) else None

    if st.button("Generate image", key="btn_image_gen"):
        if not keys.has_openai() and not keys.has_huggingface():
            st.warning("Set OpenAI or Hugging Face key for image generation.")
        elif not image_prompt.strip():
            st.warning("Enter an image description.")
        else:
            use_provider = img_provider or ("openai" if keys.has_openai() else "huggingface")
            with st.spinner("Creating image..."):
                try:
                    img_bytes, model = generate_image(
                        image_prompt, use_provider, keys, gen_options
                    )
                    st.success(f"Model: `{model}`")
                    st.image(Image.open(io.BytesIO(img_bytes)), width="stretch")
                except Exception as exc:
                    st.error(str(exc))

# --- Image tab ---
with tab_image:
    render_modality_recommendations("image_to_text", keys, provider, key_prefix="tab_i2t")
    render_learning_panel("image_to_text", provider, gen_options.model, key_prefix="learn_i2t")

    st.subheader("Image → Text")
    st.caption("Vision: OpenAI, Gemini, Anthropic, Hugging Face, OpenRouter, Ollama.")
    uploaded_image = st.file_uploader(
        "Upload image",
        type=["png", "jpg", "jpeg", "webp", "gif"],
        key="image_upload",
    )
    image_question = st.text_input(
        "Question about the image (optional)",
        placeholder="What is happening in this image?",
        key="image_question",
    )
    vision_providers = ("openai", "google", "openrouter", "ollama", "anthropic", "huggingface")
    if st.button("Analyze image", key="btn_image_analyze", type="primary"):
        if uploaded_image is None:
            st.warning("Upload an image first.")
        elif provider not in vision_providers:
            st.warning(f"Use one of: {', '.join(vision_providers)}")
        else:
            with st.spinner("Analyzing..."):
                try:
                    data = uploaded_image.read()
                    result, model = analyze_image(
                        data, image_question, provider, keys, gen_options
                    )
                    st.success(f"Model: `{model}`")
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.image(Image.open(io.BytesIO(data)), width="stretch")
                    with col2:
                        st.markdown(result)
                except Exception as exc:
                    st.error(str(exc))

# --- Audio tab ---
with tab_audio:
    col_tts, col_stt = st.columns(2)

    with col_tts:
        render_modality_recommendations("text_to_audio", keys, provider, key_prefix="tab_t2a")
        render_learning_panel("text_to_audio", provider, gen_options.model, key_prefix="learn_t2a")
        st.subheader("Text → Audio")
        st.caption("OpenAI TTS.")
        tts_text = st.text_area(
            "Text to speak",
            placeholder="Hello! This is a multimodal AI demo.",
            height=100,
            key="tts_text",
        )
        if st.button("Generate speech", key="btn_tts"):
            if not keys.has_openai():
                st.warning("Set an OpenAI API key for speech synthesis.")
            elif not tts_text.strip():
                st.warning("Enter text to convert.")
            else:
                with st.spinner("Synthesizing..."):
                    try:
                        audio_bytes, model = generate_speech(
                            tts_text, "openai", keys, gen_options
                        )
                        st.success(f"Model: `{model}`")
                        st.audio(audio_bytes, format="audio/mp3")
                    except Exception as exc:
                        st.error(str(exc))

    with col_stt:
        render_modality_recommendations("audio_to_text", keys, provider, key_prefix="tab_a2t")
        render_learning_panel("audio_to_text", provider, gen_options.model, key_prefix="learn_a2t")
        st.subheader("Audio → Text")
        st.caption("Whisper (OpenAI) or Gemini.")
        audio_file = st.file_uploader(
            "Upload audio",
            type=["mp3", "wav", "m4a", "ogg", "webm"],
            key="audio_upload",
        )
        st.caption("Or record:")
        audio_recording = st.audio_input("Record audio", key="audio_record")
        if st.button("Transcribe", key="btn_transcribe", type="primary"):
            source = audio_file or audio_recording
            if source is None:
                st.warning("Upload or record audio first.")
            elif provider not in ("openai", "google", "huggingface"):
                st.warning("Use **openai**, **google**, or **huggingface** for transcription.")
            else:
                with st.spinner("Transcribing..."):
                    try:
                        if audio_file:
                            data = audio_file.read()
                            name = audio_file.name
                        else:
                            data = audio_recording.getvalue()
                            name = "recording.wav"
                        result, model = transcribe_audio(
                            data, name, provider, keys, gen_options
                        )
                        st.success(f"Model: `{model}`")
                        st.text_area("Transcript", result, height=200)
                    except Exception as exc:
                        st.error(str(exc))

# --- Video tab ---
with tab_video:
    col_v2t, col_t2v = st.columns(2)

    with col_v2t:
        render_modality_recommendations("video_to_text", keys, provider, key_prefix="tab_v2t")
        render_learning_panel("video_to_text", provider, gen_options.model, key_prefix="learn_v2t")
        st.subheader("Video → Text")
        st.caption("Frame sampling + vision (OpenAI, Gemini, Anthropic, HF, OpenRouter, Ollama).")
        video_file = st.file_uploader(
            "Upload video",
            type=["mp4", "mov", "avi", "webm", "mkv"],
            key="video_upload",
        )
        video_question = st.text_input(
            "Summary focus (optional)",
            placeholder="Describe the main actions and setting.",
            key="video_question",
        )
        video_providers = ("openai", "google", "openrouter", "ollama", "anthropic", "huggingface")
        if st.button("Summarize video", key="btn_video", type="primary"):
            if video_file is None:
                st.warning("Upload a video first.")
            elif provider not in video_providers:
                st.warning(f"Use one of: {', '.join(video_providers)}")
            else:
                with st.spinner("Processing video (this may take a minute)..."):
                    try:
                        data = video_file.read()
                        result, model = describe_video(
                            data, video_question, provider, keys, gen_options
                        )
                        st.success(f"Model: `{model}`")
                        st.markdown(result)
                    except Exception as exc:
                        st.error(str(exc))

    with col_t2v:
        render_modality_recommendations("text_to_video", keys, provider, key_prefix="tab_t2v")
        render_learning_panel("text_to_video", provider, gen_options.model, key_prefix="learn_t2v")
        st.subheader("Text → Video")
        st.caption("Information about video generation APIs.")
        video_prompt = st.text_input(
            "Video idea",
            placeholder="A timelapse of clouds over mountains at sunset.",
            key="video_gen_prompt",
        )
        if st.button("Check video options", key="btn_video_gen"):
            if not video_prompt.strip():
                st.warning("Enter a video description.")
            else:
                result, model = generate_video_placeholder(video_prompt)
                st.info(f"Status: `{model}`")
                st.markdown(result)
