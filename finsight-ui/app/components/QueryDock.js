"use client";
import { useState } from "react";

export default function QueryDock({ onSubmit, loading }) {
  const [q, setQ] = useState("");

  return (
    <div style={{
      padding: "20px 32px",
      borderTop: "1px solid var(--border)",
      backdropFilter: "blur(10px)"
    }}>
      <textarea
        rows={2}
        placeholder="Ask about GST, MSME, EPF, ESIC, labour compliance…"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            onSubmit(q);
            setQ("");
          }
        }}
        style={{ width: "100%" }}
      />

      <div style={{ textAlign: "right", marginTop: "10px" }}>
        <button
          disabled={loading}
          onClick={() => { onSubmit(q); setQ(""); }}
          style={{
            background: "linear-gradient(135deg, var(--accent), var(--accent2))",
            color: "#020617",
            padding: "8px 20px",
            borderRadius: "12px",
            border: "none",
            cursor: "pointer"
          }}
        >
          {loading ? "Analyzing…" : "Analyze"}
        </button>
      </div>
    </div>
  );
}
