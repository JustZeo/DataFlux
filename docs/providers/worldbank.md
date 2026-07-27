# World Bank

The World Bank provider, backed by the `wbgapi` package — the odd one out in DataFlux, since it deals in **country/time-series indicators** rather than typical row-per-record datasets.

---

## Search source

`search()` queries the World Bank's live indicator series API:

```python
def search(self, query: str) -> list[SearchResult]:
    for series in wb.series.list(q=query):
        score = search_score(query, series["value"], series["id"])
        ...
```

Matches against both the indicator's human-readable name (`series["value"]`, e.g. "GDP per capita") and its code (`series["id"]`, e.g. `"NY.GDP.PCAP.CD"`).

## Result format

```python
results = flux.search("gdp per capita", display=False)
wb_result = next(r for r in results if r.provider == "worldbank")

print(wb_result.id)    # "NY.GDP.PCAP.CD" — World Bank indicator code
print(wb_result.name)  # "GDP per capita (current US$)"
```

Unlike every other provider, the `id` here is a World Bank **indicator code**, not a dataset name or slug — this is what gets passed to `info()`/`pull()`.

## A different data shape

Every other provider in DataFlux returns something that looks like a typical ML dataset — rows of records, features, a target column. World Bank data is fundamentally different: it's a single indicator's value **across many countries and years**.

```python
df = flux.pull(wb_result)
```

```python
df.columns
# ['economy', 'series', 'YR1960', 'YR1961', ..., 'YR2023']
```

If you're used to the tabular-ML-dataset shape from other providers, expect this one to look more like a wide time-series table — one row per country, one column per year — rather than one row per observation.

## `pull()`

```python
def _load_df(self, dataset_id: str):
    return wb.data.DataFrame(dataset_id).reset_index()

def pull(self, dataset_id: str) -> pl.DataFrame:
    return pl.from_pandas(self._load_df(dataset_id))
```

Always a live network call — there's no bundled/offline path for World Bank data.

## `info()`

```python
info = flux.info(wb_result)

info.instances            # dataset.shape[0] — number of countries returned
info.features              # dataset.shape[1] — number of year columns + metadata columns
info.has_missing_values    # computed from the real data — many countries lack data for many years
info.tasks                  # always None
info.target                 # always None
info.url                    # World Bank's own indicator page
info.extra                  # indicator_code, columns, dtypes
```

!!! note "Missing values are common and expected here"
    Because this is cross-country time-series data, `has_missing_values` will very often be `True` — most indicators simply aren't tracked for every country in every year. This isn't a data quality issue the way it might be for a typical ML dataset; it's the normal shape of global indicator data.