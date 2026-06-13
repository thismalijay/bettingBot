import type { ApiResponse } from "@/lib/types";

interface KpiCardsProps {
  data: ApiResponse;
}

function Card({
  label,
  value,
  sub,
  accent,
}: {
  label: string;
  value: string;
  sub?: string;
  accent?: "emerald" | "amber" | "cyan" | "slate";
}) {
  const accentColor = {
    emerald: "text-emerald-400",
    amber: "text-amber-400",
    cyan: "text-cyan-400",
    slate: "text-slate-100",
  }[accent ?? "slate"];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 flex flex-col gap-1">
      <span className="text-xs text-slate-500 uppercase tracking-widest font-medium">{label}</span>
      <span className={`text-2xl font-mono font-bold ${accentColor}`}>{value}</span>
      {sub && <span className="text-xs text-slate-500">{sub}</span>}
    </div>
  );
}

export function KpiCards({ data }: KpiCardsProps) {
  const bestEdge = data.bets.length > 0 ? Math.max(...data.bets.map((b) => b.edge_pct)) : 0;
  const totalExposure = data.bets.reduce((acc, b) => acc + b.recommended_stake, 0);
  const avgEdge =
    data.bets.length > 0
      ? data.bets.reduce((acc, b) => acc + b.edge_pct, 0) / data.bets.length
      : 0;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      <Card
        label="Matchs chargés"
        value={String(data.matches_count)}
        sub={`sur ${data.bets.length > 0 ? new Set(data.bets.map((b) => b.match)).size : 0} avec value`}
        accent="cyan"
      />
      <Card
        label="Value Bets"
        value={String(data.bets_count)}
        sub={`edge min ${(data.min_edge * 100).toFixed(0)}%`}
        accent="emerald"
      />
      <Card
        label="Meilleur Edge"
        value={`+${bestEdge.toFixed(1)}%`}
        sub={`moy. +${avgEdge.toFixed(1)}%`}
        accent={bestEdge >= 5 ? "emerald" : "amber"}
      />
      <Card
        label="Exposition Totale"
        value={`${totalExposure.toFixed(0)} EUR`}
        sub={`bankroll ${data.bankroll.toFixed(0)} EUR`}
        accent="slate"
      />
    </div>
  );
}
