// learn-drawer.jsx — Implementation logic, LangChain snippet, Architecture diagram
const { useState: _useStateL } = React;

const LEARN_CONTENT = {
  text_to_text: {
    title: "Text → Text · chat completion",
    sub: "How a prompt becomes a response when you click Generate.",
    steps: [
      ["Resolve provider", "Read sidebar selection, fall back to first available.", "config.merge_keys"],
      ["Build GenerationOptions", "Bundle temperature, max_tokens, model override.", "src/types.py"],
      ["Route by provider", "chat_completion() picks the SDK call.", "services/text.py"],
      ["Send + receive", "Single round trip · returns (text, model_name).", "openai.chat.completions"],
      ["Render", "Display text with metadata footer.", "app.py · tab"],
    ],
    code:
`from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a patient teacher."),
    ("human", "{question}"),
])
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

chain = prompt | llm | StrOutputParser()
answer = chain.invoke({"question": "Explain diffusion models."})`,
    diagram: [
      "┌──────────┐    ┌──────────────────┐    ┌─────────────┐",
      "│  prompt  │───▶│ chat_completion()│───▶│  provider   │",
      "└──────────┘    │  routes by id    │    │  SDK call   │",
      "                └────────┬─────────┘    └──────┬──────┘",
      "                         │                     │",
      "                         ▼                     ▼",
      "                  GenerationOptions      (text, model)",
    ],
  },
  text_to_image: {
    title: "Text → Image · generation",
    sub: "DALL-E 3 or HF SDXL · returns a URL or base64 PNG.",
    steps: [
      ["Validate prompt",     "Reject empty / too-long prompts client-side.", "app.py"],
      ["Pick size + quality", "Map UI selection to provider params.", "services/image.py"],
      ["Submit job",          "Single POST · synchronous for DALL-E 3.", "openai.images.generate"],
      ["Decode payload",      "Fetch URL → bytes, or decode b64.", "services/image.py"],
      ["Display + meta",      "Show with model badge + latency.", "app.py · tab"],
    ],
    code:
`from langchain_openai import DallEAPIWrapper

dalle = DallEAPIWrapper(model="dall-e-3", size="1024x1024")
url = dalle.run("a cozy reading nook with afternoon light")
# fetch url and display`,
    diagram: [
      "prompt ──▶ generate_image() ──▶ provider (DALL-E / SDXL)",
      "                                      │",
      "                                      ▼",
      "                                  url or b64",
      "                                      │",
      "                                      ▼",
      "                                 PIL.Image",
    ],
  },
  image_to_text: {
    title: "Image → Text · vision Q&A",
    sub: "Encode the image, ship it inline with an optional question.",
    steps: [
      ["Load + downsize",   "Pillow open() → max side 1568px.", "Image.thumbnail()"],
      ["Encode base64",     "Inline with mime prefix for chat APIs.", "b64encode"],
      ["Compose message",   "User turn = [image_url, text].", "services/image.py"],
      ["Call vision model", "GPT-4o / Claude / Gemini Flash.", "analyze_image()"],
      ["Return description","Display alongside thumbnail.", "app.py · tab"],
    ],
    code:
`from langchain_anthropic import ChatAnthropic
import base64

img_b64 = base64.b64encode(open("photo.jpg", "rb").read()).decode()
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

msg = llm.invoke([{
    "role": "user",
    "content": [
        {"type": "image", "source": {"type":"base64", "media_type":"image/jpeg", "data": img_b64}},
        {"type": "text", "text": "What's in this image?"},
    ],
}])`,
    diagram: [
      "image bytes ──▶ resize ──▶ b64 ──┐",
      "                                 ▼",
      "                question ──▶ vision LLM ──▶ description",
    ],
  },
  text_to_audio: {
    title: "Text → Audio · TTS",
    sub: "OpenAI tts-1 returns mp3 bytes directly.",
    steps: [
      ["Sanitize text", "Trim, cap length to provider limit.", "services/audio.py"],
      ["Pick voice",    "alloy / echo / fable / nova / onyx / shimmer.", "openai.audio.speech"],
      ["Stream mp3",    "Single call · bytes back.", "create()"],
      ["Save + play",   "BytesIO → Streamlit st.audio.", "app.py"],
    ],
    code:
`from openai import OpenAI
client = OpenAI()

resp = client.audio.speech.create(
    model="tts-1", voice="alloy",
    input="Welcome to the multimodal lab.",
)
with open("out.mp3", "wb") as f:
    f.write(resp.content)`,
    diagram: [
      "text ──▶ tts-1 (voice) ──▶ mp3 bytes ──▶ player",
    ],
  },
  audio_to_text: {
    title: "Audio → Text · transcription",
    sub: "Whisper-1 or Gemini Flash. Optional timestamps.",
    steps: [
      ["Read bytes",      "Streamlit file_uploader → bytes.", "app.py"],
      ["Choose provider", "OpenAI / Google / HF whisper-large.", "transcribe_audio()"],
      ["Submit clip",     "Multipart form upload to API.", "openai.audio.transcriptions"],
      ["Parse segments",  "Optional timestamp granularity.", "response.segments"],
      ["Render markdown", "Per-segment lines with [mm:ss].", "app.py · tab"],
    ],
    code:
`from openai import OpenAI
client = OpenAI()

with open("clip.m4a", "rb") as f:
    out = client.audio.transcriptions.create(
        model="whisper-1", file=f,
        response_format="verbose_json",
        timestamp_granularities=["segment"],
    )
for seg in out.segments:
    print(f"[{seg.start:.1f}] {seg.text}")`,
    diagram: [
      "audio bytes ──▶ whisper-1 ──▶ segments ──▶ formatted text",
    ],
  },
  video_to_text: {
    title: "Video → Text · frame sampling",
    sub: "OpenCV extracts N keyframes, ships them as a single vision call.",
    steps: [
      ["Open video",   "cv2.VideoCapture · read fps + duration.", "opencv-python-headless"],
      ["Sample N",     "Every duration/N seconds · skip first 0.1 s.", "frame_pos = i * step"],
      ["Encode JPEG",  "Per-frame imencode → base64 chunks.", "cv2.imencode('.jpg')"],
      ["Multi-image",  "Compose single user turn with all frames + prompt.", "services/video.py"],
      ["Summarize",    "Vision model treats them as a storyboard.", "describe_video()"],
    ],
    code:
`import cv2, base64
from langchain_openai import ChatOpenAI

cap = cv2.VideoCapture("clip.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
step = max(1, total // 8)

frames = []
for i in range(8):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
    ok, frame = cap.read()
    if not ok: break
    _, buf = cv2.imencode(".jpg", frame)
    frames.append(base64.b64encode(buf).decode())

llm = ChatOpenAI(model="gpt-4o-mini")
# pass frames as a multi-image content list`,
    diagram: [
      "video ──▶ OpenCV ──▶ [f1, f2, … f8] ──┐",
      "                                      ▼",
      "                         vision LLM (storyboard) ──▶ summary",
    ],
  },
};

function LearnDrawer({ open, onClose, modalityId }) {
  const [tab, setTab] = _useStateL("logic");
  if (!open) return null;
  const content = LEARN_CONTENT[modalityId] || LEARN_CONTENT.text_to_text;

  return (
    <>
      <div className="learn-overlay" onClick={onClose} />
      <aside className="learn-panel" role="dialog" aria-label="Learn panel">
        <header className="learn-hd">
          <div>
            <h2>{content.title}</h2>
            <p>{content.sub}</p>
          </div>
          <button className="kbtn kbtn-ghost kbtn-sm" onClick={onClose}>Close <span className="kbd" style={{marginLeft:6}}>Esc</span></button>
        </header>
        <div className="learn-tabs">
          <button className={classNames("learn-tab-btn", tab === "logic" && "is-active")} onClick={() => setTab("logic")}>Implementation logic</button>
          <button className={classNames("learn-tab-btn", tab === "lc"    && "is-active")} onClick={() => setTab("lc")}>LangChain code</button>
          <button className={classNames("learn-tab-btn", tab === "arch"  && "is-active")} onClick={() => setTab("arch")}>Architecture</button>
        </div>
        <div className="learn-body">
          {tab === "logic" && (
            <div>
              {content.steps.map(([h, b, code], i) => (
                <div className="step" key={i}>
                  <div className="step-n">{i + 1}</div>
                  <div>
                    <h4 className="step-h">{h}</h4>
                    <p className="step-b">{b} {code && <span className="step-code">{code}</span>}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
          {tab === "lc" && (
            <>
              <div className="codeblock-hd">
                <span>{modalityId.replace(/_/g, " ")} · python</span>
                <button className="kbtn kbtn-ghost kbtn-sm">Download .py</button>
              </div>
              <pre className="codeblock" style={{margin:0}}><code dangerouslySetInnerHTML={{__html: highlightPy(content.code)}} /></pre>
              <div className="muted" style={{marginTop:10, fontSize:12, lineHeight:1.55}}>
                The same call shape works whether you swap <span className="kbd">ChatOpenAI</span> for
                <span className="kbd"> ChatAnthropic</span>, <span className="kbd">ChatGroq</span>,
                <span className="kbd"> ChatGoogleGenerativeAI</span>, or <span className="kbd">ChatOllama</span>.
              </div>
            </>
          )}
          {tab === "arch" && (
            <>
              <pre className="diagram" style={{margin:0}}>{content.diagram.join("\n")}</pre>
              <div className="muted" style={{marginTop:14, fontSize:12.5, lineHeight:1.6}}>
                Full system diagram: UI → Education → Services → Config layers. Each modality is a
                pure function returning <span className="kbd">(result, model_name)</span>, which keeps
                the Streamlit layer thin and the tests easy.
              </div>
              <div style={{marginTop:14}}>
                <div className="codeblock-hd"><span>system · ascii</span><button className="kbtn kbtn-ghost kbtn-sm">View Mermaid</button></div>
                <pre className="diagram" style={{margin:0}}>{
`┌─────────────────────────────────────────────────────┐
│  UI Layer (app.py)                                  │
│  Tabs · Sidebar · BYOK · Recommendations · Learn    │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│  Education Layer (src/education/)                   │
│  Steps · LangChain snippets · Mermaid diagrams      │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│  Services Layer (src/services/)                     │
│  text · image · audio · video · errors              │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│  Config + Catalog                                   │
│  config.py · types.py · modality_catalog.py         │
└─────────────────────────────────────────────────────┘`}</pre>
              </div>
            </>
          )}
        </div>
      </aside>
    </>
  );
}

// minimal python highlighter for the codeblock
function highlightPy(src) {
  // escape
  let s = src.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  // comments
  s = s.replace(/(^|\n)(\s*#[^\n]*)/g, (_, p, c) => `${p}<span class="c-cm">${c}</span>`);
  // strings
  s = s.replace(/(&quot;[^&]*?&quot;|"[^"]*"|'[^']*')/g, '<span class="c-st">$1</span>');
  // keywords
  s = s.replace(/\b(from|import|def|class|return|with|as|for|in|if|not|and|or|None|True|False|lambda)\b/g, '<span class="c-kw">$1</span>');
  // functions called (word followed by ()
  s = s.replace(/\b([A-Za-z_][A-Za-z0-9_]*)(?=\()/g, '<span class="c-fn">$1</span>');
  // punctuation hint
  return s;
}

Object.assign(window, { LearnDrawer, LEARN_CONTENT });
