// sidebar.jsx — left rail: brand, BYOK, provider status & picker, generation controls
const { useState } = React;

function Sidebar({
  byok, setByokKey, provider, setProvider,
  temperature, setTemperature, maxTokens, setMaxTokens,
  modelOverride, setModelOverride,
  configuredCount, onOpenLearn,
}) {
  const [byokOpen, setByokOpen] = useState(true);

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-row">
          <div className="brand-mark" aria-hidden="true" />
          <div>
            <div className="brand-title">Multimodal AI Explorer</div>
            <div className="brand-sub">openai · gemini · groq · anthropic · hf · ollama</div>
          </div>
        </div>
        <div className="brand-tag">Lab session · live</div>
      </div>

      <div className="sb-scroll">
        {/* BYOK */}
        <div className="sb-section">
          <h3 className="sb-h">
            <span>Bring your own key</span>
            <span className="sb-h-aux" onClick={() => setByokOpen(o => !o)} style={{cursor:"default"}}>
              {byokOpen ? "hide" : "show"}
            </span>
          </h3>
          {byokOpen && (
            <div className="byok">
              {window.PROVIDERS.map(p => {
                const filled = !!byok[p.id];
                return (
                  <div key={p.id} className={classNames("byok-row", filled && "has-key")}>
                    <label htmlFor={`k-${p.id}`}>{p.name}</label>
                    <input
                      id={`k-${p.id}`}
                      type="password"
                      placeholder={p.prefix + "…"}
                      value={byok[p.id] || ""}
                      onChange={(e) => setByokKey(p.id, e.target.value)}
                      autoComplete="new-password"
                      spellCheck={false}
                    />
                    <span className="byok-check">{filled ? "✓" : "·"}</span>
                  </div>
                );
              })}
              <div className="muted" style={{fontSize:11, marginTop:4, lineHeight:1.5}}>
                Keys stay in this session only. Nothing saved to disk.
              </div>
            </div>
          )}
        </div>

        {/* Provider status */}
        <div className="sb-section">
          <h3 className="sb-h">
            <span>Providers</span>
            <span className="sb-h-aux">{configuredCount}/{window.PROVIDERS.length} ready</span>
          </h3>
          <div className="prov-grid">
            {window.PROVIDERS.map(p => {
              const on = !!byok[p.id];
              const sel = p.id === provider;
              return (
                <div
                  key={p.id}
                  className={classNames("prov-pill", on ? "prov-on" : "prov-off", sel && "prov-sel")}
                  onClick={() => on && setProvider(p.id)}
                  title={on ? `Use ${p.name}` : `${p.env} not set`}
                >
                  <span className="prov-dot" />
                  <span className="prov-name">{p.name}</span>
                  <span className="prov-key">{p.env.split("_")[0].toLowerCase()}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Generation controls */}
        <div className="sb-section">
          <h3 className="sb-h"><span>Generation</span><span className="sb-h-aux">live</span></h3>

          <div className="ctrl-row">
            <div className="ctrl-lbl">
              <span>Temperature</span>
              <span className="ctrl-val">{temperature.toFixed(2)}</span>
            </div>
            <input
              className="ctrl-slider" type="range"
              min={0} max={2} step={0.05}
              value={temperature}
              onChange={e => setTemperature(parseFloat(e.target.value))}
            />
          </div>

          <div className="ctrl-row">
            <div className="ctrl-lbl">
              <span>Max tokens</span>
              <span className="ctrl-val">{maxTokens}</span>
            </div>
            <input
              className="ctrl-slider" type="range"
              min={64} max={8192} step={64}
              value={maxTokens}
              onChange={e => setMaxTokens(parseInt(e.target.value, 10))}
            />
          </div>

          <div className="ctrl-row" style={{marginTop:14}}>
            <div className="ctrl-lbl"><span>Model override</span><span className="ctrl-val muted">optional</span></div>
            <input
              className="ctrl-input"
              placeholder={`e.g. ${provider === "openai" ? "gpt-4o" : provider === "anthropic" ? "claude-3-5-sonnet-20241022" : "default"}`}
              value={modelOverride}
              onChange={e => setModelOverride(e.target.value)}
              spellCheck={false}
            />
          </div>
        </div>

        {/* Connection */}
        <div className="sb-section">
          <h3 className="sb-h"><span>Diagnostics</span></h3>
          <div style={{display:"flex", gap:6}}>
            <button className="kbtn kbtn-ghost kbtn-sm" style={{flex:1}}>Test {window.PROVIDERS.find(p=>p.id===provider)?.name || "provider"}</button>
            <button className="kbtn kbtn-ghost kbtn-sm">Reset</button>
          </div>
          <div className="muted" style={{fontSize:11, marginTop:8, lineHeight:1.5}}>
            <span style={{color:"var(--ok)"}}>● </span>Last ping <span className="kbd">214 ms</span> · region <span className="kbd">us-east</span>
          </div>
        </div>

        {/* Learn shortcut */}
        <div className="sb-section">
          <h3 className="sb-h"><span>Learn</span><span className="sb-h-aux">logic · langchain · arch</span></h3>
          <button className="kbtn kbtn-ghost" style={{width:"100%", justifyContent:"space-between"}} onClick={onOpenLearn}>
            <span>Open Learn drawer</span>
            <span className="kbd">L</span>
          </button>
        </div>
      </div>
    </aside>
  );
}

window.Sidebar = Sidebar;
