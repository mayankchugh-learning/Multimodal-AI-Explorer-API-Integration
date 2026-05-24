// tab-text.jsx — Text → Text chat and Text → Image generation
const { useState: _useStateT } = React;

function TabText({ provider, temperature, appliedModels, applyModel }) {
  const [prompt, setPrompt] = _useStateT("Explain how diffusion models generate images, in plain English.");
  const [imgPrompt, setImgPrompt] = _useStateT("a cozy reading nook with afternoon light, watercolor illustration");
  const chat = useFakeRun();
  const img  = useFakeRun();

  const modelTT = appliedModels.text_to_text  || "gpt-4o-mini";
  const modelTI = appliedModels.text_to_image || "dall-e-3";

  return (
    <div className="split">
      {/* Text → Text */}
      <section className="card">
        <Recommendations modalityId="text_to_text" appliedModel={modelTT} onApply={r => applyModel("text_to_text", r)} />
        <div className="card-hd">
          <div className="card-hd-l">
            <span className="card-tag">T → T</span>
            <h3 className="card-title">Chat completion</h3>
          </div>
          <button className="kbtn kbtn-ghost kbtn-sm">Multi-turn</button>
        </div>
        <div className="card-bd">
          <textarea
            className="textarea"
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
            placeholder="What do you want to ask?"
          />

          <div style={{display:"flex", gap:8, alignItems:"center"}}>
            <button
              className="kbtn kbtn-accent"
              onClick={() => chat.run(1100)}
              disabled={chat.running}
            >
              {chat.running ? "Generating…" : "Generate"}
            </button>
            <button className="kbtn kbtn-ghost kbtn-sm" onClick={() => setPrompt("")}>Clear</button>
            <span className="spacer" />
            <span className="muted" style={{fontSize:11, fontFamily:"var(--mono)"}}>
              {prompt.length} chars · ~{Math.max(1, Math.round(prompt.split(/\s+/).length * 1.3))} tokens
            </span>
          </div>

          {chat.running && <RunningStrip label={`asking ${modelTT}`} />}

          {chat.hasRun && (
            <>
              <FormattedOutput text={window.MOCK_OUTPUTS.text_to_text} />
              <OutputMeta model={modelTT} temperature={temperature} latencyMs={chat.latency} />
            </>
          )}
        </div>
        <div className="card-ft">
          <span>provider · <b style={{color:"var(--ink)"}}>{provider}</b></span>
          <span>POST /v1/chat/completions</span>
        </div>
      </section>

      {/* Text → Image */}
      <section className="card">
        <Recommendations modalityId="text_to_image" appliedModel={modelTI} onApply={r => applyModel("text_to_image", r)} />
        <div className="card-hd">
          <div className="card-hd-l">
            <span className="card-tag">T → I</span>
            <h3 className="card-title">Image generation</h3>
          </div>
          <select className="ctrl-input" style={{width:120, padding:"5px 24px 5px 8px", fontSize:11.5}}>
            <option>1024 × 1024</option>
            <option>1024 × 1792</option>
            <option>1792 × 1024</option>
          </select>
        </div>
        <div className="card-bd">
          <textarea
            className="textarea"
            style={{minHeight:72}}
            value={imgPrompt}
            onChange={e => setImgPrompt(e.target.value)}
            placeholder="Describe the image you want…"
          />
          <div style={{display:"flex", gap:8, alignItems:"center"}}>
            <button className="kbtn kbtn-accent" onClick={() => img.run(1600)} disabled={img.running}>
              {img.running ? "Rendering…" : "Generate image"}
            </button>
            <button className="kbtn kbtn-ghost kbtn-sm">Style: photo</button>
            <span className="spacer" />
            <span className="muted" style={{fontSize:11, fontFamily:"var(--mono)"}}>
              1 image · standard
            </span>
          </div>

          {img.running && <RunningStrip label={`rendering ${modelTI}`} />}

          {!img.hasRun && !img.running && (
            <div className="dropzone" style={{minHeight:180, padding:18}}>
              <div className="dropzone-glyph">▭</div>
              <strong>Output preview</strong>
              <span>The generated image will appear here.</span>
            </div>
          )}

          {img.hasRun && (
            <>
              <div className="img-stage">
                <div className="img-shape" />
                <span className="img-cap">{window.MOCK_OUTPUTS.text_to_image_caption}</span>
              </div>
              <OutputMeta model={modelTI} temperature={temperature} latencyMs={img.latency} />
            </>
          )}
        </div>
      </section>
    </div>
  );
}

function FormattedOutput({ text }) {
  // tiny markdown-ish renderer (bold, lists). Safe to use innerHTML on our static strings.
  const html = text
    .replace(/\n\n/g, "</p><p>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/^([0-9]+)\. (.+)$/gm, "<div>$1. $2</div>")
    .replace(/^• (.+)$/gm, "<div>• $1</div>");
  return <div className="output-text" dangerouslySetInnerHTML={{ __html: "<p>" + html + "</p>" }} />;
}

function RunningStrip({ label }) {
  return (
    <div style={{
      display:"flex", alignItems:"center", gap:10, padding:"10px 12px",
      background:"var(--bg-2)", border:"1px solid var(--line)", borderRadius:8,
      fontFamily:"var(--mono)", fontSize:11.5, color:"var(--ink-2)"
    }}>
      <span className="loader" style={{
        width:10, height:10, borderRadius:"50%",
        background:"conic-gradient(from 0deg, var(--accent), transparent 70%)",
        animation:"spin 0.9s linear infinite",
      }} />
      <span>{label}</span>
      <span className="spacer" />
      <span className="muted">streaming</span>
    </div>
  );
}

Object.assign(window, { TabText, FormattedOutput, RunningStrip });
