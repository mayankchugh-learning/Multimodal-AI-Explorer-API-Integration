# Multimodal AI Explorer — Full Development Prompt

Use this document as a **copy-paste master prompt** for vibe coding (Cursor, Claude Code, ChatGPT, etc.) or for **Claude design** (UI mockups, architecture diagrams, component specs).

---

## Role & Goal

You are an expert Python developer and UI designer. Build a **Multimodal AI Model Exploration & Web Application** — an educational assignment project with two deliverables:

1. **Task 1:** A Jupyter notebook that explores AI models across text, image, audio, and video modalities.
2. **Task 2:** A **Streamlit** web app that wraps the same capabilities in a polished, student-friendly UI with teaching features.

The app title is **"Multimodal AI Explorer"**. Tagline: *OpenAI · Gemini · Groq · OpenRouter · Anthropic · Hugging Face · Ollama*.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Web UI | Streamlit 1.32+ (wide layout, expanded sidebar) |
| Notebook | Jupyter |
| Language | Python 3.10+ |
| Config | `python-dotenv`, `.env` file |
| HTTP | `httpx`, official provider SDKs |
| Image | `Pillow` |
| Video frames | `opencv-python-headless` |
| Optional teaching | LangChain snippets (separate `requirements-langchain.txt`) |

**Core dependencies:**

```
streamlit>=1.32.0
openai>=1.40.0
google-genai>=1.0.0
groq>=0.9.0
anthropic>=0.40.0
huggingface-hub>=0.26.0
python-dotenv>=1.0.0
httpx>=0.27.0
Pillow>=10.0.0
opencv-python-headless>=4.9.0
```

---

## Project Structure

Create this folder layout:

```
├── app.py                          # Streamlit web application (main entry)
├── docs/
│   ├── ARCHITECTURE.md             # Teaching architecture guide
│   └── DEVELOPMENT_PROMPT.md       # This file
├── requirements.txt
├── requirements-langchain.txt      # Optional LangChain deps
├── requirements-notebook.txt       # Notebook-only deps
├── .env.example
├── README.md
├── notebooks/
│   └── multimodal_exploration.ipynb
└── src/
    ├── config.py                   # API keys from .env + BYOK merge
    ├── providers.py                # Default model per provider
    ├── types.py                    # GenerationOptions dataclass
    ├── modality_catalog.py         # Best-model recommendations per task
    ├── api_key_reference.py        # Provider signup links + env var names
    ├── ui_api_keys.py              # Sidebar API key reference tables
    ├── ui_education.py             # "Learn" panel renderer
    ├── ui_recommendations.py       # Model recommendations + sidebar picker
    ├── education/
    │   ├── implementation_logic.py # Step-by-step pipeline explanations
    │   ├── langchain_examples.py   # Copy-ready LangChain snippets
    │   ├── architecture.py         # Mermaid + ASCII diagrams
    │   └── diagram_render.py       # Render Mermaid in Streamlit
    └── services/
        ├── __init__.py
        ├── text.py                 # chat_completion()
        ├── image.py                # generate_image(), analyze_image()
        ├── audio.py                # generate_speech(), transcribe_audio()
        ├── video.py                # describe_video(), generate_video_placeholder()
        ├── anthropic.py            # Anthropic API helpers
        ├── gemini.py               # Google Gemini helpers
        ├── huggingface.py          # HF Inference API helpers
        ├── connectivity.py         # test_groq() connection check
        └── errors.py               # Friendly error formatting
```

---

## Architecture (Layered Design)

```
┌─────────────────────────────────────────────────────────┐
│  UI Layer (app.py)                                      │
│  Streamlit tabs, sidebar, BYOK, recommendations, Learn  │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  Education Layer (src/education/)                       │
│  Logic steps, LangChain snippets, Mermaid diagrams      │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  Services Layer (src/services/)                       │
│  Provider adapters per modality                         │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  Config + Catalog (src/config.py, modality_catalog.py)  │
│  API keys, GenerationOptions, model recommendations     │
└─────────────────────────────────────────────────────────┘
```

**Request flow (example: Text → Text):**

1. User enters prompt in Streamlit tab
2. Sidebar provides `GenerationOptions` (temperature, max_tokens, model override)
3. `chat_completion()` in `src/services/text.py` routes by selected provider
4. Provider SDK returns text → displayed in UI with model name

See also [`ARCHITECTURE.md`](ARCHITECTURE.md) for LangChain mappings and student exercises.

---

## Supported Modalities & Models

| Modality | Direction | Best Models | Provider |
|----------|-----------|-------------|----------|
| Text | Text → Text | `gpt-4o-mini`, `gemini-2.0-flash`, `llama-3.3-70b-versatile`, `claude-3-5-sonnet-20241022`, `meta-llama/Meta-Llama-3-8B-Instruct`, `llama3.1:8b` | OpenAI, Gemini, Groq, OpenRouter, Anthropic, HF, Ollama |
| Image | Text → Image | `dall-e-3`, `stabilityai/stable-diffusion-xl-base-1.0` | OpenAI, Hugging Face |
| Image | Image → Text | `gpt-4o-mini`, `gemini-2.0-flash`, `claude-3-5-sonnet-20241022`, `Salesforce/blip-image-captioning-large` | OpenAI, Google, Anthropic, HF, OpenRouter, Ollama |
| Audio | Text → Audio | `tts-1` (voice: alloy) | OpenAI |
| Audio | Audio → Text | `whisper-1`, `gemini-2.0-flash`, `openai/whisper-large-v3` | OpenAI, Google, HF |
| Video | Video → Text | Frame sampling + vision models above | OpenAI, Google, Anthropic, HF, OpenRouter, Ollama |
| Video | Text → Video | Placeholder / API guidance (Runway, Sora, Veo) | Informational only |

---

## Environment Variables

Create `.env.example`:

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GROQ_API_KEY=gsk_...
OPENROUTER_API_KEY=sk-or-...
HUGGINGFACEHUB_API_TOKEN=hf_...
GOOGLE_API_KEY=...
OLLAMA_BASE_URL=http://localhost:11434/v1
```

Support aliases: `GEMINI_API_KEY`, `HF_TOKEN`, `HUGGINGFACE_API_KEY`.

---

## UI/UX Design Spec (for Claude Design)

### Page Layout

- **Layout:** Wide (`layout="wide"`)
- **Page icon:** 🧠
- **Header:** Large bold title "Multimodal AI Explorer"
- **Subheader:** Gray muted provider list
- **Sidebar:** Always expanded — settings, keys, generation controls, learning panel

### Color & Typography

- Primary header: 2rem, font-weight 700
- Subheader: `#6b7280` (gray-500)
- Use Streamlit native components; minimal custom CSS only for headers
- Success states: green checkmarks ✅ / ❌ for provider status

### Main Tabs (horizontal)

| Tab | Icon | Content |
|-----|------|---------|
| Text | 📝 | Text→Text chat + Text→Image generation |
| Image | 🖼️ | Image upload + vision Q&A |
| Audio | 🎵 | Two columns: Text→Audio (TTS) \| Audio→Text (STT) |
| Video | 🎬 | Two columns: Video→Text summary \| Text→Video guidance |

### Sidebar Sections (top to bottom)

1. **🔑 Bring Your Own Key (BYOK)** — collapsible expander with password inputs for each provider; keys stay in session only, never saved to disk
2. **📋 API keys → `.env` variable names** — table with signup links
3. **Provider status** — ✅/❌ checklist for each provider
4. **Provider selectbox** — dropdown of available providers
5. **Test Groq connection** button (when Groq selected)
6. **Task guide** — modality picker with Apply buttons to switch provider+model
7. **Generation controls** — Temperature slider (0–2), Max tokens (64–8192), Model override text input
8. **Learn panel** — Implementation logic, LangChain snippet (downloadable `.py`), Architecture diagrams

### Per-Tab UI Pattern

Each modality section includes:

1. **⭐ Model recommendations** expander — "Best" options with one-click Apply
2. **Learn: Logic, LangChain & Architecture** expander
3. **Input widgets** (text area, file uploader, audio recorder)
4. **Primary action button** with spinner during API call
5. **Output area** — markdown text, image display, audio player, or transcript

### UX Behaviors

- Show model name + temperature on success: `Model: gpt-4o-mini · temp=0.7`
- Friendly warnings when keys missing or wrong provider selected
- Groq 403 errors suggest VPN/hotspot/OpenRouter fallback
- Video processing shows "this may take a minute" spinner
- Image analysis: side-by-side columns (image | description)

---

## Feature Requirements (Detailed)

### 1. Config & Key Management (`src/config.py`)

- `ProviderKeys` dataclass with `has_*()` methods and `available_providers()`
- `get_keys()` loads from `.env`
- `merge_keys(env, overrides)` — BYOK session values override `.env` when non-empty

### 2. Generation Options (`src/types.py`)

```python
@dataclass
class GenerationOptions:
    temperature: float = 0.7
    max_tokens: int = 1024
    model: str | None = None

    def resolved_model(self, default: str) -> str:
        return self.model or default
```

### 3. Service Layer Functions

Each returns `(result, model_name)` tuple:

| Function | File | Description |
|----------|------|-------------|
| `chat_completion(prompt, provider, keys, options)` | text.py | Route to OpenAI/Gemini/Groq/OpenRouter/Anthropic/HF/Ollama |
| `generate_image(prompt, provider, keys, options)` | image.py | DALL-E 3 or HF SDXL |
| `analyze_image(bytes, question, provider, keys, options)` | image.py | Vision models with optional Q&A |
| `generate_speech(text, provider, keys, options)` | audio.py | OpenAI TTS → MP3 bytes |
| `transcribe_audio(bytes, filename, provider, keys, options)` | audio.py | Whisper or Gemini |
| `describe_video(bytes, question, provider, keys, options)` | video.py | OpenCV frame extraction → vision model |
| `generate_video_placeholder(prompt)` | video.py | Return info about Runway/Sora/Veo APIs |

### 4. Modality Catalog (`src/modality_catalog.py`)

- Define all 7 modalities: `text_to_text`, `text_to_image`, `image_to_text`, `text_to_audio`, `audio_to_text`, `video_to_text`, `text_to_video`
- Each has `ModelRecommendation` entries with ratings: `best`, `good`, `supported`, `unsupported`
- `best_for_modality(id, keys)` returns first best option with configured credentials

### 5. Education / Teaching Features

Each tab and sidebar includes **"Learn: Logic, LangChain & Architecture"** with three sub-tabs:

**A. Implementation Logic** — numbered steps matching the actual codebase pipeline

**B. LangChain Code** — copy-ready snippet for the selected provider + modality:

| App calls | LangChain equivalent |
|-----------|---------------------|
| `openai.chat.completions` | `ChatOpenAI` + LCEL `\|` chain |
| `anthropic.messages.create` | `ChatAnthropic` |
| `google.genai` | `ChatGoogleGenerativeAI` |
| `groq.chat.completions` | `ChatGroq` |
| HF InferenceClient | `ChatHuggingFace` |
| Ollama URL | `ChatOllama` |

Include a **Download as `.py`** button for the snippet.

**C. Architecture** — render Mermaid diagrams in-browser + ASCII fallback for slides

### 6. Video Processing Logic

- Use OpenCV to extract key frames (e.g., every N seconds or max 8 frames)
- Encode frames as base64
- Send as multi-image message to vision model
- Prompt: "Summarize this video based on these frames" + optional user focus question

### 7. Text → Video Placeholder

Do NOT integrate paid video APIs. Instead return markdown explaining:

- OpenAI Sora (preview access)
- Google Veo (Vertex AI)
- Runway, Luma, Replicate options
- Why production video gen needs separate billing

---

## Jupyter Notebook (Task 1)

Create `notebooks/multimodal_exploration.ipynb` with cells for:

1. Setup & API key loading
2. Text → Text demos (at least 2 providers)
3. Text → Image (DALL-E or HF)
4. Image → Text (vision model)
5. Text → Audio (TTS)
6. Audio → Text (Whisper)
7. Video → Text (frame extraction + vision) — note: add `sample.mp4` for testing
8. Summary table of models tested

---

## Implementation Phases (Build Order)

### Phase 1 — Foundation

- [ ] Project scaffold, `requirements.txt`, `.env.example`, `README.md`
- [ ] `src/config.py`, `src/types.py`, `src/providers.py`

### Phase 2 — Services

- [ ] `text.py` — all 7 providers for chat
- [ ] `image.py` — generation + vision
- [ ] `audio.py` — TTS + STT
- [ ] `video.py` — frame extraction + placeholder

### Phase 3 — Catalog & UI helpers

- [ ] `modality_catalog.py` with all recommendations
- [ ] `ui_recommendations.py`, `ui_api_keys.py`

### Phase 4 — Education layer

- [ ] `implementation_logic.py`, `langchain_examples.py`, `architecture.py`
- [ ] `ui_education.py` with Mermaid rendering

### Phase 5 — Main app

- [ ] `app.py` — sidebar + 4 tabs wired to services
- [ ] BYOK, generation controls, error handling

### Phase 6 — Notebook & docs

- [ ] `multimodal_exploration.ipynb`
- [ ] `docs/ARCHITECTURE.md`, full `README.md`

---

## Acceptance Criteria

- [ ] `streamlit run app.py` opens **Multimodal AI Explorer** (not another app)
- [ ] Works with at least one configured API key
- [ ] All 4 tabs functional with appropriate provider gating
- [ ] Sidebar shows provider status, temperature, max tokens, model override
- [ ] BYOK keys override `.env` for current session only
- [ ] Each modality shows ⭐ Best recommendations with Apply buttons
- [ ] Learn panels show logic, LangChain code, and architecture diagrams
- [ ] Video tab extracts frames and summarizes via vision model
- [ ] Text→Video shows informational placeholder (not broken API call)
- [ ] Notebook runs end-to-end with documented models
- [ ] README includes model table, setup instructions, submission checklist
- [ ] No API keys committed to git

---

## Security & Best Practices

- Never commit `.env` or real keys
- Use `type="password"` for BYOK inputs
- Validate provider availability before API calls
- Wrap API calls in try/except with user-friendly error messages
- Support markdown errors (for formatted provider error messages)

---

## Run Commands

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # fill in keys

# Task 1
jupyter notebook notebooks/multimodal_exploration.ipynb

# Task 2
streamlit run app.py
# If port 8501 busy:
streamlit run app.py --server.port 8502
```

---

## Optional Enhancements (if time permits)

- LangSmith tracing via `LANGCHAIN_API_KEY`
- Conversation history / multi-turn chat
- Export results as JSON or PDF
- Dark mode toggle
- Rate limiting / cost estimate display

---

## How to Use This Prompt

| Tool | How |
|------|-----|
| **Cursor / vibe coding** | Paste the full prompt and say: *"Build this phase by phase. Start with Phase 1."* |
| **Claude (design)** | Paste the **UI/UX Design Spec** section and ask for wireframes, component mockups, or a Figma-style layout |
| **Claude (architecture)** | Paste the **Architecture** section and ask for Mermaid diagrams, sequence diagrams, or a system design doc |
| **Incremental build** | Use one phase at a time: *"Implement Phase 2 — Services layer only"* |

### Quick-start prompts

**Full rebuild:**

```
Read docs/DEVELOPMENT_PROMPT.md and build the Multimodal AI Explorer app phase by phase.
Start with Phase 1. Match the existing project structure and conventions.
```

**Design only:**

```
Using the UI/UX Design Spec in docs/DEVELOPMENT_PROMPT.md, create wireframes and a
component layout for the Multimodal AI Explorer Streamlit app (sidebar + 4 tabs).
```

**Services only:**

```
Using docs/DEVELOPMENT_PROMPT.md Phase 2, implement src/services/ with all provider
adapters for text, image, audio, and video modalities.
```
