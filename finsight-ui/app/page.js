"use client";

import { useState } from "react";
import QueryInput from "./components/QueryInput";
import AnswerPanel from "./components/AnswerPanel";
import SignalBar from "./components/SignalBar";

export default function Home() {
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function handleQuery(query) {
    setLoading(true);
    setResponse(null);

    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });

    const data = await res.json();
    setResponse(data);
    setLoading(false);
  }

  return (
    <div style={{ display: "grid", gridTemplateColumns: "280px 1fr", height: "100vh" }}>
      <SignalBar data={response} loading={loading} />
      <main style={{ padding: "40px", display: "flex", flexDirection: "column" }}>
        <h1 style={{ fontSize: "1.8rem", marginBottom: "20px" }}>
          FinSight <span style={{ color: "var(--accent)" }}>Legal Intelligence</span>
        </h1>

        <QueryInput onSubmit={handleQuery} loading={loading} />
        <AnswerPanel response={response} loading={loading} />
      </main>
    </div>
  );
}
