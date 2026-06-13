"use client";

import { useCallback, useEffect, useState } from "react";
import { TrendingUp, AlertCircle } from "lucide-react";
import { fetchValueBets } from "@/lib/api";
import type { ApiResponse } from "@/lib/types";
import { LiveBadge } from "@/components/live-badge";
import { KpiCards } from "@/components/kpi-cards";
import { ValueBetsTable } from "@/components/value-bets-table";
import { RefreshTimer } from "@/components/refresh-timer";

const REFRESH_INTERVAL = 60; // secondes

export default function Dashboard() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchValueBets();
      setData(res);
      setLastUpdated(new Date());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur inconnue");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            <span className="font-semibold text-slate-100 tracking-tight">BetEdge</span>
            <span className="text-slate-600 text-sm hidden sm:block">Value Bet Dashboard</span>
          </div>
          <div className="flex items-center gap-4">
            {data && <LiveBadge mode={data.mode} />}
            {lastUpdated && (
              <span className="text-xs text-slate-600 hidden sm:block font-mono">
                {lastUpdated.toLocaleTimeString("fr-FR")}
              </span>
            )}
            <RefreshTimer
              intervalSeconds={REFRESH_INTERVAL}
              onRefresh={load}
              loading={loading}
            />
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 py-6 flex flex-col gap-5">
        {/* Error */}
        {error && (
          <div className="flex items-center gap-3 bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-3 text-red-400 text-sm">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <div>
              <span className="font-medium">Impossible de joindre l&apos;API.</span>{" "}
              <span className="text-red-400/70">
                Verifiez que le serveur FastAPI tourne sur :8000
              </span>
            </div>
          </div>
        )}

        {/* Loading skeleton */}
        {loading && !data && (
          <div className="animate-pulse space-y-3">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-20 bg-slate-800/50 rounded-lg" />
              ))}
            </div>
            <div className="h-64 bg-slate-800/50 rounded-lg" />
          </div>
        )}

        {/* Content */}
        {data && (
          <>
            <KpiCards data={data} />

            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-widest">
                Value Bets — {data.bets_count} detectees
              </h2>
              <span className="text-xs text-slate-600 font-mono">
                tri par edge decroissant par defaut
              </span>
            </div>

            <ValueBetsTable bets={data.bets} />
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-3 px-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between text-xs text-slate-600">
          <span>
            True odds via{" "}
            <span className="text-slate-500">Pinnacle</span> → consensus bookmakers
          </span>
          {data && (
            <span className="font-mono">
              Kelly {(data.kelly_fraction * 100).toFixed(0)}% · Edge min{" "}
              {(data.min_edge * 100).toFixed(0)}% · Bankroll {data.bankroll.toFixed(0)} EUR
            </span>
          )}
        </div>
      </footer>
    </div>
  );
}
