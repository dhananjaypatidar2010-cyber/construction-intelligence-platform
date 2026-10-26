import { useEffect, useState } from "react";
import { Cracks, Safety } from "./pages/ImagePages.jsx";
import { Planning, Valuation } from "./pages/PlanPages.jsx";
import { Daily, Knowledge, Weather } from "./pages/AssistPages.jsx";

const MODULES = [
  { id: "safety", name: "Safety monitoring", group: "Inspect", C: Safety },
  { id: "cracks", name: "Crack analysis", group: "Inspect", C: Cracks },
  { id: "planning", name: "Project planning", group: "Plan", C: Planning },
  { id: "valuation", name: "Real estate valuation", group: "Plan", C: Valuation },
  { id: "daily", name: "Daily site assistant", group: "Operate", C: Daily },
  { id: "weather", name: "Weather advisory", group: "Operate", C: Weather },
  { id: "knowledge", name: "Knowledge assistant", group: "Operate", C: Knowledge },
];

export default function App() {
  const [id, setId] = useState(() => location.hash.slice(1) || "safety");
  const [provider, setProvider] = useState("");
  useEffect(() => { location.hash = id; }, [id]);
  useEffect(() => {
    fetch((import.meta.env.VITE_API_URL || "/api") + "/health").then((r) => r.json()).then((d) => setProvider(d.provider)).catch(() => setProvider("offline"));
  }, []);
  const Current = (MODULES.find((m) => m.id === id) || MODULES[0]).C;
  const groups = [...new Set(MODULES.map((m) => m.group))];

  return (
    <div className="shell">
      <nav className="side" aria-label="Modules">
        <div className="brand">Construction<br />Intelligence</div>
        {groups.map((g) => (
          <div key={g}>
            <h2>{g}</h2>
            {MODULES.filter((m) => m.group === g).map((m) => (
              <button key={m.id} className={m.id === id ? "nav on" : "nav"} onClick={() => setId(m.id)}>{m.name}</button>
            ))}
          </div>
        ))}
        <p className={`provider ${provider === "offline" ? "bad" : ""}`}>
          {provider === "offline" ? "Backend not reachable" : provider === "mock" ? "Demo mode: sample data" : provider ? `AI: ${provider}` : ""}
        </p>
      </nav>
      <main><Current key={id} /></main>
    </div>
  );
}
