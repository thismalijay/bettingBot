"use client";

interface LiveBadgeProps {
  mode: "live" | "demo";
}

export function LiveBadge({ mode }: LiveBadgeProps) {
  const isLive = mode === "live";
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold tracking-wider ${
        isLive
          ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
          : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
      }`}
    >
      <span
        className={`w-1.5 h-1.5 rounded-full pulse-dot ${
          isLive ? "bg-emerald-400" : "bg-amber-400"
        }`}
      />
      {isLive ? "LIVE" : "DEMO"}
    </span>
  );
}
