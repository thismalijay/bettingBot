import asyncio
import sys

# Force UTF-8 pour les noms d'équipes avec accents / caractères spéciaux
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import config
from ingestion.odds_collector import collect_all_odds
from quant.kelly import ValueBet, find_value_bets

console = Console()

SPORT_LABELS = {
    "soccer_france_ligue1": "Ligue 1",
    "soccer_england_premier_league": "Premier League",
    "soccer_spain_la_liga": "La Liga",
    "soccer_uefa_champs_league": "Champions League",
}


def _sport_label(key: str) -> str:
    return SPORT_LABELS.get(key, key.replace("soccer_", "").replace("_", " ").title())


def print_banner(demo: bool) -> None:
    mode = "[yellow bold]DEMO[/yellow bold]" if demo else "[green bold]LIVE[/green bold]"
    console.print(Panel(
        f"[bold cyan]Bot Paris Sportif - Value Bet Finder[/bold cyan]\n"
        f"Bankroll: [bold]{config.BANKROLL:.0f} EUR[/bold]  |  "
        f"Kelly: [bold]{config.KELLY_FRACTION * 100:.0f}%[/bold]  |  "
        f"Edge min: [bold]{config.MIN_EDGE * 100:.0f}%[/bold]  |  "
        f"Mode: {mode}",
        border_style="cyan",
        padding=(0, 2),
    ))


def print_value_bets(value_bets: list[ValueBet]) -> None:
    if not value_bets:
        console.print("\n[yellow]Aucune value bet détectée avec les critères actuels.[/yellow]")
        console.print("[dim]Essayez de baisser MIN_EDGE dans .env (ex: 0.02)[/dim]")
        return

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta", padding=(0, 1))
    table.add_column("Match", style="white", min_width=28)
    table.add_column("Compétition", style="dim", min_width=16)
    table.add_column("Book", style="cyan", min_width=10)
    table.add_column("Sélection", style="white bold", min_width=22)
    table.add_column("Cote", justify="right", style="yellow")
    table.add_column("Prob réelle", justify="right")
    table.add_column("Edge", justify="right")
    table.add_column("Kelly", justify="right", style="dim")
    table.add_column("Mise (EUR)", justify="right", style="bold green")

    for vb in value_bets:
        edge_pct = vb.edge * 100
        edge_color = "green" if edge_pct >= 5 else "yellow"
        table.add_row(
            vb.match,
            _sport_label(vb.sport),
            vb.bookmaker,
            vb.outcome,
            f"{vb.odds:.2f}",
            f"{vb.true_prob * 100:.1f}%",
            f"[{edge_color}]+{edge_pct:.1f}%[/{edge_color}]",
            f"{vb.kelly_fraction * 100:.1f}%",
            f"{vb.recommended_stake:.0f}",
        )

    count = len(value_bets)
    console.print(f"\n[bold]{count} value bet{'s' if count > 1 else ''} détectée{'s' if count > 1 else ''}[/bold]\n")
    console.print(table)
    console.print(
        "\n[dim]True odds : Pinnacle (si dispo dans la reponse API) -> consensus bookmakers sinon.[/dim]"
    )


async def main() -> None:
    demo = config.DEMO_MODE
    print_banner(demo)

    if demo:
        console.print("[dim]Mode démo — ajoutez ODDS_API_KEY dans .env pour les cotes réelles.[/dim]\n")

    console.print("Récupération des cotes...", end=" ")
    matches = await collect_all_odds(demo=demo)
    console.print(f"[green]{len(matches)} match(s) chargé(s)[/green]")

    value_bets = find_value_bets(
        matches=matches,
        sharp_books=config.SHARP_BOOKS,
        min_edge=config.MIN_EDGE,
        kelly_fraction=config.KELLY_FRACTION,
        bankroll=config.BANKROLL,
    )

    print_value_bets(value_bets)


if __name__ == "__main__":
    asyncio.run(main())
