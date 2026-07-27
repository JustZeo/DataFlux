# Vega

The Vega provider, backed by the `vega_datasets` package — small, well-known datasets commonly used for data visualization examples and benchmarks (cars, stocks, barley, and similar).

---

## Search source

Unlike Seaborn/Statsmodels, this provider doesn't use a DataFlux-bundled list — it enumerates directly from the `vega_datasets` package itself:

```python
def search(self, query: str) -> list[SearchResult]:
    for dataset in data.list_datasets():
        score = search_score(query, dataset)
        ...
```

This means Vega's available catalog always matches whatever version of `vega_datasets` you have installed, rather than a list DataFlux maintains separately.

## Result format

```python
results = flux.search("cars", display=False)
vega_result = next(r for r in results if r.provider == "vega")

print(vega_result.id)    # "cars"
print(vega_result.name)  # "Cars"
```

Dataset names containing hyphens (e.g. `"seattle-weather"`) are converted to spaces and title-cased for display, but the underlying `id` preserves the original hyphenated form.

## `pull()`

```python
def _load_df(self, dataset_id: str):
    return data(str(dataset_id).replace("-", "_"))

def pull(self, dataset_id: str) -> pl.DataFrame:
    return pl.from_pandas(self._load_df(dataset_id))
```

!!! note "Some Vega datasets are fetched over the network"
    A handful of `vega_datasets` entries are bundled locally with the package, but many are fetched from a remote CDN the first time they're loaded. Whether a given `pull()` call touches the network depends on which specific dataset you request.

## `info()`

```python
info = flux.info(vega_result)

info.instances            # dataset.shape[0]
info.features              # dataset.shape[1]
info.has_missing_values    # computed from the real data
info.tasks                  # always None
info.target                 # always None
info.url                    # always None
info.extra                  # columns and dtypes
```