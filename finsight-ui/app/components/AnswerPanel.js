"use client";
import { motion } from "framer-motion";

export default function AnswerPanel({ data, loading }) {
  if (loading) {
    return (
      <motion.div
        animate={{ opacity: [0.4, 1, 0.4] }}
        transition={{ repeat: Infinity, duration: 1.2 }}
        style={{ color: "var(--muted)" }}
      >
        Interpreting legal framework…
      </motion.div>
    );
  }

  if (!data) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      style={{
        background: "var(--card)",
        border: "1px solid var(--border)",
        padding: "28px",
        borderRadius: "18px"
      }}
    >
      <h3 style={{ color: "var(--accent2)" }}>Legal Interpretation</h3>
      <p style={{ lineHeight: 1.7 }}>{data.answer}</p>
    </motion.div>
  );
}
