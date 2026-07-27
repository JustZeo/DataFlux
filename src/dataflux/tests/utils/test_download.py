from pathlib import Path
from unittest.mock import MagicMock, patch

from dataflux.utils.download import (
    DEFAULT_TIMEOUT,
    download,
    download_bytes,
    download_json,
    download_text,
    exists,
    remove,
)


# ============================================================================
# download()
# ============================================================================

@patch("urllib.request.urlopen")
def test_download(mock_urlopen, tmp_path):
    data = b"Hello DataFlux"

    response = MagicMock()
    response.__enter__.return_value.read.return_value = data
    response.__enter__.return_value = response.__enter__.return_value

    mock_urlopen.return_value = response

    destination = tmp_path / "test.bin"

    # Patch shutil.copyfileobj indirectly by making response behave like a file
    response.__enter__.return_value.read = MagicMock(
        side_effect=[data, b""]
    )

    path = download(
        "https://example.com/file.bin",
        destination,
    )

    assert path.exists()
    assert path == destination


# ============================================================================
# download_bytes()
# ============================================================================

@patch("urllib.request.urlopen")
def test_download_bytes(mock_urlopen):
    response = MagicMock()
    response.__enter__.return_value.read.return_value = b"hello"

    mock_urlopen.return_value = response

    data = download_bytes("https://example.com")

    assert data == b"hello"


# ============================================================================
# download_text()
# ============================================================================

@patch("urllib.request.urlopen")
def test_download_text(mock_urlopen):
    response = MagicMock()
    response.__enter__.return_value.read.return_value = (
        b"Hello DataFlux"
    )

    mock_urlopen.return_value = response

    text = download_text("https://example.com")

    assert text == "Hello DataFlux"


# ============================================================================
# download_json()
# ============================================================================

@patch("urllib.request.urlopen")
def test_download_json(mock_urlopen):
    response = MagicMock()
    response.__enter__.return_value.read.return_value = (
        b'{"rows":150}'
    )

    mock_urlopen.return_value = response

    data = download_json("https://example.com")

    assert data["rows"] == 150


# ============================================================================
# Exists
# ============================================================================

def test_exists(tmp_path):
    file = tmp_path / "iris.csv"

    file.write_text("hello")

    assert exists(file)


def test_not_exists(tmp_path):
    assert not exists(tmp_path / "missing.csv")


# ============================================================================
# Remove
# ============================================================================

def test_remove(tmp_path):
    file = tmp_path / "iris.csv"

    file.write_text("hello")

    assert remove(file)
    assert not file.exists()


def test_remove_missing():
    assert remove("missing.csv") is False


# ============================================================================
# Constants
# ============================================================================

def test_default_timeout():
    assert DEFAULT_TIMEOUT == 30