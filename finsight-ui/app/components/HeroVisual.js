"use client";
import { motion } from "framer-motion";

export default function HeroVisual() {
  return (
    <motion.div
      animate={{ opacity: [0.6, 1, 0.6] }}
      transition={{ repeat: Infinity, duration: 6 }}
      style={{
        height: "120px",
        borderRadius: "16px",
        marginBottom: "24px",
        background: "linear-gradient(135deg, #34d39933, #38bdf833)",
        border: "1px solid var(--border)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: "var(--muted)"
      }}
    >
      Legal reasoning • Compliance • Intelligence
    </motion.div>
  );
}
