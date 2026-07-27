# Searching

`search()` is the entry point to everything else in DataFlux. This page covers how ranking actually works, the `raw`/`display`/`limit` options in depth, and how to use `search()` inside scripts and pipelines without any console output.

```python
flux.search(query: str, *, raw: bool = False, display: bool = True, limit: int | None = 10) -> list[SearchResult]
```

---

## How results are ranked

Every provider's results are merged and sorted by a single score, computed per result:

```
score = (relevance × 1000) + provider_priority + documentation_bonus
```

Broken down:

### 1. Relevance (dominant factor)

Each provider scores its own results against the query before DataFlux ever sees them:

| Match type | Relevance |
|---|---|
| Exact word match (e.g. query `"iris"` matches the whole word "iris" in the title/description) | `2` |
| Partial/substring match | `1` |
| No match | `-1` |

Because relevance is multiplied by `1000`, it dominates the score — an exact word match from a lower-priority provider will still rank above a merely-partial match from a higher-priority one.

### 2. Provider priority (tiebreaker among equally-relevant results)

When two results have the same relevance, provider priority decides the order:

| Provider | Priority |
|---|---|
| scikit-learn | 100 |
| UCI | 95 |
| TorchVision | 90 |
| Hugging Face | 80 |
| Kaggle | 70 |
| Statsmodels | 60 |
| Seaborn | 50 |
| Vega | 40 |
| World Bank | 30 |

This is why, for an exact-match query like `"iris"`, scikit-learn and UCI surface before Kaggle — not because Kaggle's dataset is less relevant, but because among many equally-relevant exact matches, the curated sources are given precedence.

### 3. Documentation bonus (final tiebreaker)

A result with a non-empty description gets a small `+5` bonus over an otherwise identical result with no description. This nudges well-documented datasets slightly above bare, undocumented ones when everything else is tied.

### Final tiebreak: alphabetical

If two results have the exact same score, they're sorted alphabetically by name.

!!! tip "In short"
    Relevance to your query always wins first. Provider trustworthiness and documentation quality only break ties — DataFlux will never rank a weak match from scikit-learn above a strong match from Kaggle just because of provider priority.

---

## `display` — controlling console output

By default, `search()` prints a formatted table as a side effect and still returns the full result list:

```python
results = flux.search("iris")
```

Set `display=False` to search silently — useful inside scripts, loops, or when you're about to immediately pass results to `info()`/`pull()` and don't want a table printed first:

```python
results = flux.search("iris", display=False)
```

The return value is identical either way — `display` only affects what gets printed, never what gets returned.

---

## `raw` — bypassing pretty formatting entirely

```python
results = flux.search("iris", raw=True)
```

`raw=True` skips pretty output regardless of `display`. Use this when you want the plainest, most predictable path through `search()` — for example, in automated pipelines where you never want any formatting logic to run at all.

---

## `limit` — capping the printed table

```python
flux.search("iris", limit=25)
```

`limit` only controls how many rows appear in the **printed** table (default `10`). It does not truncate the actual returned list — `search()` always returns every ranked match, however many there are.

```python
results = flux.search("iris", display=False)
len(results)  # could be 300+, regardless of limit
```

If you want to work with the full result set programmatically, use `display=False` (or `raw=True`) rather than trying to raise `limit` — `limit` is purely a display concern.

---

## Searching silently in a script

The common pattern for automated/programmatic use:

```python
from dataflux import flux

results = flux.search("housing", display=False)

if not results:
    # in practice this won't be reached — see below
    ...

best_match = results[0]
df = flux.pull(best_match)
```

## When nothing matches

If **no provider** returns a match for the query, `search()` raises `DatasetNotFoundError` rather than returning an empty list:

```python
from dataflux.exceptions import DatasetNotFoundError

try:
    flux.search("asdkfjhaslkdjf")
except DatasetNotFoundError as e:
    print(e)  # "Dataset 'asdkfjhaslkdjf' was not found."
```

See [Error Handling](error-handling.md) for the full exception hierarchy.

## Next step

[:octicons-arrow-right-24: Inspecting Datasets](inspecting-datasets.md) — using `info()` to check a dataset before pulling it.