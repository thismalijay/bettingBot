from typing import Optional


def overround(odds_list: list[float]) -> float:
    """Marge totale du bookmaker (ex: 0.05 = 5% de marge)."""
    return sum(1.0 / o for o in odds_list) - 1.0


def true_probs_multiplicative(odds_list: list[float]) -> list[float]:
    """
    Supprime la marge par méthode multiplicative (la plus utilisée).
    Chaque prob implicite est divisée par la somme totale pour qu'elles
    s'additionnent à 1.
    """
    raw = [1.0 / o for o in odds_list]
    total = sum(raw)
    return [p / total for p in raw]


def extract_h2h_outcomes(bookmaker: dict) -> Optional[list[tuple[str, float]]]:
    """Retourne [(selection, cote), ...] pour le marché h2h, ou None."""
    for market in bookmaker.get("markets", []):
        if market["key"] == "h2h":
            return [(o["name"], o["price"]) for o in market["outcomes"]]
    return None


def get_true_probs(match: dict, sharp_books: list[str]) -> Optional[dict[str, float]]:
    """
    Probabilités "réelles" du match.

    Priorité 1 : cotes Pinnacle (ou autre sharp book) après suppression de marge.
    Priorité 2 : moyenne des probabilités corrigées de tous les books disponibles.
    """
    for bm in match.get("bookmakers", []):
        if bm["key"] in sharp_books:
            outcomes = extract_h2h_outcomes(bm)
            if outcomes:
                names = [o[0] for o in outcomes]
                odds = [o[1] for o in outcomes]
                probs = true_probs_multiplicative(odds)
                return dict(zip(names, probs))

    # Fallback consensus : moyenne des probs corrigées de tous les books
    aggregated: dict[str, list[float]] = {}
    for bm in match.get("bookmakers", []):
        outcomes = extract_h2h_outcomes(bm)
        if not outcomes:
            continue
        names = [o[0] for o in outcomes]
        odds = [o[1] for o in outcomes]
        corrected = true_probs_multiplicative(odds)
        for name, prob in zip(names, corrected):
            aggregated.setdefault(name, []).append(prob)

    if not aggregated:
        return None

    return {name: sum(ps) / len(ps) for name, ps in aggregated.items()}
