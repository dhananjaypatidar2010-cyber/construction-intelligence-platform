import { useRef, useState } from "react";
import { postJson } from "../api.js";
import { Field, Page, Status, useAction } from "../components/Common.jsx";
import Result from "../components/Result.jsx";

function useLocation() {
  const [loc, setLoc] = useState({ latitude: "", longitude: "" });
  const [msg, setMsg] = useState("");
  const detect = () => {
    if (!navigator.geolocation) return setMsg("This browser cannot share location. Enter coordinates by hand.");
    navigator.geolocation.getCurrentPosition(
      (p) => { setLoc({ latitude: p.coords.latitude.toFixed(4), longitude: p.coords.longitude.toFixed(4) }); setMsg(""); },
      () => setMsg("Location was blocked. Enter coordinates by hand.")
    );
  };
  return { loc, setLoc, msg, detect };
}

function LocationFields({ l }) {
  return (
    <>
      <div className="grid">
        <Field label="Latitude"><input type="number" step="any" value={l.loc.latitude} onChange={(e) => l.setLoc({ ...l.loc, latitude: e.target.value })} /></Field>
        <Field label="Longitude"><input type="number" step="any" value={l.loc.longitude} onChange={(e) => l.setLoc({ ...l.loc, longitude: e.target.value })} /></Field>
      </div>
      <button type="button" className="ghost" onClick={l.detect}>Use my location</button>
      {l.msg && <p className="status error">{l.msg}</p>}
    </>
  );
}

export function Daily() {
  const l = useLocation();
  const [tasks, setTasks] = useState("");
  const [crew, setCrew] = useState(10);
  const [notes, setNotes] = useState("");
  const [state, run] = useAction(() =>
    postJson("/assistant/daily", {
      tasks_today: tasks.split("\n").map((s) => s.trim()).filter(Boolean),
      crew_size: Number(crew) || 1,
      notes,
      latitude: l.loc.latitude === "" ? null : Number(l.loc.latitude),
      longitude: l.loc.longitude === "" ? null : Number(l.loc.longitude),
    })
  );
  return (
    <Page title="Daily site assistance" intro="List today’s tasks and get a briefing: priorities, safety reminders, materials to check and risks.">
      <Field label="Today’s tasks" hint="One per line"><textarea rows={4} value={tasks} onChange={(e) => setTasks(e.target.value)} placeholder={"Pour first-floor slab\nInspect scaffold\nReceive steel delivery"} /></Field>
      <Field label="Crew size"><input type="number" min="1" value={crew} onChange={(e) => setCrew(e.target.value)} /></Field>
      <Field label="Notes"><textarea rows={2} value={notes} onChange={(e) => setNotes(e.target.value)} /></Field>
      <p className="muted">Add a location to include live weather in the briefing.</p>
      <LocationFields l={l} />
      <button disabled={!tasks.trim() || state.loading} onClick={run}>Get briefing</button>
      <Status state={state} loadingText="Preparing briefing…" />
    </Page>
  );
}

export function Weather() {
  const l = useLocation();
  const [activity, setActivity] = useState("concrete pouring");
  const [state, run] = useAction(() =>
    postJson("/advisory/weather", { latitude: Number(l.loc.latitude), longitude: Number(l.loc.longitude), activity })
  );
  const ready = l.loc.latitude !== "" && l.loc.longitude !== "";
  return (
    <Page title="Weather-aware advisory" intro="Live weather checked against safety thresholds. High wind, storms or hail always force a halt, whatever the AI says.">
      <LocationFields l={l} />
      <Field label="Planned activity"><input value={activity} onChange={(e) => setActivity(e.target.value)} /></Field>
      <button disabled={!ready || state.loading} onClick={run}>Check conditions</button>
      <Status state={state} loadingText="Checking weather…" />
    </Page>
  );
}

export function Knowledge() {
  const [history, setHistory] = useState([]);
  const [q, setQ] = useState("");
  const [last, setLast] = useState(null);
  const [state, setState] = useState({ loading: false, error: "" });
  const end = useRef(null);

  const ask = async (question) => {
    if (!question.trim()) return;
    const turns = [...history, { role: "user", content: question }];
    setHistory(turns);
    setQ("");
    setState({ loading: true, error: "" });
    try {
      const res = await postJson("/knowledge/ask", { question, history });
      setHistory([...turns, { role: "assistant", content: res.answer }]);
      setLast(res);
      setState({ loading: false, error: "" });
    } catch (e) {
      setState({ loading: false, error: e.message });
    }
    setTimeout(() => end.current?.scrollIntoView({ behavior: "smooth" }), 50);
  };

  return (
    <Page title="Construction knowledge assistant" intro="Ask about methods, materials, codes and troubleshooting.">
      <div className="chat">
        {history.length === 0 && <p className="muted">Try: “How long should a slab be cured?”</p>}
        {history.map((t, i) => (
          <div key={i} className={`bubble ${t.role}`}>{t.content}</div>
        ))}
        {state.loading && <p className="status">Thinking…</p>}
        {state.error && <p className="status error" role="alert">{state.error}</p>}
        <div ref={end} />
      </div>
      {last && (
        <div className="chips">
          {last.follow_up_questions.map((f) => (
            <button key={f} className="chip" onClick={() => ask(f)}>{f}</button>
          ))}
        </div>
      )}
      {last && last.references.length > 0 && <p className="muted">References: {last.references.join(" · ")}</p>}
      <form className="askbar" onSubmit={(e) => { e.preventDefault(); ask(q); }}>
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Ask a construction question" aria-label="Question" />
        <button disabled={state.loading || q.trim().length < 3}>Ask</button>
      </form>
    </Page>
  );
}
