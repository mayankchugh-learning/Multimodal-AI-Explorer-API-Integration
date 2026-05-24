// tab-image.jsx — Image → Text (vision Q&A)
const { useState: _useStateI } = React;

function TabImage({ provider, temperature, appliedModels, applyModel }) {
  const [file, setFile] = _useStateI(null);
  const [question, setQuestion] = _useStateI("What's in this image? Pay attention to lighting and depth of field.");
  const r = useFakeRun();
  const modelIT = appliedModels.image_to_text || "gpt-4o-mini";

  function fakeUpload(name="honeybee-on-sunflower.jpg") {
    setFile({ name, size: "1.84 MB", w: 2048, h: 1365 });
    r.reset();
  }

  return (
    <div className="split">
      <section className="card">
        <Recommendations modalityId="image_to_text" appliedModel={modelIT} onApply={r2 => applyModel("image_to_text", r2)} />
        <div className="card-hd">
          <div className="card-hd-l">
            <span className="card-tag">I → T</span>
            <h3 className="card-title">Input image</h3>
          </div>
          <button className="kbtn kbtn-ghost kbtn-sm" onClick={() => { setFile(null); r.reset(); }}>Clear</button>
        </div>
        <div className="card-bd">
          {!file && (
            <div className="dropzone" onClick={() => fakeUpload()}>
              <div className="dropzone-glyph">↥</div>
              <strong>Drop an image or click to upload</strong>
              <span>PNG, JPG, WEBP · up to 20 MB</span>
              <span className="muted" style={{fontSize:11}}>Tip: try a photo with strong subject + background separation.</span>
            </div>
          )}
          {file && (
            <>
              <div className="img-stage" style={{aspectRatio:"3/2"}}>
                <div className="img-shape" style={{
                  background:"radial-gradient(circle at 35% 40%, rgba(255,255,255,.65), rgba(255,255,255,0) 55%), radial-gradient(circle at 70% 80%, oklch(0.5 0.16 30), transparent 60%)"
                }} />
                <span className="img-cap">{file.name}</span>
              </div>
              <div className="upfile" style={{marginTop:2}}>
                <div className="upfile-thumb">JPG</div>
                <div className="upfile-meta">
                  <b>{file.name}</b>
                  <span>{file.w} × {file.h} · {file.size}</span>
                </div>
                <button className="kbtn kbtn-ghost kbtn-sm" onClick={() => fakeUpload("sunset-pier-iceland.jpg")}>Swap</button>
              </div>
            </>
          )}
        </div>
        <div className="card-ft">
          <span>encoder · <b style={{color:"var(--ink)"}}>base64 inline</b></span>
          <span>max-side 1568px</span>
        </div>
      </section>

      <section className="card">
        <div className="card-hd">
          <div className="card-hd-l">
            <span className="card-tag">Q&amp;A</span>
            <h3 className="card-title">Ask about the image</h3>
          </div>
          <span className="card-sub">{file ? "ready" : "upload first"}</span>
        </div>
        <div className="card-bd">
          <textarea
            className="textarea"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            style={{minHeight:90}}
            placeholder="e.g. transcribe any text, describe the lighting, count the people…"
          />

          <div style={{display:"flex", gap:8, alignItems:"center"}}>
            <button
              className="kbtn kbtn-accent"
              disabled={!file || r.running}
              onClick={() => r.run(1200)}
              style={!file ? {opacity:0.5} : null}
            >
              {r.running ? "Analyzing…" : "Analyze"}
            </button>
            <button className="kbtn kbtn-ghost kbtn-sm" disabled={!file}>Describe (no Q)</button>
            <span className="spacer" />
            <span className="muted" style={{fontSize:11, fontFamily:"var(--mono)"}}>vision · {abbrev(modelIT)}</span>
          </div>

          {r.running && <RunningStrip label={`asking ${modelIT}`} />}

          {!r.hasRun && !r.running && (
            <div className="output-text" style={{color:"var(--ink-4)", fontStyle:"italic", minHeight:80}}>
              Model response will appear here.
            </div>
          )}

          {r.hasRun && (
            <>
              <FormattedOutput text={window.MOCK_OUTPUTS.image_to_text} />
              <OutputMeta model={modelIT} temperature={temperature} latencyMs={r.latency} />
            </>
          )}
        </div>
      </section>
    </div>
  );
}

window.TabImage = TabImage;
