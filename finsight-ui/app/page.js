"use client";
import { useState } from "react";
import QueryDock from "./components/QueryDock";
import AnswerPanel from "./components/AnswerPanel";
import SystemPanel from "./components/SystemPanel";
import HeroVisual from "./components/HeroVisual";

export default function Home() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  async function runQuery(q) {
    setLoading(true);
    setData(null);

    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: q })
    });

    const json = await res.json();
    setData(json);
    setLoading(false);
  }

  return (
    <div style={{ display: "grid", gridTemplateRows: "80px 1fr 140px", height: "100vh" }}>
      <header style={{ padding: "20px 32px", fontSize: "1.3rem" }}>
        <span style={{ color: "var(--accent)" }}>FinSight</span>{" "}
        <span style={{ color: "var(--muted)" }}>Legal Intelligence</span>
      </header>

      <div style={{ display: "grid", gridTemplateColumns: "320px 1fr" }}>
        <SystemPanel data={data} loading={loading} />
        <div style={{ padding: "32px" }}>
          <HeroVisual />
          <AnswerPanel data={data} loading={loading} />
        </div>
      </div>

      <QueryDock onSubmit={runQuery} loading={loading} />
    </div>
  );
}
