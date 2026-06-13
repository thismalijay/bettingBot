import os
from dotenv import load_dotenv

load_dotenv()

ODDS_API_KEY: str = os.getenv("ODDS_API_KEY", "")
BANKROLL: float = float(os.getenv("BANKROLL", "1000"))
KELLY_FRACTION: float = float(os.getenv("KELLY_FRACTION", "0.5"))  # Demi-Kelly par défaut
MIN_EDGE: float = float(os.getenv("MIN_EDGE", "0.03"))             # Edge minimum 3%

SPORTS: list[str] = [
    # Football — sports actifs en juin 2026
    "soccer_fifa_world_cup",              # Coupe du Monde 2026 (en cours !)
    "soccer_conmebol_copa_libertadores",  # Copa Libertadores
    "soccer_conmebol_copa_sudamericana",  # Copa Sudamericana
    "soccer_norway_eliteserien",          # Eliteserien Norvège
    "soccer_sweden_allsvenskan",          # Allsvenskan Suède
    # Basket
    "basketball_nba",
    # Tennis
    "tennis_wta_queens_club_champ",
]

REGIONS: str = "eu"
MARKETS: str = "h2h"

# Pinnacle est la référence "sharp" — ses cotes reflètent les vraies probabilités de marché
SHARP_BOOKS: list[str] = ["pinnacle"]

DEMO_MODE: bool = not bool(ODDS_API_KEY)
