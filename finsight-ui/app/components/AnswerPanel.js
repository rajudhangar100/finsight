"use client";
import { motion } from "framer-motion";

export default function AnswerPanel({ response, loading }) {
  if (loading) {
    return (
      <motion.div
        animate={{ opacity: [0.4, 1, 0.4] }}
        transition={{ repeat: Infinity, duration: 1.5 }}
        style={{ color: "var(--muted)" }}
      >
        Interpreting legal context...
      </motion.div>
    );
  }

  if (!response) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      style={{
        background: "linear-gradient(180deg, #111827, #020617)",
        border: "1px solid #1f2937",
        padding: "24px",
        borderRadius: "14px"
      }}
    >
      <p style={{ lineHeight: 1.6 }}>{response.answer}</p>

      {response.sources && (
        <div style={{ marginTop: "14px", color: "var(--muted)", fontSize: "0.85rem" }}>
          Sources: {response.sources.join(", ")}
        </div>
      )}
    </motion.div>
  );
}
