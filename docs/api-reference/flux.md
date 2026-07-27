# `flux`

`flux` is the single entry point for DataFlux. It's a ready-to-use instance of the `Flux` class, pre-loaded with all nine built-in providers — you import it directly rather than constructing `Flux` yourself.

```python
from dataflux import flux
```

---

## `Flux`

```python
class Flux
```

Wires up a `ProviderRegistry` with every built-in provider and exposes the four core operations: `search`, `info`, `pull`, and `export`.

```python
def __init__(self)
```

Registers all nine built-in providers (scikit-learn, UCI, Kaggle, Hugging Face, TorchVision, Seaborn, Statsmodels, Vega, World Bank) against an internal `ProviderRegistry`. You won't normally instantiate `Flux` yourself — use the pre-built `flux` singleton instead.

---

### `search`

```python
def search(
    self,
    query: str,
    *,
    raw: bool = False,
    display: bool = True,
    limit: int | None = 10,
) -> list[SearchResult]
```

Searches every registered provider for `query` and returns matches ranked across all of them. See [Searching](../guide/searching.md) for how ranking works.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | — | Search term, matched against each provider's dataset names (and descriptions, where available). |
| `raw` | `bool` | `False` | If `True`, suppresses the console table even if `display=True`. |
| `display` | `bool` | `True` | If `True` and `raw` is `False`, prints a formatted results table to the console. |
| `limit` | `int \| None` | `10` | Maximum number of rows shown in the printed table. Does not truncate the returned list — pass `None` to show every result. |

**Returns**

`list[SearchResult]` — every match, across every provider, ranked best-first. Raises `DatasetNotFoundError` if nothing matches — see [Exceptions](exceptions.md).

**Example**

```python
results = flux.search("housing")
results = flux.search("housing", display=False)  # no console output
```

---

### `info`

```python
def info(
    self,
    result: SearchResult,
    *,
    raw: bool = False,
    display: bool = True,
) -> DatasetInfo
```

Fetches metadata for a specific search result, without downloading the dataset itself.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `result` | `SearchResult` | — | A result previously returned by `search()`. Its `.provider` and `.id` determine what gets looked up. |
| `raw` | `bool` | `False` | If `True`, suppresses the formatted console output even if `display=True`. |
| `display` | `bool` | `True` | If `True` and `raw` is `False`, prints a formatted info panel to the console. |

**Returns**

`DatasetInfo` — see [Models](models.md) for the field-by-field shape and which fields each provider populates.

**Example**

```python
result = flux.search("iris", display=False)[0]
info = flux.info(result)
```

!!! note "Fetches twice when displaying"
    `info()` currently calls the provider's `info(dataset_id)` twice when `display=True` — once to render the panel, once for the returned value. This mostly matters for providers that hit a live network endpoint on every call.

---

### `pull`

```python
def pull(self, result: SearchResult) -> pl.DataFrame
```

Downloads the dataset behind `result` and loads it into memory.

**Parameters**

| Name | Type | Description |
|---|---|---|
| `result` | `SearchResult` | A result previously returned by `search()`. |

**Returns**

`polars.DataFrame` — always, regardless of which provider the data came from. See [Pulling Datasets](../guide/pulling-datasets.md).

**Example**

```python
result = flux.search("iris", display=False)[0]
df = flux.pull(result)
```

---

### `export`

```python
def export(
    self,
    df: pl.DataFrame,
    path: str,
    **kwargs,
) -> Path
```

Writes a `polars.DataFrame` to disk. Thin wrapper around the module-level `export()` function — see [Exporting Data](../guide/exporting-data.md) for supported formats and keyword arguments (`overwrite`, `mkdir`).

**Parameters**

| Name | Type | Description |
|---|---|---|
| `df` | `pl.DataFrame` | The DataFrame to write. Must be a Polars DataFrame — pandas is not accepted. |
| `path` | `str` | Destination path. The file extension determines the output format. |
| `**kwargs` | — | Forwarded to `export()` — e.g. `overwrite=True`. |

**Returns**

`Path` — the path that was written.

**Example**

```python
df = flux.pull(result)
flux.export(df, "iris.csv")
flux.export(df, "iris.parquet", overwrite=True)
```

---

## Next step

See [Models](models.md) for the shape of `SearchResult` and `DatasetInfo`, or [Exceptions](exceptions.md) for everything these methods can raise.
