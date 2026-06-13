import sys
import os
from datetime import datetime, timezone

# Permet d'importer config, ingestion, quant depuis le dossier parent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from ingestion.odds_collector import collect_all_odds
from quant.kelly import find_value_bets

app = FastAPI(title="Bot Paris Sportif API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

SPORT_LABELS = {
    "soccer_fifa_world_cup": "FIFA World Cup",
    "soccer_conmebol_copa_libertadores": "Copa Libertadores",
    "soccer_conmebol_copa_sudamericana": "Copa Sudamericana",
    "soccer_norway_eliteserien": "Eliteserien",
    "soccer_sweden_allsvenskan": "Allsvenskan",
    "basketball_nba": "NBA",
    "tennis_wta_queens_club_champ": "WTA Queen's Club",
}


@app.get("/api/health")
async def health():
    return {"status": "ok", "mode": "demo" if config.DEMO_MODE else "live"}


@app.get("/api/value-bets")
async def get_value_bets():
    matches = await collect_all_odds(demo=config.DEMO_MODE)

    bets = find_value_bets(
        matches=matches,
        sharp_books=config.SHARP_BOOKS,
        min_edge=config.MIN_EDGE,
        kelly_fraction=config.KELLY_FRACTION,
        bankroll=config.BANKROLL,
    )

    return {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "demo" if config.DEMO_MODE else "live",
        "bankroll": config.BANKROLL,
        "kelly_fraction": config.KELLY_FRACTION,
        "min_edge": config.MIN_EDGE,
        "matches_count": len(matches),
        "bets_count": len(bets),
        "bets": [
            {
                "match": b.match,
                "sport_key": b.sport,
                "sport_label": SPORT_LABELS.get(b.sport, b.sport.replace("_", " ").title()),
                "bookmaker": b.bookmaker,
                "outcome": b.outcome,
                "odds": round(b.odds, 2),
                "true_prob": round(b.true_prob, 4),
                "edge": round(b.edge, 4),
                "edge_pct": round(b.edge * 100, 2),
                "kelly_fraction": round(b.kelly_fraction, 4),
                "kelly_pct": round(b.kelly_fraction * 100, 2),
                "recommended_stake": round(b.recommended_stake, 2),
            }
            for b in bets
        ],
    }
