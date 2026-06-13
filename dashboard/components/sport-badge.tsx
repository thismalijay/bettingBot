const SPORT_COLORS: Record<string, string> = {
  soccer_fifa_world_cup: "bg-yellow-500/10 text-yellow-300 border-yellow-500/20",
  soccer_conmebol_copa_libertadores: "bg-blue-500/10 text-blue-300 border-blue-500/20",
  soccer_conmebol_copa_sudamericana: "bg-indigo-500/10 text-indigo-300 border-indigo-500/20",
  soccer_norway_eliteserien: "bg-red-500/10 text-red-300 border-red-500/20",
  soccer_sweden_allsvenskan: "bg-sky-500/10 text-sky-300 border-sky-500/20",
  basketball_nba: "bg-orange-500/10 text-orange-300 border-orange-500/20",
  tennis_wta_queens_club_champ: "bg-green-500/10 text-green-300 border-green-500/20",
};

const DEFAULT = "bg-slate-500/10 text-slate-300 border-slate-500/20";

export function SportBadge({ sportKey, label }: { sportKey: string; label: string }) {
  const colors = SPORT_COLORS[sportKey] ?? DEFAULT;
  return (
    <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium border ${colors} whitespace-nowrap`}>
      {label}
    </span>
  );
}
