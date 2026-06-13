import os
from dotenv import load_dotenv

load_dotenv()

ODDS_API_KEY: str = os.getenv("ODDS_API_KEY", "")
BANKROLL: float = float(os.getenv("BANKROLL", "1000"))
KELLY_FRACTION: float = float(os.getenv("KELLY_FRACTION", "0.5"))  # Demi-Kelly par défaut
MIN_EDGE: float = float(os.getenv("MIN_EDGE", "0.03"))             # Edge minimum 3%

SPORTS: list[str] = [
    "soccer_france_ligue1",
    "soccer_england_premier_league",
    "soccer_spain_la_liga",
    "soccer_uefa_champs_league",
]

REGIONS: str = "eu"
MARKETS: str = "h2h"

# Pinnacle est la référence "sharp" — ses cotes reflètent les vraies probabilités de marché
SHARP_BOOKS: list[str] = ["pinnacle"]

DEMO_MODE: bool = not bool(ODDS_API_KEY)
