# scikit-learn

The scikit-learn provider — fully bundled, fully offline, and the fastest of the nine since nothing ever touches the network.

---

## Search source

`search()` matches against a fixed list of dataset names bundled with DataFlux (`SKLEARN_DATASETS`), covering the datasets scikit-learn ships loader functions for (iris, wine, digits, diabetes, breast cancer, and similar toy/reference datasets):

```python
def search(self, query: str) -> list[SearchResult]:
    for dataset in SKLEARN_DATASETS:
        score = search_score(query, dataset)
        ...
```

Since this list is fixed and bundled, `search()` never hits the network and is effectively instant.

## Result format

```python
results = flux.search("iris", display=False)
sklearn_result = next(r for r in results if r.provider == "sklearn")

print(sklearn_result.id)    # "iris" — the internal loader key
print(sklearn_result.name)  # "Iris" — title-cased for display
```

## `pull()`

```python
def pull(self, dataset_id: str) -> pl.DataFrame:
    dataset = self._load_dataset(dataset_id, as_frame=True)
    return pl.from_pandas(dataset.frame)
```

Uses scikit-learn's own `as_frame=True` loading path, then converts the resulting pandas DataFrame to Polars. Feature and target columns arrive together in `dataset.frame`, same as scikit-learn's native behavior.

## `info()`

```python
info = flux.info(sklearn_result)

info.instances            # dataset.data.shape[0]
info.features              # dataset.data.shape[1]
info.description            # scikit-learn's own DESCR text
info.target                 # list of target class names
info.tasks                  # always None — scikit-learn doesn't label task type
info.has_missing_values    # always False
info.url                    # always None — no canonical source URL for these
info.extra                  # feature_names, filename, data_module
```

!!! note "`has_missing_values` is hardcoded, not measured"
    Unlike UCI, this field isn't computed from the actual data — it's set to `False` unconditionally, since scikit-learn's bundled toy datasets are curated to be clean. If you're relying on this field to detect missing values programmatically across providers, be aware this one doesn't actually check.