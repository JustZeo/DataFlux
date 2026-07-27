# Exporting Data

`export()` writes a `polars.DataFrame` to disk, inferring the format from the file extension.

```python
flux.export(df: polars.DataFrame, path: str | Path, *, overwrite: bool = False, mkdir: bool = True) -> Path
```

---

## Basic usage

```python
df = flux.pull(results[0])
flux.export(df, "iris.csv")
```

Returns the `Path` that was written to, so you can chain it into further code:

```python
path = flux.export(df, "iris.csv")
print(f"Saved to {path}")
```

## Supported formats

The format is determined entirely by the file extension — there's no separate `format=` argument to set:

| Extension | Written via |
|---|---|
| `.csv` | `df.write_csv()` |
| `.parquet` | `df.write_parquet()` |
| `.json` | `df.write_json()` |
| `.ndjson` | `df.write_ndjson()` |
| `.ipc` | `df.write_ipc()` |
| `.feather` | `df.write_ipc()` |
| `.arrow` | `df.write_ipc()` |

```python
flux.export(df, "housing.parquet")
flux.export(df, "housing.ndjson")
```

An unrecognized extension raises `UnsupportedExportFormatError`:

```python
from dataflux.exceptions import UnsupportedExportFormatError

try:
    flux.export(df, "housing.xlsx")
except UnsupportedExportFormatError as e:
    print(e)  # "Export format '.xlsx' is not supported. Supported formats: ..."
```

## Overwriting existing files

By default, `export()` refuses to overwrite a file that already exists:

```python
flux.export(df, "housing.csv")
flux.export(df, "housing.csv")  # raises ExportFileExistsError
```

Pass `overwrite=True` to replace it intentionally:

```python
flux.export(df, "housing.csv", overwrite=True)
```

## Creating parent directories

If the target path's parent directory doesn't exist, `export()` creates it automatically by default:

```python
flux.export(df, "data/processed/housing.csv")  # creates data/processed/ if needed
```

Set `mkdir=False` if you'd rather it fail when the directory doesn't already exist:

```python
flux.export(df, "data/processed/housing.csv", mkdir=False)  # raises if data/processed/ is missing
```

## Validating input

`export()` only accepts a real `polars.DataFrame` — passing anything else (a pandas DataFrame, a list, a dict) raises `InvalidExportDataError`:

```python
from dataflux.exceptions import InvalidExportDataError

try:
    flux.export([1, 2, 3], "not-a-dataframe.csv")
except InvalidExportDataError as e:
    print(e)  # "export() expects a Polars DataFrame."
```

If you have a pandas DataFrame and need to export it, convert it first:

```python
import polars as pl

flux.export(pl.from_pandas(pandas_df), "output.csv")
```

## Next step

[:octicons-arrow-right-24: Caching](caching.md) — what's cached automatically today, and what to expect as caching support expands across providers.