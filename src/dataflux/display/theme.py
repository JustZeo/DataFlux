from rich.theme import Theme

DATAFLUX_THEME = Theme(
    {
        # General
        "header": "bold cyan",
        "title": "bold bright_cyan",
        "subtitle": "dim cyan",

        # Tables
        "label": "bold cyan",
        "value": "white",

        # Status
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "info": "cyan",

        # Panels
        "panel": "cyan",
        "description": "green",
        "extra": "yellow",

        # Search
        "provider": "magenta",
        "highlight": "bold bright_green",

        # Misc
        "dim": "dim",
    }
)