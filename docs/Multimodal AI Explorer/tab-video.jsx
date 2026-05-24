// tab-video.jsx — Video → Text (frame sampling) and Text → Video (informational placeholder)
const { useState: _useStateV } = React;

function TabVideo({ provider, temperature, appliedModels, applyModel }) {
  const [vfile, setVfile] = _useStateV(null);
  const [focus, setFocus] = _useStateV("What is this video about? Any text on screen?");
  const [frameCount, setFrameCount] = _useStateV(8);
  const r = useFakeRun();
  const modelVT = appliedModels.video_to_text || "gpt-4o-mini";

  function attach() {
    setVfile({ name: "kitchen-blender-demo.mp4", size: "12.4 MB", duration: "01:02", fps: 30, dim:"1920×1080" });
    r.reset();
  }

  return (
    <div className="split">
      {/* V → T */}
      <section className="card">
        <Recommendations modalityId="video_to_text" appliedModel={modelVT} onApply={rec => applyModel("video_to_text", rec)} />
        <div className="card-hd">
          <div className="card-hd-l">
            <span className="card-tag">V → T</span>
            <h3 className="card-title">Summarize video</h3>
          </div>
          <button className="kbtn kbtn-ghost kbtn-sm" onClick={() => { setVfile(null); r.reset(); }}>Clear</button>
        </div>

        <div className="card-bd">
          {!vfile && (
            <div className="dropzone" onClick={attach}>
              <div className="dropzone-glyph">▶</div>
              <strong>Upload a short video</strong>
              <span>mp4 · mov · webm · up to 60 s recommended</span>
              <span className="muted" style={{fontSize:11}}>Frames are sampled with OpenCV, then sent to a vision model.</span>
            </div>
          )}

          {vfile && (
            <>
              <div className="upfile">
                <div className="upfile-thumb">MP4</div>
                <div className="upfile-meta">
                  <b>{vfile.name}</b>
                  <span>{vfile.duration} · {vfile.dim} · {vfile.fps} fps · {vfile.size}</span>
                </div>
                <button className="kbtn kbtn-ghost kbtn-sm">▶</button>
              </div>

              <div style={{display:"flex", flexDirection:"column", gap:6}}>
                <div className="ctrl-lbl">
                  <span>Sample frames</span>
                  <span className="ctrl-val">{frameCount} frames · every {(parseFloat(vfile.duration.split(":")[1])/frameCount).toFixed(1)}s</span>
                </div>
                <input className="ctrl-slider" type="range" min={2} max={12} step={1}
                  value={frameCount} onChange={e => setFrameCount(parseInt(e.target.value, 10))} />
              </div>

              <div>
                <div className="card-tag" style={{marginBottom:6}}>Extracted frames · base64</div>
                <Filmstrip count={frameCount} duration={vfile.duration} />
              </div>

              <textarea
                className="textarea"
                value={focus} onChange={e => setFocus(e.target.value)}
                style={{minHeight:60, fontSize:13}}
                placeholder="Optional focus question for the vision model…"
              />

              <div style={{display:"flex", gap:8, alignItems:"center"}}>
                <button className="kbtn kbtn-accent" onClick={() => r.run(2200)} disabled={r.running}>
                  {r.running ? "Reading frames…" : "Summarize"}
                </button>
                <span className="muted" style={{fontSize:11.5}}>this may take a minute on long clips</span>
                <span className="spacer" />
                <span className="muted" style={{fontSize:11, fontFamily:"var(--mono)"}}>{abbrev(modelVT)}</span>
              </div>

              {r.running && <RunningStrip label={`extracting ${frameCount} frames → vision`} />}

              {r.hasRun && (
                <>
                  <FormattedOutput text={window.MOCK_OUTPUTS.video_to_text} />
                  <OutputMeta model={modelVT} temperature={temperature} latencyMs={r.latency} />
                </>
              )}
            </>
          )}
        </div>
      </section>

      {/* T → V placeholder */}
      <section className="card">
        <div className="card-hd">
          <div className="card-hd-l">
            <span className="card-tag">T → V</span>
            <h3 className="card-title">Text-to-video</h3>
          </div>
          <span className="card-sub" style={{color:"var(--bad)"}}>informational</span>
        </div>

        <div className="card-bd">
          <textarea
            className="textarea"
            defaultValue="A slow drone shot over autumn forest, golden hour, soft fog rolling between the trees."
            style={{minHeight:80, opacity:.85}}
          />
          <div className="notice">
            <b>Not wired to a paid API.</b> Production video generation requires a separate billing
            relationship with one of the providers below. The notebook documents the call shapes; the
            app shows the routing only.
          </div>

          <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:8}}>
            <ProviderCard name="OpenAI · Sora"  status="preview"   blurb="Limited access · 5–20 s clips · waitlist" />
            <ProviderCard name="Google · Veo"   status="vertex-ai" blurb="Vertex AI region-gated · text + image refs" />
            <ProviderCard name="Runway · Gen-3" status="public"    blurb="REST + dashboard · per-second pricing" />
            <ProviderCard name="Luma · Dream"   status="public"    blurb="Cheap, fast · 5 s ceiling" />
          </div>

          <div style={{display:"flex", gap:8}}>
            <button className="kbtn kbtn-ghost kbtn-sm">Copy curl recipe</button>
            <button className="kbtn kbtn-ghost kbtn-sm">View pricing notes</button>
          </div>
        </div>
      </section>
    </div>
  );
}

function Filmstrip({ count=8, duration="01:02" }) {
  const [mm, ss] = duration.split(":").map(n => parseInt(n, 10));
  const totalSec = (mm||0)*60 + (ss||0);
  const stamps = [];
  for (let i = 0; i < count; i++) {
    const t = Math.round((totalSec * (i + 0.5)) / count);
    const m = Math.floor(t / 60).toString().padStart(2, "0");
    const s = (t % 60).toString().padStart(2, "0");
    stamps.push(`${m}:${s}`);
  }
  return (
    <div className="filmstrip" style={{gridTemplateColumns:`repeat(${Math.min(8, count)},1fr)`}}>
      {stamps.map((t, i) => (
        <div key={i} className={`frame f${(i % 4) + 1}`} data-t={t} />
      ))}
    </div>
  );
}

function ProviderCard({ name, status, blurb }) {
  return (
    <div style={{
      border:"1px solid var(--line)", borderRadius:8, padding:"10px 12px",
      display:"flex", flexDirection:"column", gap:4, background:"var(--bg-2)"
    }}>
      <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
        <b style={{fontSize:12.5, fontWeight:600, color:"var(--ink)"}}>{name}</b>
        <span className="kbd" style={{fontSize:9.5}}>{status}</span>
      </div>
      <div className="muted" style={{fontSize:11.5, lineHeight:1.45}}>{blurb}</div>
    </div>
  );
}

Object.assign(window, { TabVideo, Filmstrip, ProviderCard });
