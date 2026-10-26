import { useState } from "react";
import { postJson } from "../api.js";
import { Field, Page, Status, useAction } from "../components/Common.jsx";

const num = (v) => (v === "" ? "" : Number(v));

export function Valuation() {
  const [f, setF] = useState({ location: "", property_type: "apartment", area_sqft: 1000, bedrooms: 2, age_years: 0, condition: "good", amenities: "", notes: "" });
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });
  const [state, run] = useAction(() =>
    postJson("/valuation", {
      ...f,
      area_sqft: num(f.area_sqft),
      bedrooms: num(f.bedrooms) || 0,
      age_years: num(f.age_years) || 0,
      amenities: f.amenities.split(",").map((s) => s.trim()).filter(Boolean),
    })
  );
  return (
    <Page title="Real estate valuation" intro="Get an indicative value range with the factors behind it. It is a guide, not a certified valuation.">
      <div className="grid">
        <Field label="Location"><input value={f.location} onChange={set("location")} placeholder="Locality, city" /></Field>
        <Field label="Property type">
          <select value={f.property_type} onChange={set("property_type")}>
            {["apartment", "independent house", "villa", "plot", "commercial"].map((x) => <option key={x}>{x}</option>)}
          </select>
        </Field>
        <Field label="Area (sq ft)"><input type="number" min="1" value={f.area_sqft} onChange={set("area_sqft")} /></Field>
        <Field label="Bedrooms"><input type="number" min="0" value={f.bedrooms} onChange={set("bedrooms")} /></Field>
        <Field label="Age (years)"><input type="number" min="0" value={f.age_years} onChange={set("age_years")} /></Field>
        <Field label="Condition">
          <select value={f.condition} onChange={set("condition")}>
            {["poor", "average", "good", "excellent"].map((x) => <option key={x}>{x}</option>)}
          </select>
        </Field>
      </div>
      <Field label="Amenities" hint="Separate with commas"><input value={f.amenities} onChange={set("amenities")} placeholder="parking, lift, security" /></Field>
      <Field label="Notes"><textarea rows={2} value={f.notes} onChange={set("notes")} /></Field>
      <button disabled={!f.location || state.loading} onClick={run}>Estimate value</button>
      <Status state={state} loadingText="Estimating value…" />
    </Page>
  );
}

export function Planning() {
  const [f, setF] = useState({ project_name: "", project_type: "residential building", area_sqft: 2000, budget: 5000000, duration_weeks: 52, location: "", constraints: "" });
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });
  const [state, run] = useAction(() =>
    postJson("/planning", { ...f, area_sqft: num(f.area_sqft), budget: num(f.budget), duration_weeks: num(f.duration_weeks) })
  );
  return (
    <Page title="Construction project planning" intro="Turn a brief into phases, tasks, milestones, resources and risks that fit your budget and timeline.">
      <div className="grid">
        <Field label="Project name"><input value={f.project_name} onChange={set("project_name")} /></Field>
        <Field label="Project type"><input value={f.project_type} onChange={set("project_type")} /></Field>
        <Field label="Built-up area (sq ft)"><input type="number" min="1" value={f.area_sqft} onChange={set("area_sqft")} /></Field>
        <Field label="Budget"><input type="number" min="1" value={f.budget} onChange={set("budget")} /></Field>
        <Field label="Duration (weeks)"><input type="number" min="1" value={f.duration_weeks} onChange={set("duration_weeks")} /></Field>
        <Field label="Location"><input value={f.location} onChange={set("location")} /></Field>
      </div>
      <Field label="Constraints"><textarea rows={2} value={f.constraints} onChange={set("constraints")} placeholder="Narrow plot, monsoon start in June…" /></Field>
      <button disabled={!f.project_name || state.loading} onClick={run}>Build plan</button>
      <Status state={state} loadingText="Building plan…" />
    </Page>
  );
}
