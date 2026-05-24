// data.jsx — providers, modalities, recommendations, mock outputs
// Shared data only. Components export to window at end.

const PROVIDERS = [
  { id: "openai",     name: "OpenAI",       env: "OPENAI_API_KEY",            prefix: "sk-" },
  { id: "anthropic",  name: "Anthropic",    env: "ANTHROPIC_API_KEY",         prefix: "sk-ant-" },
  { id: "gemini",     name: "Gemini",       env: "GOOGLE_API_KEY",            prefix: "AIza" },
  { id: "groq",       name: "Groq",         env: "GROQ_API_KEY",              prefix: "gsk_" },
  { id: "openrouter", name: "OpenRouter",   env: "OPENROUTER_API_KEY",        prefix: "sk-or-" },
  { id: "hf",         name: "Hugging Face", env: "HUGGINGFACEHUB_API_TOKEN",  prefix: "hf_" },
  { id: "ollama",     name: "Ollama",       env: "OLLAMA_BASE_URL",           prefix: "http://" },
];

const MODALITIES = {
  text_to_text: {
    id: "text_to_text",  glyph: "T→T", label: "Text → Text",
    recs: [
      { rating:"best",  model:"gpt-4o-mini",                provider:"openai",    note:"Fast, cheap, capable" },
      { rating:"best",  model:"claude-3-5-sonnet-20241022", provider:"anthropic", note:"Top reasoning" },
      { rating:"good",  model:"gemini-2.0-flash",           provider:"gemini",    note:"Multimodal native" },
      { rating:"good",  model:"llama-3.3-70b-versatile",    provider:"groq",      note:"Blazing fast inference" },
    ],
  },
  text_to_image: {
    id: "text_to_image", glyph: "T→I", label: "Text → Image",
    recs: [
      { rating:"best", model:"dall-e-3",                                provider:"openai", note:"Highest fidelity" },
      { rating:"good", model:"stabilityai/stable-diffusion-xl-base-1.0",provider:"hf",     note:"Open weights" },
    ],
  },
  image_to_text: {
    id: "image_to_text", glyph: "I→T", label: "Image → Text",
    recs: [
      { rating:"best", model:"gpt-4o-mini",                provider:"openai",    note:"Strong vision Q&A" },
      { rating:"best", model:"claude-3-5-sonnet-20241022", provider:"anthropic", note:"Detail capture" },
      { rating:"good", model:"gemini-2.0-flash",           provider:"gemini",    note:"Cheapest vision" },
    ],
  },
  text_to_audio: {
    id: "text_to_audio", glyph: "T→A", label: "Text → Audio",
    recs: [
      { rating:"best", model:"tts-1 · alloy", provider:"openai", note:"Only configured TTS" },
    ],
  },
  audio_to_text: {
    id: "audio_to_text", glyph: "A→T", label: "Audio → Text",
    recs: [
      { rating:"best", model:"whisper-1",          provider:"openai", note:"Reference transcription" },
      { rating:"good", model:"gemini-2.0-flash",   provider:"gemini", note:"Native audio in" },
      { rating:"good", model:"openai/whisper-large-v3", provider:"hf", note:"Self-host friendly" },
    ],
  },
  video_to_text: {
    id: "video_to_text", glyph: "V→T", label: "Video → Text",
    recs: [
      { rating:"best", model:"gpt-4o-mini + OpenCV frames", provider:"openai",    note:"8 keyframes → vision" },
      { rating:"good", model:"claude-3-5-sonnet",           provider:"anthropic", note:"Long-frame reasoning" },
    ],
  },
};

const MOCK_OUTPUTS = {
  text_to_text: `**Diffusion** is a generative process that learns to reverse a gradual noising of data. During training, the model sees pairs of (noisy_x, t) and predicts the noise that was added; at inference, it starts from pure noise and denoises step-by-step.

Three pieces matter:

1. **Forward process** — fixed Markov chain that adds Gaussian noise over T steps.
2. **Reverse model** — a U-Net (or transformer) that predicts the noise at each step.
3. **Sampler** — DDPM, DDIM, or DPM-Solver; trades steps for quality.

Vision models like SDXL pair this with a text encoder (CLIP) so the noise prediction is conditioned on your prompt.`,

  image_to_text: `The image shows a **macro photograph of a honeybee** on a sunflower head, captured at a shallow depth of field. Sharp focus sits on the bee's compound eye and the pollen-laden hind leg; the surrounding florets fall into a creamy bokeh.

Lighting is diffuse and slightly warm, consistent with late-afternoon sun. No human subjects, no text overlays. Suitable as a stock-style nature photograph.`,

  audio_to_text: `[00:00] Hey team, quick update on the multimodal evals.
[00:08] We landed on a sampling rate of one frame every two seconds, capped at eight frames per clip.
[00:17] Whisper one-large beats the small model on noisy phone audio by about four points on word error rate.
[00:28] Let's freeze the provider mix before Friday so the notebook ships clean.`,

  video_to_text: `The video is a **62-second product demo for a kitchen blender**. Across the eight sampled frames:

• Opens with a top-down shot of fresh fruit on a wooden counter
• Cuts to a close-up of the operator dropping berries into the jar
• The blender powers on — visible motion blur on the blades
• Final two frames show a glass being filled with a deep-purple smoothie

Inferred tone: warm, domestic. No on-screen text. Soundtrack appears upbeat from the implied motion pacing.`,

  text_to_image_caption: "DALL·E 3 · synthetic preview",
};

// helpers
function classNames(...a){ return a.filter(Boolean).join(" "); }
function abbrev(model){
  if (!model) return "";
  return model.length > 36 ? model.slice(0,33)+"…" : model;
}

Object.assign(window, { PROVIDERS, MODALITIES, MOCK_OUTPUTS, classNames, abbrev });
