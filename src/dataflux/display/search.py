from textwrap import shorten

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from dataflux.display.console import console


DESCRIPTION_WIDTH = 60


def _truncate(text: str | None) -> str:
    """Truncate long descriptions cleanly."""
    if not text:
        return "-"

    return shorten(
        " ".join(text.split()),
        width=DESCRIPTION_WIDTH,
        placeholder="...",
    )


def display_search(results: list, limit: int = 10) -> None:
    """
    Pretty-print search results using Rich.
    """

    if not results:
        console.print(
            Panel(
                "[error]No datasets found.[/error]",
                title="[header]Search Results[/header]",
                border_style="error",
            )
        )
        return

    # -------------------------------------------------------------------------
    # Single Result
    # -------------------------------------------------------------------------

    if len(results) == 1:
        result = results[0]

        text = Text()

        text.append("Name: ", style="label")
        text.append(f"{result.name}\n", style="value")

        text.append("Provider: ", style="label")
        text.append(f"{result.provider}\n", style="provider")

        text.append("ID: ", style="label")
        text.append(f"{result.id}\n", style="value")

        if result.description:
            text.append("Description: ", style="label")
            text.append(result.description, style="value")

        if getattr(result, "match_score", None) is not None:
            text.append("\nMatch Score: ", style="label")
            text.append(
                f"{result.match_score:.2f}",
                style="highlight",
            )

        console.print(
            Panel(
                text,
                title="[header]Search Result[/header]",
                border_style="panel",
            )
        )
        return

    # -------------------------------------------------------------------------
    # Multiple Results
    # -------------------------------------------------------------------------

    display_results = results[:limit]

    table = Table(
        title=f"[header]Search Results ({len(display_results)} of {len(results)})[/header]",
        show_lines=False,
        expand=True,
    )

    table.add_column("#", justify="right", style="label", no_wrap=True)
    table.add_column("Name", style="title")
    table.add_column("Provider", style="provider")
    table.add_column("ID", style="value")
    table.add_column("Description", style="dim")

    # Uncomment later if match_score becomes public.
    # table.add_column("Score", justify="right", style="highlight")

    for index, result in enumerate(display_results, start=1):
        table.add_row(
            str(index),
            result.name,
            result.provider,
            str(result.id),
            _truncate(result.description),
            # f"{result.match_score:.2f}" if result.match_score else "-",
        )

    console.print(table)

    # -------------------------------------------------------------------------
    # Footer
    # -------------------------------------------------------------------------

    if len(results) > limit:
        console.print(
            f"[dim]Showing {len(display_results)} of {len(results)} matching datasets.[/dim]"
        )
        console.print(
            "[dim]Use [bold]limit=...[/bold] to display more results or "
            "[bold]display=False[/bold] to suppress console output.[/dim]"
        )