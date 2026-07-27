# Core Concepts

DataFlux is built around four verbs and two data shapes. Once these click, you know the entire public API — everything else in these docs is detail on top of this foundation.

```
search()  →  list[SearchResult]
info()    →  DatasetInfo
pull()    →  polars.DataFrame
export()  →  writes a DataFrame to disk
```

---

## The four verbs

### `search(query, *, raw=False, display=True, limit=10)`

Fans a query out to every registered provider at once, merges the results, ranks them, and returns a `list[SearchResult]`.

```python
results = flux.search("housing")
```

- **`display`** (default `True`) — prints a formatted table to the console as a side effect. The return value is identical either way.
- **`raw`** (default `False`) — when `True`, skips the pretty output entirely, regardless of `display`.
- **`limit`** (default `10`) — caps how many rows appear in the *printed* table. The full ranked result list is still returned in full; only the visual table is capped.

!!! tip "`display` vs `raw` — they're not the same knob"
    `raw` controls what shape of thing you get back conceptually; `display` controls whether anything gets printed. In practice today, both default to producing a pretty side effect, and setting either to disable it will stop the table from printing — but think of them as two independent questions: *"do I want this printed?"* (`display`) and *"do I want it printed as a pretty table at all, ever?"* (`raw`).

If nothing matches across **any** provider, `search()` raises `DatasetNotFoundError` rather than returning an empty list — see [Error Handling](../guide/error-handling.md).

### `info(result, *, raw=False, display=True)`

Takes a single `SearchResult` and returns a `DatasetInfo` — the metadata you'd want to check before committing to a download: row/feature counts, tasks, target columns, whether the data has missing values, license, and a source URL.

```python
info = flux.info(results[0])
```

### `pull(result)`

Takes a single `SearchResult` and returns the actual dataset as a `polars.DataFrame`. This is the only verb that always triggers a real download (or read from local cache, if already pulled before).

```python
df = flux.pull(results[0])
```

Every provider — no matter its native format (pandas, CSV, JSON, image folders, HTTP JSON responses) — is normalized into this one shape. You never need to know or care what the source format was.

### `export(df, path, *, overwrite=False, mkdir=True)`

Writes a `polars.DataFrame` to disk. Format is inferred from the file extension.

```python
flux.export(df, "housing.csv")
```

Raises `ExportFileExistsError` if the target path already exists and `overwrite` isn't set to `True`, and `UnsupportedExportFormatError` for an unrecognized extension.

---

## The two data shapes

Every provider, regardless of source, returns exactly these two objects. This is the actual mechanism that makes "one API for every dataset source" true rather than aspirational.

### `SearchResult`

What you get back from `search()` — enough to identify a dataset and hand it to `info()` or `pull()`.

```python
@dataclass(slots=True)
class SearchResult:
    id: str
    name: str
    provider: str
    description: str | None = None
    relevance: int = 0
```

### `DatasetInfo`

What you get back from `info()` — everything you'd want to know before pulling.

```python
@dataclass(slots=True)
class DatasetInfo:
    id: str | int
    name: str
    description: str | None
    instances: int | None
    features: int | None
    tasks: list[str]
    target: list[str]
    has_missing_values: bool | None
    provider: str
    url: str | None
    extra: dict[str, Any]
```

`extra` holds anything provider-specific that doesn't fit the standardized fields — worth checking if you need something unusual for a particular source.

---

## How ranking works

When `search()` fans out to all nine providers, results don't come back in an arbitrary merged order. Each result is scored as:

```
score = (relevance × 1000) + provider_priority + documentation_bonus
```

**Relevance to your query always wins first** — an exact word match outranks a partial match, regardless of provider. Provider priority (scikit-learn and UCI ranked above crowd-sourced Kaggle, for example) only breaks ties *among* equally-relevant results, and a small documentation bonus breaks any remaining tie in favor of better-described datasets.

This is why searching `"iris"` puts the UCI and scikit-learn results first — not because Kaggle is deprioritized outright, but because among many equally exact matches, the curated sources are given precedence. See [Searching](../guide/searching.md) for the full breakdown, and [Providers Overview](../providers/overview.md) for the reasoning per provider.

---

## The typical flow

Most usage follows the same shape:

```python
from dataflux import flux

# 1. Find candidates
results = flux.search("housing", display=False)

# 2. Check what you're about to download
info = flux.info(results[0])

# 3. Load it
df = flux.pull(results[0])

# 4. Do something with it — or hand it straight to another tool
flux.export(df, "housing.csv")
```

## Next step

[:octicons-arrow-right-24: Searching](../guide/searching.md) — a deeper look at ranking, the `raw`/`display`/`limit` options, and how to search programmatically without any console output at all.