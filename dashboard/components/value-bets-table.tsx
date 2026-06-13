"use client";

import { useState } from "react";
import { ChevronUp, ChevronDown, ChevronsUpDown } from "lucide-react";
import type { ValueBet } from "@/lib/types";
import { SportBadge } from "./sport-badge";

type SortKey = keyof Pick<ValueBet, "edge_pct" | "odds" | "recommended_stake" | "kelly_pct">;
type SortDir = "asc" | "desc";

function EdgeCell({ pct }: { pct: number }) {
  const color =
    pct >= 8 ? "text-emerald-400" : pct >= 5 ? "text-emerald-300" : "text-amber-400";
  const bg =
    pct >= 8 ? "bg-emerald-500/10" : pct >= 5 ? "bg-emerald-500/5" : "bg-amber-500/10";
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded font-mono font-semibold text-sm ${color} ${bg}`}>
      +{pct.toFixed(1)}%
    </span>
  );
}

function SortIcon({ col, active, dir }: { col: string; active: boolean; dir: SortDir }) {
  if (!active) return <ChevronsUpDown className="w-3 h-3 text-slate-600" />;
  return dir === "desc"
    ? <ChevronDown className="w-3 h-3 text-cyan-400" />
    : <ChevronUp className="w-3 h-3 text-cyan-400" />;
}

interface Props {
  bets: ValueBet[];
}

export function ValueBetsTable({ bets }: Props) {
  const [sortKey, setSortKey] = useState<SortKey>("edge_pct");
  const [sortDir, setSortDir] = useState<SortDir>("desc");

  function handleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir((d) => (d === "desc" ? "asc" : "desc"));
    } else {
      setSortKey(key);
      setSortDir("desc");
    }
  }

  const sorted = [...bets].sort((a, b) => {
    const mult = sortDir === "desc" ? -1 : 1;
    return (a[sortKey] - b[sortKey]) * mult;
  });

  if (bets.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-12 text-center">
        <p className="text-slate-500 text-sm">Aucune value bet avec les criteres actuels.</p>
        <p className="text-slate-600 text-xs mt-1">Baissez MIN_EDGE dans le .env</p>
      </div>
    );
  }

  const cols: { key: SortKey; label: string }[] = [
    { key: "edge_pct", label: "Edge" },
    { key: "odds", label: "Cote" },
    { key: "kelly_pct", label: "Kelly" },
    { key: "recommended_stake", label: "Mise (EUR)" },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-800">
              <th className="text-left px-4 py-3 text-xs font-medium text-slate-500 uppercase tracking-wider whitespace-nowrap">
                Match
              </th>
              <th className="text-left px-4 py-3 text-xs font-medium text-slate-500 uppercase tracking-wider whitespace-nowrap">
                Competition
              </th>
              <th className="text-left px-4 py-3 text-xs font-medium text-slate-500 uppercase tracking-wider whitespace-nowrap">
                Bookmaker
              </th>
              <th className="text-left px-4 py-3 text-xs font-medium text-slate-500 uppercase tracking-wider whitespace-nowrap">
                Selection
              </th>
              {cols.map((c) => (
                <th key={c.key} className="px-4 py-3 whitespace-nowrap">
                  <button
                    onClick={() => handleSort(c.key)}
                    className="flex items-center gap-1 text-xs font-medium text-slate-500 uppercase tracking-wider hover:text-slate-300 transition-colors"
                  >
                    {c.label}
                    <SortIcon col={c.key} active={sortKey === c.key} dir={sortDir} />
                  </button>
                </th>
              ))}
              <th className="text-left px-4 py-3 text-xs font-medium text-slate-500 uppercase tracking-wider whitespace-nowrap">
                Prob Reelle
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/50">
            {sorted.map((bet, i) => (
              <tr key={i} className="bet-row transition-colors">
                <td className="px-4 py-3 text-slate-200 font-medium whitespace-nowrap max-w-[200px] truncate">
                  {bet.match}
                </td>
                <td className="px-4 py-3">
                  <SportBadge sportKey={bet.sport_key} label={bet.sport_label} />
                </td>
                <td className="px-4 py-3 text-slate-400 whitespace-nowrap">{bet.bookmaker}</td>
                <td className="px-4 py-3 text-slate-200 whitespace-nowrap font-medium">
                  {bet.outcome}
                </td>
                <td className="px-4 py-3">
                  <EdgeCell pct={bet.edge_pct} />
                </td>
                <td className="px-4 py-3 text-right font-mono text-yellow-300 whitespace-nowrap">
                  {bet.odds.toFixed(2)}
                </td>
                <td className="px-4 py-3 text-right font-mono text-slate-400 whitespace-nowrap">
                  {bet.kelly_pct.toFixed(1)}%
                </td>
                <td className="px-4 py-3 text-right font-mono font-semibold text-slate-100 whitespace-nowrap">
                  {bet.recommended_stake.toFixed(0)}
                </td>
                <td className="px-4 py-3 text-right font-mono text-slate-500 whitespace-nowrap">
                  {(bet.true_prob * 100).toFixed(1)}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
