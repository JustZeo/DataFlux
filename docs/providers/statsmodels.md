# Statsmodels

The Statsmodels provider — a small, fixed catalog of the classic econometrics and time-series datasets bundled with `statsmodels` (e.g. macroeconomic data, Grunfeld's investment data, and similar reference datasets).

---

## Search source

`search()` matches against a fixed list of dataset names (`STATSMODELS_DATASETS`), bundled with DataFlux:

```python
def search(self, query: str) -> list[SearchResult]:
    for dataset in STATSMODELS_DATASETS:
        score = search_score(query, dataset)
        ...
```

No network call during search — instant, offline.

## Result format

```python
results = flux.search("macrodata", display=False)
sm_result = next(r for r in results if r.provider == "statsmodels")

print(sm_result.id)    # "macrodata"
print(sm_result.name)  # "Macrodata"
```

## `pull()`

```python
def _load_df(self, dataset_id: str):
    module = getattr(sm.datasets, dataset_id)
    return module.load_pandas().data

def pull(self, dataset_id: str) -> pl.DataFrame:
    return pl.from_pandas(self._load_df(dataset_id))
```

Loads via `statsmodels.api.datasets.<name>.load_pandas().data` and converts to Polars. These datasets are bundled with `statsmodels` itself, so no network access is required for this provider at any stage — search, info, and pull are all fully offline.

## `info()`

```python
info = flux.info(sm_result)

info.instances            # dataset.shape[0]
info.features              # dataset.shape[1]
info.has_missing_values    # computed from the real data
info.tasks                  # always None
info.target                 # always None
info.url                    # always None
info.extra                  # columns and dtypes
```

## Dataset identifiers

The `dataset_id` here corresponds directly to an attribute name on `statsmodels.api.datasets` (e.g. `macrodata`, `grunfeld`, `sunspots`) — the same names you'd use if calling `statsmodels` directly. `search()` handles the lookup for you, so you generally don't need to know these names in advance.