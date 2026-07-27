import pytest
import polars as pl

from dataflux import flux
from dataflux.exceptions import (
    ExportFileExistsError,
    InvalidExportDataError,
    UnsupportedExportFormatError,
)


@pytest.fixture
def df():
    return pl.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "score": [90, 85, 95],
        }
    )


# ============================================================================
# CSV
# ============================================================================

def test_export_csv(df, tmp_path):
    path = tmp_path / "data.csv"

    exported = flux.export(df, path)

    assert path.exists()
    assert exported == path


# ============================================================================
# Parquet
# ============================================================================

def test_export_parquet(df, tmp_path):
    path = tmp_path / "data.parquet"

    flux.export(df, path)

    assert path.exists()


# ============================================================================
# JSON
# ============================================================================

def test_export_json(df, tmp_path):
    path = tmp_path / "data.json"

    flux.export(df, path)

    assert path.exists()


# ============================================================================
# IPC
# ============================================================================

def test_export_ipc(df, tmp_path):
    path = tmp_path / "data.ipc"

    flux.export(df, path)

    assert path.exists()


# ============================================================================
# Feather
# ============================================================================

def test_export_feather(df, tmp_path):
    path = tmp_path / "data.feather"

    flux.export(df, path)

    assert path.exists()


# ============================================================================
# Arrow
# ============================================================================

def test_export_arrow(df, tmp_path):
    path = tmp_path / "data.arrow"

    flux.export(df, path)

    assert path.exists()


# ============================================================================
# Overwrite
# ============================================================================

def test_overwrite(df, tmp_path):
    path = tmp_path / "data.csv"

    flux.export(df, path)

    flux.export(
        df,
        path,
        overwrite=True,
    )

    assert path.exists()


# ============================================================================
# Existing File
# ============================================================================

def test_existing_file(df, tmp_path):
    path = tmp_path / "data.csv"

    flux.export(df, path)

    with pytest.raises(ExportFileExistsError):
        flux.export(df, path)


# ============================================================================
# Unsupported Format
# ============================================================================

def test_invalid_extension(df, tmp_path):
    path = tmp_path / "data.xyz"

    with pytest.raises(UnsupportedExportFormatError):
        flux.export(df, path)


# ============================================================================
# Invalid Object
# ============================================================================

def test_invalid_dataframe(tmp_path):
    path = tmp_path / "data.csv"

    with pytest.raises(InvalidExportDataError):
        flux.export([1, 2, 3], path)