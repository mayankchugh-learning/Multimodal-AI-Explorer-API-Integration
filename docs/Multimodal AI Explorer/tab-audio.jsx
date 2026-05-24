// tab-audio.jsx — Text → Audio (TTS) and Audio → Text (STT)
const { useState: _useStateA } = React;

function TabAudio({ provider, temperature, appliedModels, applyModel }) {
  const [tts, setTts] = _useStateA("Welcome to the multimodal lab. Today we'll wire up four providers across text, image, audio, and video.");
  const [voice, setVoice] = _useStateA("alloy");
  const ttsRun = useFakeRun();

  const [audioFile, setAudioFile] = _useStateA(null);
  const sttRun = useFakeRun();

  const modelAT = appliedModels.audio_to_text || "whisper-1";
  const modelTA = appliedModels.text_to_audio || "tts-1";

  function fakeAttach() {
    setAudioFile({ name: "standup-2026-05-22.m4a", size: "3.41 MB", duration: "00:42" });
    sttRun.reset();
  }

  return (
    <div className="split">
      {/* TTS */}
      <section className="card">
        <Recommendations modalityId="text_to_audio" appliedModel={modelTA} onApply={r => applyModel("text_to_audio", r)} />
        <div className="card-hd">
          <div className="card-hd-l">
            <span className="card-tag">T → A</span>
            <h3 className="card-title">Text-to-speech</h3>
          </div>
          <select className="ctrl-input" style={{width:120, padding:"5px 24px 5px 8px", fontSize:11.5}}
            value={voice} onChange={e => setVoice(e.target.value)}>
            <option>alloy</option><option>echo</option>
            <option>fable</option><option>onyx</option>
            <option>nova</option><option>shimmer</option>
          </select>
        </div>
        <div className="card-bd">
          <textarea
            className="textarea"
            value={tts} onChange={e => setTts(e.target.value)}
            style={{minHeight:96}}
            placeholder="Paste a script. The voice will read it aloud."
          />
          <div style={{display:"flex", gap:8, alignItems:"center"}}>
            <button className="kbtn kbtn-accent" onClick={() => ttsRun.run(1300)} disabled={ttsRun.running}>
              {ttsRun.running ? "Synthesizing…" : "Speak it"}
            </button>
            <button className="kbtn kbtn-ghost kbtn-sm">Voice: {voice}</button>
            <span className="spacer" />
            <span className="muted" style={{fontSize:11, fontFamily:"var(--mono)"}}>
              ~{Math.ceil(tts.length/14)} s @ mp3
            </span>
          </div>

          {ttsRun.running && <RunningStrip label={`synthesizing tts-1 (${voice})`} />}

          {ttsRun.hasRun && (
            <>
              <AudioPlayer label={`tts · ${voice}`} bars={64} duration="0:08" />
              <OutputMeta model={`tts-1 · ${voice}`} temperature={temperature} latencyMs={ttsRun.latency} />
            </>
          )}
          {!ttsRun.hasRun && !ttsRun.running && (
            <div className="dropzone" style={{padding:18, minHeight:90}}>
              <div className="dropzone-glyph">♪</div>
              <strong>Player will appear here</strong>
              <span>One-click playback after synthesis.</span>
            </div>
          )}
        </div>
      </section>

      {/* STT */}
      <section className="card">
        <Recommendations modalityId="audio_to_text" appliedModel={modelAT} onApply={r => applyModel("audio_to_text", r)} />
        <div className="card-hd">
          <div className="card-hd-l">
            <span className="card-tag">A → T</span>
            <h3 className="card-title">Transcribe audio</h3>
          </div>
          <button className="kbtn kbtn-ghost kbtn-sm" onClick={() => { setAudioFile(null); sttRun.reset(); }}>Clear</button>
        </div>
        <div className="card-bd">
          {!audioFile && (
            <div className="dropzone" onClick={fakeAttach}>
              <div className="dropzone-glyph">●</div>
              <strong>Upload or record audio</strong>
              <span>m4a · mp3 · wav · webm · up to 25 MB</span>
              <div style={{display:"flex", gap:6, marginTop:6}}>
                <button className="kbtn kbtn-ghost kbtn-sm" onClick={(e)=>{e.stopPropagation(); fakeAttach();}}>Upload file</button>
                <button className="kbtn kbtn-ghost kbtn-sm" onClick={(e)=>{e.stopPropagation(); fakeAttach();}}>● Record</button>
              </div>
            </div>
          )}
          {audioFile && (
            <>
              <div className="upfile">
                <div className="upfile-thumb">M4A</div>
                <div className="upfile-meta">
                  <b>{audioFile.name}</b>
                  <span>{audioFile.duration} · {audioFile.size}</span>
                </div>
                <button className="kbtn kbtn-ghost kbtn-sm">▶</button>
              </div>
              <AudioPlayer label="input · m4a" bars={48} duration={audioFile.duration} flat />
              <div style={{display:"flex", gap:8, alignItems:"center"}}>
                <button className="kbtn kbtn-accent" onClick={() => sttRun.run(1500)} disabled={sttRun.running}>
                  {sttRun.running ? "Transcribing…" : "Transcribe"}
                </button>
                <label style={{display:"inline-flex", alignItems:"center", gap:6, fontSize:12, color:"var(--ink-3)"}}>
                  <input type="checkbox" defaultChecked /> timestamps
                </label>
                <span className="spacer" />
                <span className="muted" style={{fontSize:11, fontFamily:"var(--mono)"}}>{abbrev(modelAT)}</span>
              </div>

              {sttRun.running && <RunningStrip label={`whisper · streaming segments`} />}

              {sttRun.hasRun && (
                <>
                  <FormattedOutput text={window.MOCK_OUTPUTS.audio_to_text} />
                  <OutputMeta model={modelAT} temperature={temperature} latencyMs={sttRun.latency} />
                </>
              )}
            </>
          )}
        </div>
      </section>
    </div>
  );
}

function AudioPlayer({ label="audio", bars=48, duration="0:08", flat=false }) {
  const heights = React.useMemo(() => {
    // deterministic pseudo-random waveform
    const out = []; let s = 7;
    for (let i = 0; i < bars; i++) {
      s = (s * 9301 + 49297) % 233280;
      const r = s / 233280;
      const t = i / bars;
      const env = Math.sin(t * Math.PI); // fade in/out
      const h = (flat ? 0.3 : 0.2) + 0.85 * env * (0.45 + r * 0.55);
      out.push(Math.max(0.08, Math.min(1, h)));
    }
    return out;
  }, [bars, flat]);

  return (
    <div style={{display:"flex", flexDirection:"column", gap:6}}>
      <div className="wave">
        {heights.map((h, i) => (
          <div key={i} className="bar" style={{height:`${Math.round(h*100)}%`,
            background: i < bars*0.32 ? "var(--accent)" : "var(--ink-3)",
            opacity: i < bars*0.32 ? 0.95 : 0.55 }} />
        ))}
      </div>
      <div style={{display:"flex", justifyContent:"space-between", alignItems:"center",
        fontFamily:"var(--mono)", fontSize:10.5, color:"var(--ink-3)"}}>
        <span>▶ {label}</span>
        <span>0:02 / {duration}</span>
      </div>
    </div>
  );
}

Object.assign(window, { TabAudio, AudioPlayer });
