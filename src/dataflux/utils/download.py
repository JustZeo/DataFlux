from __future__ import annotations

import json
import shutil
import urllib.request
from pathlib import Path
from typing import Any

from dataflux.utils.filesystem import ensure_dir


CHUNK_SIZE = 8192
DEFAULT_TIMEOUT = 30


# ============================================================================
# Core Downloads
# ============================================================================

def download(
    url: str,
    destination: str | Path,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> Path:
    """
    Download a file.

    Returns
    -------
    Path
        Downloaded file.
    """
    destination = Path(destination)
    ensure_dir(destination.parent)

    with (
        urllib.request.urlopen(url, timeout=timeout) as response,
        open(destination, "wb") as f,
    ):
        shutil.copyfileobj(response, f, CHUNK_SIZE)

    return destination


def download_bytes(
    url: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> bytes:
    """
    Download raw bytes.
    """
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read()


def download_text(
    url: str,
    *,
    encoding: str = "utf-8",
    timeout: int = DEFAULT_TIMEOUT,
) -> str:
    """
    Download text.
    """
    return download_bytes(
        url,
        timeout=timeout,
    ).decode(encoding)


def download_json(
    url: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> Any:
    """
    Download JSON.
    """
    return json.loads(
        download_text(
            url,
            timeout=timeout,
        )
    )


# ============================================================================
# Helpers
# ============================================================================

def exists(path: str | Path) -> bool:
    """
    Check whether a downloaded file exists.
    """
    return Path(path).exists()


def remove(path: str | Path) -> bool:
    """
    Delete a downloaded file.
    """
    path = Path(path)

    if not path.exists():
        return False

    path.unlink()
    return True