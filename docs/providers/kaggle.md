# Kaggle

Kaggle is the one provider in DataFlux with a genuinely different architecture from the rest — and it's a deliberate design choice, not a workaround.

```python
flux.search("netflix")   # provider="kaggle" results included automatically
```

---

## The problem this provider solves

Kaggle's own search API (`/datasets/list`) requires authentication — even to search **public** datasets. That's a hard constraint of Kaggle's platform, not something DataFlux can configure around.

DataFlux's core commitment is that **no provider should require a login just to discover what's available.** Rather than break that promise for Kaggle alone, or force every DataFlux user to create a Kaggle account and API key just to use `search()`, `KaggleProvider` takes a different approach entirely.

## How it actually works

### `search()` — bundled offline index, zero auth

Instead of calling Kaggle's live API, `KaggleProvider.search()` reads from a JSON index bundled inside the package itself:

```python
def _load_index(self) -> list[dict]:
    with open(
        Path(__file__).parent.parent / "resources" / "kaggle_index.json",
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)
```

Each entry in this index has enough metadata to power search and a reasonable `info()` without ever touching the network:

```json
{
  "owner_slug": "uciml",
  "dataset_slug": "iris",
  "title": "Iris Species",
  "subtitle": "Classify iris plants into three species in this classic dataset"
}
```

This index is refreshed on a recurring schedule (via an authenticated maintainer-side script, run in CI — not something end users ever touch) rather than live, per-query.

### `pull()` — live download, still zero auth

Once you've found a dataset via the offline index, `pull()` downloads the actual data live, using `kagglehub`:

```python
def pull(self, dataset_id: str) -> pl.DataFrame:
    dataset_path = Path(kagglehub.dataset_download(dataset_id))
    csv_file = next(dataset_path.rglob("*.csv"))

    return kagglehub.dataset_load(
        KaggleDatasetAdapter.POLARS,
        handle=dataset_id,
        path=csv_file.name,
    ).collect()
```

Kaggle's *download* endpoint (unlike its search/list endpoint) doesn't require authentication for public datasets — so `pull()` genuinely hits Kaggle's live infrastructure, with no login needed.

## The honest tradeoff

| | Search freshness | Requires auth |
|---|---|---|
| `search()` | As current as the last index refresh (periodic, not real-time) | No |
| `pull()` | Always live | No |

If a dataset was published on Kaggle very recently, it won't show up in `flux.search()` until the bundled index is next refreshed. Everything already in the index will `pull()` correctly at any time.

!!! note "Live Kaggle search is a possible future addition"
    An opt-in mode for authenticated, real-time Kaggle search is a reasonable future extension, but it's deliberately not the default — DataFlux's Kaggle provider is designed so the common case never requires you to touch a Kaggle account at all.

## Result format

```python
results = flux.search("iris", display=False)
kaggle_result = next(r for r in results if r.provider == "kaggle")

print(kaggle_result.id)    # "uciml/iris" — owner_slug/dataset_slug
print(kaggle_result.name)  # "Iris Species"
```

## `info()` field notes

Kaggle's bundled index doesn't include row/column counts or task metadata, so several `DatasetInfo` fields are always `None` for this provider:

```python
info = flux.info(kaggle_result)

info.instances            # None
info.features             # None
info.tasks                # None
info.target               # None
info.has_missing_values   # None
info.url                  # "https://www.kaggle.com/datasets/uciml/iris"
info.extra                # full raw index entry (title, subtitle, owner_slug, dataset_slug)
```

!!! warning "One inconsistency to know about"
    If you call `info()` with a dataset id that isn't in the bundled index, `KaggleProvider` raises a plain `ValueError` rather than a `DataFluxError` subclass. See [Error Handling](../guide/error-handling.md#a-known-inconsistency-to-be-aware-of) for how to handle this defensively.

## Assumptions about the downloaded file

`pull()` looks for the **first CSV file** it finds inside the downloaded dataset folder (`next(dataset_path.rglob("*.csv"))`). For datasets that ship multiple CSVs (e.g. separate train/test files), this means you may not get the file you expect — there's currently no way to select a specific file within a multi-file Kaggle dataset through `pull()`.