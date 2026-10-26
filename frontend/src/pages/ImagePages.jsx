import { useState } from "react";
import { postImage } from "../api.js";
import { Field, ImageDrop, Page, Status, useAction } from "../components/Common.jsx";

export function Safety() {
  const [file, setFile] = useState(null);
  const [notes, setNotes] = useState("");
  const [state, run] = useAction(() => postImage("/safety/analyze", file, { notes }));
  return (
    <Page title="Site safety monitoring" intro="Upload a photo from site. The model checks PPE, edges, scaffolding and housekeeping, then lists what to fix first.">
      <ImageDrop file={file} onFile={setFile} />
      <Field label="Site notes (optional)">
        <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={2} placeholder="e.g. Level 3 slab, night shift" />
      </Field>
      <button disabled={!file || state.loading} onClick={run}>Check safety</button>
      <Status state={state} loadingText="Inspecting photo…" />
    </Page>
  );
}

export function Cracks() {
  const [file, setFile] = useState(null);
  const [element, setElement] = useState("wall");
  const [state, run] = useAction(() => postImage("/cracks/analyze", file, { element }));
  return (
    <Page title="Crack detection and analysis" intro="Upload a close-up of a crack. Place a coin or ruler beside it for a better width estimate.">
      <ImageDrop file={file} onFile={setFile} />
      <Field label="Building element">
        <select value={element} onChange={(e) => setElement(e.target.value)}>
          {["wall", "column", "beam", "slab", "foundation", "floor", "ceiling"].map((x) => (
            <option key={x}>{x}</option>
          ))}
        </select>
      </Field>
      <button disabled={!file || state.loading} onClick={run}>Analyse crack</button>
      <Status state={state} loadingText="Analysing crack…" />
    </Page>
  );
}
