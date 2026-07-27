from collections.abc import Mapping, Sequence
from textwrap import fill

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from dataflux.display.console import console
from dataflux.models.dataset import DatasetInfo


DESCRIPTION_LIMIT = 600


def _truncate(text: str | None) -> str | None:
    """Truncate long descriptions for prettier display."""
    if not text:
        return None

    text = " ".join(text.split())

    if len(text) <= DESCRIPTION_LIMIT:
        return fill(text, width=80)

    return (
        fill(text[:DESCRIPTION_LIMIT].rsplit(" ", 1)[0], width=80)
        + "\n\n[dim]... (description truncated)[/dim]"
    )


def _format(value):
    """Pretty-format common Python objects."""

    if value is None:
        return None

    if isinstance(value, bool):
        return "[success]Yes[/success]" if value else "[error]No[/error]"

    if isinstance(value, Mapping):
        return "\n".join(
            f"• {k}: {v}"
            for k, v in value.items()
        )

    if (
        isinstance(value, Sequence)
        and not isinstance(value, (str, bytes))
    ):
        if len(value) == 0:
            return None

        return "\n".join(
            f"• {item}"
            for item in value
        )

    return str(value)


def _add_row(table: Table, label: str, value) -> None:
    """Skip empty values automatically."""

    value = _format(value)

    if value is None:
        return

    table.add_row(label, value)


def display_info(info: DatasetInfo) -> None:
    """Pretty-print DatasetInfo."""

    # -------------------------------------------------------------------------
    # Header
    # -------------------------------------------------------------------------

    console.print(
        Panel.fit(
            Text(info.name, style="title"),
            subtitle=f"[subtitle]{info.provider} • {info.id}[/subtitle]",
            border_style="panel",
        )
    )

    # -------------------------------------------------------------------------
    # General Information
    # -------------------------------------------------------------------------

    table = Table(
        title="[header]General Information[/header]",
        show_header=False,
        expand=True,
        box=None,
    )

    table.add_column(style="label", width=20)
    table.add_column(style="value")

    _add_row(table, "Provider", info.provider)
    _add_row(table, "Dataset ID", info.id)
    _add_row(table, "Instances", info.instances)
    _add_row(table, "Features", info.features)
    _add_row(table, "Tasks", info.tasks)
    _add_row(table, "Target", info.target)
    _add_row(table, "Missing Values", info.has_missing_values)
    _add_row(table, "URL", info.url)

    console.print(table)

    # -------------------------------------------------------------------------
    # Description
    # -------------------------------------------------------------------------

    description = _truncate(info.description)

    if description:
        console.print(
            Panel(
                description,
                title="[description]Description[/description]",
                border_style="description",
            )
        )

    # -------------------------------------------------------------------------
    # Additional Information
    # -------------------------------------------------------------------------

    if info.extra:

        extra = Table(
            title="[header]Additional Information[/header]",
            show_header=False,
            expand=True,
            box=None,
        )

        extra.add_column(style="warning", width=25)
        extra.add_column(style="value")

        for key, value in info.extra.items():
            _add_row(
                extra,
                key.replace("_", " ").title(),
                value,
            )

        console.print(extra)