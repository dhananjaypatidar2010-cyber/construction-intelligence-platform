const SEVERITY = new Set(["low", "medium", "high", "critical"]);
const money = (n) => Number(n).toLocaleString(undefined, { maximumFractionDigits: 0 });

const label = (k) => k.replace(/_/g, " ").replace(/^./, (c) => c.toUpperCase());

function Value({ k, v }) {
  if (v === null || v === undefined) return <span className="muted">Not available</span>;
  if (typeof v === "boolean") return <b>{v ? "Yes" : "No"}</b>;
  if (typeof v === "number") {
    if (/value|cost|price/.test(k)) return <b>{money(v)}</b>;
    return <b>{v}</b>;
  }
  if (typeof v === "string") {
    const lower = v.toLowerCase();
    if (SEVERITY.has(lower) || ["proceed", "caution", "halt"].includes(lower))
      return <span className={`tag tag-${lower}`}>{v}</span>;
    return <span>{v}</span>;
  }
  if (Array.isArray(v)) {
    if (v.length === 0) return <span className="muted">None</span>;
    if (typeof v[0] !== "object")
      return (
        <ul className="plain">
          {v.map((x, i) => (
            <li key={i}>{x}</li>
          ))}
        </ul>
      );
    return (
      <div className="stack">
        {v.map((x, i) => (
          <div className="card-in" key={i}>
            <Fields data={x} />
          </div>
        ))}
      </div>
    );
  }
  return <Fields data={v} />;
}

function Fields({ data }) {
  return (
    <dl>
      {Object.entries(data).map(([k, v]) => (
        <div className="row" key={k}>
          <dt>{label(k)}</dt>
          <dd>
            <Value k={k} v={v} />
          </dd>
        </div>
      ))}
    </dl>
  );
}

export default function Result({ data }) {
  if (!data) return null;
  return (
    <section className="result" aria-live="polite">
      <Fields data={data} />
    </section>
  );
}
