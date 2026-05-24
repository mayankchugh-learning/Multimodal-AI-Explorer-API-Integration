# Multimodal AI Model Exploration & Web Application

Assignment project: explore AI models across **text, image, audio, and video** modalities in a Jupyter notebook, then use them in a **Streamlit** web app.

## Teaching features (students)

Each tab and the sidebar include **Learn: Logic, LangChain & Architecture**:

- **Implementation logic** — step-by-step pipeline matching this codebase
- **LangChain code** — copy-ready snippet for the selected provider + modality (download as `.py`)
- **Architecture** — Mermaid diagrams (modality flow, full app, LCEL)

Optional install for running snippets:

```bash
pip install -r requirements-langchain.txt
```

See also [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Project structure

```
├── app.py                          # Streamlit web application (Task 2)
├── docs/ARCHITECTURE.md            # Teaching architecture guide
├── requirements-langchain.txt    # Optional LangChain deps for students
├── src/education/                 # Logic, LangChain snippets, diagrams
├── notebooks/
│   └── multimodal_exploration.ipynb  # Model exploration (Task 1)
├── src/
│   ├── config.py                   # API keys from .env
│   └── services/                   # Modality handlers
│       ├── text.py
│       ├── image.py
│       ├── audio.py
│       └── video.py
├── requirements.txt
├── .env.example
└── README.md
```

## Models used

| Modality | Direction | Model | Provider |
|----------|-----------|-------|----------|
| Text | Text → Text | `gpt-4o-mini` | OpenAI |
| Text | Text → Text | `gemini-2.0-flash` | Google Gemini |
| Text | Text → Text | `llama-3.3-70b-versatile` | Groq |
| Text | Text → Text | `openai/gpt-4o-mini` (configurable) | OpenRouter |
| Text | Text → Text | `claude-3-5-sonnet-20241022` | Anthropic |
| Text | Text → Text | `meta-llama/Meta-Llama-3-8B-Instruct` | Hugging Face |
| Text | Text → Text | `llama3.1:8b` (configurable) | Ollama (local) |
| Image | Text → Image | `stabilityai/stable-diffusion-xl-base-1.0` | Hugging Face |
| Image | Image → Text | `claude-3-5-sonnet-20241022` | Anthropic |
| Image | Image → Text | `Salesforce/blip-image-captioning-large` | Hugging Face |
| Audio | Audio → Text | `openai/whisper-large-v3` | Hugging Face |
| Image | Text → Image | `dall-e-3` | OpenAI |
| Image | Image → Text | `gpt-4o-mini` | OpenAI (vision) |
| Image | Image → Text | `gemini-2.0-flash` | Google (vision) |
| Audio | Text → Audio | `tts-1` (voice: alloy) | OpenAI |
| Audio | Audio → Text | `whisper-1` | OpenAI |
| Audio | Audio → Text | `gemini-2.0-flash` | Google |
| Video | Video → Text | Frame sampling + vision models | OpenAI / Google |
| Video | Text → Video | Placeholder (see below) | — |

### Modality explanations

- **Text → Text:** Standard chat completion; compares fast Groq Llama, Gemini Flash, and OpenAI mini.
- **Text → Image:** DALL-E 3 generates images from natural-language prompts.
- **Image → Text:** Vision models describe or answer questions about uploaded images.
- **Text → Audio:** OpenAI TTS converts text to spoken MP3 audio.
- **Audio → Text:** Whisper (or Gemini) transcribes uploaded or recorded audio.
- **Video → Text:** OpenCV extracts key frames; vision models produce a summary (full native video APIs can be swapped in later).
- **Text → Video:** Production APIs (Runway, Luma, Sora) need separate billing; the app documents options.

## Setup

1. **Python 3.10+** recommended.

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   pip install -r requirements.txt
   ```

3. Copy environment template and add keys (at least one provider):

   ```bash
   copy .env.example .env
   ```

   ### API keys → typical `.env` names

   | Provider | Get key at | Env variable |
   |----------|------------|--------------|
   | OpenAI | https://platform.openai.com/api-keys | `OPENAI_API_KEY` |
   | Anthropic | https://platform.claude.com/docs/en/api/admin/api_keys/retrieve | `ANTHROPIC_API_KEY` |
   | Groq | https://console.groq.com/ | `GROQ_API_KEY` |
   | OpenRouter | https://openrouter.ai/workspaces/default/keys | `OPENROUTER_API_KEY` |
   | Hugging Face | https://huggingface.co/settings/tokens | `HUGGINGFACEHUB_API_TOKEN` |
   | Gemini | https://ai.google.dev/gemini-api/docs/api-key | `GOOGLE_API_KEY` |
   | Ollama (local) | https://ollama.com/ | `OLLAMA_BASE_URL` |
   | LangSmith | https://smith.langchain.com/settings | `LANGCHAIN_API_KEY` (optional; tracing) |

   Hugging Face aliases: `HUGGINGFACE_API_KEY`, `HF_TOKEN`. Gemini alias: `GEMINI_API_KEY`.

   **BYOK:** In the app sidebar, expand **Bring Your Own Key** to paste keys for this session only (not saved to disk). Expand **API keys → `.env` variable names** for the same table with clickable links.

   **Generation controls:** Adjust **Temperature**, **Max tokens**, and optional **Model override** in the sidebar.

   **Model recommendations:** Each tab shows ⭐ **Best** providers/models for that modality. Expand **All providers & models** for the full list, or use **Apply** buttons to switch provider + model instantly. The sidebar **Task guide** browses every modality.

## Run Task 1 — Notebook

```bash
jupyter notebook notebooks/multimodal_exploration.ipynb
```

Run all cells top to bottom. For **Video → Text**, add a short clip at `notebooks/sample.mp4`.

## Run Task 2 — Streamlit app

From the project root:

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

### Port conflict (wrong app / PostgreSQL error)

If you see **"RAG Chat"** or a `psycopg2` PostgreSQL error, another Streamlit app is using port 8501 (often from a class RAG project). Either stop that server, or run this app on a different port:

```bash
streamlit run app.py --server.port 8502
```

Then open **http://localhost:8502**. You should see **"Multimodal AI Explorer"** with tabs: Text, Image, Audio, Video.

### Web app features

| Input | Output | Tab |
|-------|--------|-----|
| Text prompt | Text response | Text |
| Text prompt | Generated image | Text |
| Image upload | Description / Q&A | Image |
| Text | Spoken audio | Audio |
| Audio upload / mic | Transcript | Audio |
| Video upload | Summary | Video |
| Text | Video API guidance | Video |

## Screenshots / demo

After running the app, capture screenshots of each tab or record a short screen demo for submission.

Suggested filenames:

- `docs/screenshot-text.png`
- `docs/screenshot-image.png`
- `docs/screenshot-audio.png`
- `docs/screenshot-video.png`

## Submission checklist

- [x] Jupyter notebook (`notebooks/multimodal_exploration.ipynb`)
- [x] Web application (`app.py` + `src/`)
- [x] README (this file)
- [ ] Screenshots or demo video (you add after running)
- [x] List of models (table above)
- [x] Modality explanations (above)

## Notes

- **Costs:** API calls may incur charges on OpenAI/Google/Groq accounts.
- **Text → Video:** Integrate Runway, Replicate, or similar when you have API access; the placeholder explains this for graders.
- **Security:** Never commit `.env` or real API keys to git.

## License

Educational use — course assignment.
