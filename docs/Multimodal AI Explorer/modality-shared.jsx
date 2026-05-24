// modality-shared.jsx — recommendation strip, output meta, helpers used by all 4 tabs
const { useState: _useState } = React;

function Recommendations({ modalityId, appliedModel, onApply }) {
  const m = window.MODALITIES[modalityId];
  if (!m) return null;
  return (
    <div className="recs">
      <div style={{display:"inline-flex", alignItems:"center", gap:6, fontFamily:"var(--mono)", fontSize:10, textTransform:"uppercase", letterSpacing:".12em", color:"var(--ink-3)", marginRight:4}}>
        <span style={{color:"var(--accent)"}}>★</span> Recommendations
      </div>
      {m.recs.map((r, i) => {
        const isApplied = r.model === appliedModel;
        return (
          <button
            key={i}
            className={classNames("rec", isApplied && "is-applied")}
            onClick={() => onApply(r)}
            title={r.note}
          >
            <span className="rec-star">{r.rating === "best" ? "★" : "·"}</span>
            <span className="rec-model">{abbrev(r.model)}</span>
            <span className="rec-prov">{r.provider}</span>
          </button>
        );
      })}
    </div>
  );
}

function OutputMeta({ model, temperature, latencyMs, status="ok" }) {
  return (
    <div className="output-meta">
      <span className={"pill " + (status === "ok" ? "ok" : "warn")}>
        {status === "ok" ? "● live" : "● error"}
      </span>
      <span className="pill">model: {abbrev(model || "—")}</span>
      <span className="pill">temp: {temperature.toFixed(2)}</span>
      <span className="pill">{latencyMs} ms</span>
    </div>
  );
}

// fake "running" delay
function useFakeRun() {
  const [running, setRunning] = _useState(false);
  const [latency, setLatency] = _useState(0);
  const [hasRun, setHasRun] = _useState(false);
  function run(ms=900) {
    setRunning(true); setHasRun(false);
    const t0 = performance.now();
    setTimeout(() => {
      setLatency(Math.round(performance.now() - t0));
      setRunning(false); setHasRun(true);
    }, ms);
  }
  return { running, latency, hasRun, run, reset: () => { setHasRun(false); setLatency(0); } };
}

Object.assign(window, { Recommendations, OutputMeta, useFakeRun });
