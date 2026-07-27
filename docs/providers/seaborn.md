# Seaborn

The Seaborn provider — a small, fixed catalog of the example datasets bundled with the `seaborn` visualization library (tips, titanic, penguins, and similar).

---

## Search source

`search()` matches against a fixed list of dataset names (`SEABORN_DATASETS`), bundled with DataFlux:

```python
def search(self, query: str) -> list[SearchResult]:
    for dataset in SEABORN_DATASETS:
        score = search_score(query, dataset)
        ...
```

No network call during search — instant, offline.

## Result format

```python
results = flux.search("tips", display=False)
seaborn_result = next(r for r in results if r.provider == "seaborn")

print(seaborn_result.id)    # "tips"
print(seaborn_result.name)  # "Tips"
```

## `pull()`

```python
def pull(self, dataset_id: str) -> pl.DataFrame:
    return pl.from_pandas(self._load_df(dataset_id))
```

Loads via `seaborn.load_dataset()` and converts the resulting pandas DataFrame to Polars.

!!! note "Downloads on first use"
    `seaborn.load_dataset()` fetches data from Seaborn's own GitHub-hosted CSV repository the first time a dataset is requested — it's not bundled inside `seaborn` itself. This means the very first `pull()` (or `info()`) for a given Seaborn dataset does make a network request, even though `search()` never does.

## `info()`

```python
info = flux.info(seaborn_result)

info.instances            # dataset.shape[0]
info.features              # dataset.shape[1]
info.has_missing_values    # computed from the real data via .isnull().values.any()
info.tasks                  # always None
info.target                 # always None
info.url                    # always None
info.extra                  # columns and dtypes
```

Unlike scikit-learn's hardcoded `has_missing_values=False`, Seaborn's version actually checks the loaded data — some Seaborn example datasets (like `titanic`) genuinely do have missing values, and this field reflects that correctly.