from __future__ import annotations
from pathlib import Path
import polars as pl
from dataflux.exceptions import ExportFileExistsError,UnsupportedExportFormatError,InvalidExportDataError
SUPPORTED_EXPORTS = {
    ".csv",
    ".parquet",
    ".json",
    ".ndjson",
    ".ipc",
    ".feather",
    ".arrow",
}


def export(df:pl.DataFrame,path:str | Path,*,overwrite:bool = False,mkdir:bool=True,)->Path:
    if not isinstance(df,pl.DataFrame):
        raise InvalidExportDataError(
            "export() expect a Polars DataFrame"
        )
    path = Path(path)

    if mkdir:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
    if path.exists() and not overwrite:
        raise ExportFileExistsError(
            f"'{path}' already exists."
        )

    suffix = path.suffix.lower()

    if suffix not in SUPPORTED_EXPORTS:
        raise UnsupportedExportFormatError(
            f"Unsupported export format '{suffix}'. "
            f"Supported formats:{', '.join(sorted(SUPPORTED_EXPORTS))} "
        )
    match suffix:
        case ".csv":
            df.write_csv(path)

        case ".parquet":
            df.write_parquet(path)

        case ".json":
            df.write_json(path)

        case ".ndjson":
            df.write_ndjson(path)

        case ".ipc":
            df.write_ipc(path)

        case ".feather":
            df.write_ipc(path)

        case ".arrow":
            df.write_ipc(path)

    return path