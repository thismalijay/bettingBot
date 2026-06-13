export interface ValueBet {
  match: string;
  sport_key: string;
  sport_label: string;
  bookmaker: string;
  outcome: string;
  odds: number;
  true_prob: number;
  edge: number;
  edge_pct: number;
  kelly_fraction: number;
  kelly_pct: number;
  recommended_stake: number;
}

export interface ApiResponse {
  updated_at: string;
  mode: "live" | "demo";
  bankroll: number;
  kelly_fraction: number;
  min_edge: number;
  matches_count: number;
  bets_count: number;
  bets: ValueBet[];
}
