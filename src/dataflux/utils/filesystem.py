from pathlib import Path


# ============================================================================
# Base Directories
# ============================================================================

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = PACKAGE_ROOT.parent.parent

CACHE_DIR = Path.home() / ".cache" / "dataflux"
TEMP_DIR = CACHE_DIR / "temp"
RESOURCE_DIR = PACKAGE_ROOT / "resources"


# ============================================================================
# Path Helpers
# ============================================================================

def package_root() -> Path:
    """Return the root directory of the dataflux package."""
    return PACKAGE_ROOT


def project_root() -> Path:
    """Return the root directory of the project."""
    return PROJECT_ROOT


def resource_path(*parts: str) -> Path:
    """
    Return a path inside the resources directory.

    Example
    -------
    >>> resource_path("kaggle_index.json")
    """
    return RESOURCE_DIR.joinpath(*parts)


def cache_path(*parts: str) -> Path:
    """
    Return a path inside the DataFlux cache directory.

    Example
    -------
    >>> cache_path("torchvision")
    """
    return CACHE_DIR.joinpath(*parts)


def temp_path(*parts: str) -> Path:
    """
    Return a path inside the temporary directory.

    Example
    -------
    >>> temp_path("downloads")
    """
    return TEMP_DIR.joinpath(*parts)


# ============================================================================
# Filesystem Helpers
# ============================================================================

def ensure_dir(path: str | Path) -> Path:
    """
    Create a directory if it doesn't exist.

    Returns
    -------
    Path
        The created/existing directory.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def expand(path: str | Path) -> Path:
    """
    Expand '~' and return an absolute Path.

    Example
    -------
    >>> expand("~/datasets")
    """
    return Path(path).expanduser().resolve()