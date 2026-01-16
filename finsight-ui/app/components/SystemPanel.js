"use client";

export default function SystemPanel({ data, loading }) {
  return (
    <aside style={{
      padding: "28px",
      borderRight: "1px solid var(--border)",
      color: "var(--muted)"
    }}>
      <h4 style={{ color: "var(--accent)" }}>System State</h4>

      <div style={{ marginTop: "16px" }}>
        <strong>Intent</strong>
        <div>{data?.intent || "—"}</div>
      </div>

      <div style={{ marginTop: "12px" }}>
        <strong>Confidence</strong>
        <div>{data?.confidence ?? "—"}</div>
      </div>

      <div style={{ marginTop: "12px" }}>
        <strong>Law</strong>
        <div>{data?.entities?.law || "—"}</div>
      </div>

      {loading && <div style={{ marginTop: "16px" }}>▣ Processing…</div>}
    </aside>
  );
}
