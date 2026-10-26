import { useState } from "react";
import Result from "./Result.jsx";

export function useAction(fn) {
  const [state, set] = useState({ loading: false, error: "", data: null });
  const run = async (...args) => {
    set({ loading: true, error: "", data: null });
    try {
      set({ loading: false, error: "", data: await fn(...args) });
    } catch (e) {
      set({ loading: false, error: e.message || "Something went wrong", data: null });
    }
  };
  return [state, run];
}

export function Status({ state, loadingText = "Analysing…" }) {
  if (state.loading) return <p className="status" role="status">{loadingText}</p>;
  if (state.error) return <p className="status error" role="alert">{state.error}</p>;
  return <Result data={state.data} />;
}

export function Field({ label, children, hint }) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
      {hint && <small>{hint}</small>}
    </label>
  );
}

export function ImageDrop({ file, onFile }) {
  const url = file ? URL.createObjectURL(file) : null;
  return (
    <label className={`drop ${file ? "has" : ""}`}>
      {url ? <img src={url} alt="Selected upload" /> : <span>Choose a site photo (JPEG, PNG, WebP)</span>}
      <input type="file" accept="image/jpeg,image/png,image/webp,image/gif" onChange={(e) => onFile(e.target.files[0] || null)} />
    </label>
  );
}

export function Page({ title, intro, children }) {
  return (
    <div className="page">
      <h1>{title}</h1>
      <p className="intro">{intro}</p>
      {children}
    </div>
  );
}
