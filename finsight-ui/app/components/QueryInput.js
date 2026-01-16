"use client";
import { useState } from "react";
import { motion } from "framer-motion";

export default function QueryInput({
  onSubmit,
  loading
}) {
  const [value, setValue] = useState("");

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      style={{
        background: "var(--panel)",
        padding: "16px",
        borderRadius: "12px",
        marginBottom: "20px"
      }}
    >
      <textarea
        rows={2}
        placeholder="Ask about GST, MSME, EPF, ESIC, compliance..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            onSubmit(value);
            setValue("");
          }
        }}
        style={{ width: "100%", resize: "none" }}
      />

      <div style={{ textAlign: "right", marginTop: "8px" }}>
        <button
          disabled={loading}
          onClick={() => {
            onSubmit(value);
            setValue("");
          }}
          style={{
            background: "var(--accent)",
            color: "#000",
            padding: "6px 14px",
            borderRadius: "8px",
            cursor: "pointer",
            border: "none"
          }}
        >
          {loading ? "Analyzing..." : "Ask"}
        </button>
      </div>
    </motion.div>
  );
}
