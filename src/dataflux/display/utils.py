from __future__ import annotations

from collections.abc import Mapping, Sequence
from textwrap import fill, shorten


# ============================================================================
# Constants
# ============================================================================

DESCRIPTION_LIMIT = 600
DESCRIPTION_WIDTH = 60


# ============================================================================
# Text Formatting
# ============================================================================

def truncate_description(
    text: str | None,
    *,
    limit: int = DESCRIPTION_LIMIT,
    width: int = 80,
) -> str | None:
    """
    Truncate long descriptions for panels.
    """

    if not text:
        return None

    text = " ".join(text.split())

    if len(text) <= limit:
        return fill(text, width=width)

    return (
        fill(text[:limit].rsplit(" ", 1)[0], width=width)
        + "\n\n[dim]... (description truncated)[/dim]"
    )


def truncate_text(
    text: str | None,
    *,
    width: int = DESCRIPTION_WIDTH,
) -> str:
    """
    Truncate text for table cells.
    """

    if not text:
        return "-"

    return shorten(
        " ".join(text.split()),
        width=width,
        placeholder="...",
    )


# ============================================================================
# Value Formatting
# ============================================================================

def format_value(value):
    """
    Pretty-format common Python objects for Rich.
    """

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


def add_row(table, label: str, value) -> None:
    """
    Add a row to a Rich table while skipping empty values.
    """

    value = format_value(value)

    if value is None:
        return

    table.add_row(label, value)


# ============================================================================
# Provider Display Names
# ============================================================================

_PROVIDER_NAMES = {
    "uci": "UCI Machine Learning Repository",
    "sklearn": "Scikit-Learn",
    "huggingface": "Hugging Face",
    "kaggle": "Kaggle",
    "torchvision": "TorchVision",
    "pyg": "PyTorch Geometric",
    "seaborn": "Seaborn",
    "statsmodels": "StatsModels",
    "vega": "Vega Datasets",
    "worldbank": "World Bank",
}


def provider_name(provider: str) -> str:
    """
    Convert an internal provider identifier into a display name.

    Examples
    --------
    >>> provider_name("sklearn")
    'Scikit-Learn'
    """
    return _PROVIDER_NAMES.get(provider.lower(), provider.title())