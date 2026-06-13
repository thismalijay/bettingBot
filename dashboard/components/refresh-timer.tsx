"use client";

import { useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";

interface Props {
  intervalSeconds: number;
  onRefresh: () => void;
  loading: boolean;
}

export function RefreshTimer({ intervalSeconds, onRefresh, loading }: Props) {
  const [remaining, setRemaining] = useState(intervalSeconds);

  useEffect(() => {
    setRemaining(intervalSeconds);
    const tick = setInterval(() => {
      setRemaining((r) => {
        if (r <= 1) {
          onRefresh();
          return intervalSeconds;
        }
        return r - 1;
      });
    }, 1000);
    return () => clearInterval(tick);
  }, [intervalSeconds, onRefresh]);

  return (
    <div className="flex items-center gap-2 text-xs text-slate-500">
      <RefreshCw className={`w-3 h-3 ${loading ? "animate-spin text-cyan-400" : ""}`} />
      <span>
        {loading ? "Mise a jour..." : `Refresh dans ${remaining}s`}
      </span>
    </div>
  );
}
