import asyncio
from typing import Any

import httpx

from config import ODDS_API_KEY, SPORTS, REGIONS, MARKETS

BASE_URL = "https://api.the-odds-api.com/v4"

# Données de démonstration — reproduit le format exact de The Odds API
DEMO_DATA: list[dict[str, Any]] = [
    {
        "id": "demo_1",
        "sport_key": "soccer_france_ligue1",
        "commence_time": "2026-06-14T20:00:00Z",
        "home_team": "Paris Saint-Germain",
        "away_team": "Olympique de Marseille",
        "bookmakers": [
            {
                "key": "pinnacle",
                "title": "Pinnacle",
                "markets": [{"key": "h2h", "outcomes": [
                    {"name": "Paris Saint-Germain", "price": 1.72},
                    {"name": "Olympique de Marseille", "price": 4.80},
                    {"name": "Draw", "price": 3.60},
                ]}],
            },
            {
                "key": "bet365",
                "title": "Bet365",
                "markets": [{"key": "h2h", "outcomes": [
                    {"name": "Paris Saint-Germain", "price": 1.65},
                    {"name": "Olympique de Marseille", "price": 4.50},
                    {"name": "Draw", "price": 3.40},
                ]}],
            },
            {
                "key": "winamax",
                "title": "Winamax",
                "markets": [{"key": "h2h", "outcomes": [
                    {"name": "Paris Saint-Germain", "price": 1.68},
                    {"name": "Olympique de Marseille", "price": 5.60},  # Value : true odds ~5.12, edge ~9.4%
                    {"name": "Draw", "price": 3.50},
                ]}],
            },
        ],
    },
    {
        "id": "demo_2",
        "sport_key": "soccer_england_premier_league",
        "commence_time": "2026-06-15T15:00:00Z",
        "home_team": "Arsenal",
        "away_team": "Manchester City",
        "bookmakers": [
            {
                "key": "pinnacle",
                "title": "Pinnacle",
                "markets": [{"key": "h2h", "outcomes": [
                    {"name": "Arsenal", "price": 2.95},
                    {"name": "Manchester City", "price": 2.40},
                    {"name": "Draw", "price": 3.30},
                ]}],
            },
            {
                "key": "bet365",
                "title": "Bet365",
                "markets": [{"key": "h2h", "outcomes": [
                    {"name": "Arsenal", "price": 2.80},
                    {"name": "Manchester City", "price": 2.50},
                    {"name": "Draw", "price": 3.20},
                ]}],
            },
            {
                "key": "unibet",
                "title": "Unibet",
                "markets": [{"key": "h2h", "outcomes": [
                    {"name": "Arsenal", "price": 3.30},  # Value : true odds ~3.12, edge ~5.8%
                    {"name": "Manchester City", "price": 2.35},
                    {"name": "Draw", "price": 3.70},  # Value : true odds ~3.49, edge ~6%
                ]}],
            },
        ],
    },
    {
        "id": "demo_3",
        "sport_key": "soccer_spain_la_liga",
        "commence_time": "2026-06-15T18:00:00Z",
        "home_team": "Real Madrid",
        "away_team": "FC Barcelona",
        "bookmakers": [
            {
                "key": "pinnacle",
                "title": "Pinnacle",
                "markets": [{"key": "h2h", "outcomes": [
                    {"name": "Real Madrid", "price": 2.10},
                    {"name": "FC Barcelona", "price": 3.45},
                    {"name": "Draw", "price": 3.20},
                ]}],
            },
            {
                "key": "betclic",
                "title": "Betclic",
                "markets": [{"key": "h2h", "outcomes": [
                    {"name": "Real Madrid", "price": 2.05},
                    {"name": "FC Barcelona", "price": 3.30},
                    {"name": "Draw", "price": 3.10},
                ]}],
            },
        ],
    },
]


async def _fetch_sport_odds(sport: str, client: httpx.AsyncClient) -> list[dict[str, Any]]:
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": "decimal",
    }
    response = await client.get(f"{BASE_URL}/sports/{sport}/odds/", params=params)
    response.raise_for_status()
    return response.json()


async def collect_all_odds(demo: bool = False) -> list[dict[str, Any]]:
    if demo:
        return DEMO_DATA

    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [_fetch_sport_odds(sport, client) for sport in SPORTS]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    all_odds: list[dict[str, Any]] = []
    for result in results:
        if isinstance(result, Exception):
            print(f"[WARNING] Erreur API: {result}")
        else:
            all_odds.extend(result)  # type: ignore[arg-type]

    return all_odds
