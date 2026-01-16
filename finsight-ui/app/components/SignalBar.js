"use client";
import { motion } from "framer-motion";

export default function SignalBar({ data, loading }) {
  return (
    <aside
      style={{
        background: "#020617",
        borderRight: "1px solid #1f2937",
        padding: "20px"
      }}
    >
      <h3 style={{ fontSize: "0.9rem", color: "var(--muted)" }}>SYSTEM SIGNALS</h3>

      <motion.div
        animate={{ opacity: loading ? 0.5 : 1 }}
        style={{ marginTop: "20px" }}
      >
        <div>
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
      </motion.div>
    </aside>
  );
}
