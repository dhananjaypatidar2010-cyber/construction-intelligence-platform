const BASE = import.meta.env.VITE_API_URL || "/api";

async function handle(res) {
  if (!res.ok) {
    let msg = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") msg = body.detail;
      else if (Array.isArray(body.detail))
        msg = body.detail.map((d) => `${d.loc.slice(1).join(".")}: ${d.msg}`).join("; ");
    } catch {}
    throw new Error(msg);
  }
  return res.json();
}

export const postJson = (path, body) =>
  fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  }).then(handle);

export const postImage = (path, file, fields = {}) => {
  const fd = new FormData();
  fd.append("image", file);
  Object.entries(fields).forEach(([k, v]) => fd.append(k, v));
  return fetch(`${BASE}${path}`, { method: "POST", body: fd }).then(handle);
};
