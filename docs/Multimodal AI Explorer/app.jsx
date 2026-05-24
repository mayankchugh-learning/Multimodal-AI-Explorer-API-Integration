// app.jsx — root component: state, header, tab switching, learn drawer + tweaks
const { useState, useEffect, useMemo } = React;

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "accent": "#c47a2b",
  "density": "regular",
  "theme": "warm"
}/*EDITMODE-END*/;

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);

  // sidebar state
  const [byok, setByok] = useState({
    openai: "sk-prj-_______________K9b",
    anthropic: "sk-ant-_____________q7L",
    gemini: "AIzaSy_____________rJ4",
    groq: "",
    openrouter: "",
    hf: "hf_______________w2N",
    ollama: "http://localhost:11434/v1",
  });
  const [provider, setProvider] = useState("openai");
  const [temperature, setTemperature] = useState(0.70);
  const [maxTokens, setMaxTokens] = useState(1024);
  const [modelOverride, setModelOverride] = useState("");

  // main state
  const [tab, setTab] = useState("text");
  const [learnOpen, setLearnOpen] = useState(false);
  const [learnModality, setLearnModality] = useState("text_to_text");

  // applied recommendation per modality
  const [appliedModels, setAppliedModels] = useState({
    text_to_text: "gpt-4o-mini",
    text_to_image: "dall-e-3",
    image_to_text: "gpt-4o-mini",
    text_to_audio: "tts-1 · alloy",
    audio_to_text: "whisper-1",
    video_to_text: "gpt-4o-mini + OpenCV frames",
  });
  function applyModel(modalityId, rec) {
    setAppliedModels(m => ({ ...m, [modalityId]: rec.model }));
    if (rec.provider && byok[rec.provider]) setProvider(rec.provider);
  }

  function setByokKey(id, val) { setByok(b => ({ ...b, [id]: val })); }
  const configuredCount = Object.values(byok).filter(Boolean).length;

  // open Learn with the right modality based on current tab
  function openLearnFor(modalityId) { setLearnModality(modalityId); setLearnOpen(true); }
  function openLearnDefault() {
    const map = { text:"text_to_text", image:"image_to_text", audio:"audio_to_text", video:"video_to_text" };
    openLearnFor(map[tab]);
  }

  // keyboard shortcuts
  useEffect(() => {
    function onKey(e) {
      if (e.key === "Escape") setLearnOpen(false);
      if (e.key === "l" && !e.metaKey && !e.ctrlKey && document.activeElement.tagName !== "TEXTAREA" && document.activeElement.tagName !== "INPUT") {
        e.preventDefault(); openLearnDefault();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  // apply accent + density + theme to root
  const rootStyle = useMemo(() => ({
    "--accent": t.accent,
    "--accent-soft": `color-mix(in oklab, ${t.accent} 18%, #faf6ee)`,
    "--accent-ink": `color-mix(in oklab, ${t.accent} 60%, #1a1816)`,
  }), [t.accent]);

  const TAB_DEFS = [
    { id:"text",  label:"Text",  glyph:"T", modalities:["text_to_text", "text_to_image"] },
    { id:"image", label:"Image", glyph:"I", modalities:["image_to_text"] },
    { id:"audio", label:"Audio", glyph:"A", modalities:["text_to_audio", "audio_to_text"] },
    { id:"video", label:"Video", glyph:"V", modalities:["video_to_text"] },
  ];

  return (
    <div className="app" data-density={t.density} data-theme={t.theme} style={rootStyle}>
      <Sidebar
        byok={byok} setByokKey={setByokKey}
        provider={provider} setProvider={setProvider}
        temperature={temperature} setTemperature={setTemperature}
        maxTokens={maxTokens} setMaxTokens={setMaxTokens}
        modelOverride={modelOverride} setModelOverride={setModelOverride}
        configuredCount={configuredCount}
        onOpenLearn={openLearnDefault}
      />

      <main className="main">
        <header className="main-hd">
          <div>
            <div className="crumbs">
              <span>lab</span><span className="sep">/</span><span>{tab}</span>
              <span className="sep">/</span>
              <span style={{color:"var(--ink-2)"}}>provider: <b>{provider}</b></span>
            </div>
            <h1 className="main-title" style={{marginTop:8}}>Multimodal AI Explorer</h1>
            <p className="main-sub">
              Wire prompts to OpenAI, Anthropic, Gemini, Groq, OpenRouter, Hugging Face or Ollama —
              across text, image, audio, and video. Built as a learning lab: every tab has a Learn
              drawer with the underlying logic, a LangChain equivalent, and the system diagram.
            </p>
          </div>
          <div className="session">
            <div>session <b>#a73f</b></div>
            <div>•</div>
            <div>{configuredCount}/{window.PROVIDERS.length} providers</div>
            <div>•</div>
            <div>temp <b>{temperature.toFixed(2)}</b></div>
          </div>
        </header>

        <nav className="tabs" role="tablist">
          {TAB_DEFS.map(d => (
            <button
              key={d.id}
              className={classNames("tab", tab === d.id && "is-active")}
              onClick={() => setTab(d.id)}
              role="tab" aria-selected={tab === d.id}
            >
              <span className="tab-glyph">{d.glyph}</span>
              <span>{d.label}</span>
              <span className="tab-count">{d.modalities.length}</span>
            </button>
          ))}
          <span className="spacer" />
          <button className="kbtn kbtn-ghost kbtn-sm" style={{marginBottom:8}} onClick={openLearnDefault}>
            Learn <span className="kbd" style={{marginLeft:6}}>L</span>
          </button>
        </nav>

        <div className="canvas">
          {tab === "text"  && <TabText  provider={provider} temperature={temperature} appliedModels={appliedModels} applyModel={applyModel} />}
          {tab === "image" && <TabImage provider={provider} temperature={temperature} appliedModels={appliedModels} applyModel={applyModel} />}
          {tab === "audio" && <TabAudio provider={provider} temperature={temperature} appliedModels={appliedModels} applyModel={applyModel} />}
          {tab === "video" && <TabVideo provider={provider} temperature={temperature} appliedModels={appliedModels} applyModel={applyModel} />}
        </div>
      </main>

      {/* Learn drawer */}
      <button className="learn-tab" onClick={openLearnDefault} title="Open Learn drawer (L)">
        <span className="learn-tab-glyph">L</span>
        <span>Learn · logic · LangChain · arch</span>
      </button>
      <LearnDrawer open={learnOpen} onClose={() => setLearnOpen(false)} modalityId={learnModality} />

      {/* Tweaks */}
      <TweaksPanel title="Tweaks">
        <TweakSection label="Theme" />
        <TweakRadio label="Theme" value={t.theme}
          options={["warm", "ink"]}
          onChange={v => setTweak("theme", v)} />
        <TweakColor label="Accent" value={t.accent}
          options={["#c47a2b", "#2f6f5a", "#3a5fa8", "#7a4d9a"]}
          onChange={v => setTweak("accent", v)} />
        <TweakSection label="Layout" />
        <TweakRadio label="Density" value={t.density}
          options={["compact", "regular"]}
          onChange={v => setTweak("density", v)} />
      </TweaksPanel>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
