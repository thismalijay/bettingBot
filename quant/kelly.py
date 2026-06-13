from dataclasses import dataclass

from quant.margin import extract_h2h_outcomes, get_true_probs


@dataclass
class ValueBet:
    match: str
    sport: str
    bookmaker: str
    outcome: str
    odds: float
    true_prob: float
    edge: float              # (true_prob * odds) - 1, ex: 0.08 = +8%
    kelly_fraction: float    # fraction du capital à miser (après Kelly fractionnaire)
    recommended_stake: float # mise recommandée en euros


def _kelly(p: float, b: float) -> float:
    """
    Critère de Kelly : f* = (b*p - q) / b
    p = probabilité réelle de gagner
    b = gain net si victoire (cote décimale - 1)
    Retourne 0 si le bet n'est pas positif (pas de value).
    """
    q = 1.0 - p
    return max(0.0, (b * p - q) / b)


def find_value_bets(
    matches: list[dict],
    sharp_books: list[str],
    min_edge: float,
    kelly_fraction: float,
    bankroll: float,
) -> list[ValueBet]:
    """
    Parcourt tous les matchs et tous les bookmakers.
    Retourne les sélections où l'edge dépasse min_edge, triées par edge décroissant.
    """
    value_bets: list[ValueBet] = []

    for match in matches:
        home = match["home_team"]
        away = match["away_team"]
        match_name = f"{home} vs {away}"
        sport = match.get("sport_key", "")

        true_probs = get_true_probs(match, sharp_books)
        if not true_probs:
            continue

        for bm in match.get("bookmakers", []):
            outcomes = extract_h2h_outcomes(bm)
            if not outcomes:
                continue

            for selection, odds in outcomes:
                true_p = true_probs.get(selection)
                if true_p is None or true_p <= 0:
                    continue

                # edge = rendement espéré net : >0 signifie que la cote est sous-évaluée
                edge = (true_p * odds) - 1.0
                if edge < min_edge:
                    continue

                b = odds - 1.0
                raw_kelly = _kelly(true_p, b)
                frac = raw_kelly * kelly_fraction
                stake = frac * bankroll

                value_bets.append(ValueBet(
                    match=match_name,
                    sport=sport,
                    bookmaker=bm.get("title", bm["key"]),
                    outcome=selection,
                    odds=odds,
                    true_prob=true_p,
                    edge=edge,
                    kelly_fraction=frac,
                    recommended_stake=stake,
                ))

    return sorted(value_bets, key=lambda x: x.edge, reverse=True)
