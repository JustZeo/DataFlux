# UCI

The UCI Machine Learning Repository provider, backed by the `ucimlrepo` package — one of the two fully curated, high-signal sources in DataFlux (alongside scikit-learn).

---

## Search source

`search()` queries UCI's live dataset listing API and matches against dataset names:

```python
def _datasets(self) -> list[dict]:
    with urllib.request.urlopen(API_LIST_URL) as response:
        payload = json.load(response)
    return payload["data"]
```

Because this is a real network call, results always reflect UCI's current catalog — there's no bundled/stale index for this provider.

## Result format

```python
results = flux.search("iris", display=False)
uci_result = next(r for r in results if r.provider == "uci")

print(uci_result.id)    # 53 — UCI's internal integer dataset id
print(uci_result.name)  # "Iris"
```

## `pull()`

```python
def pull(self, dataset_id: int | str) -> pl.DataFrame:
    dataset = fetch_ucirepo(id=int(dataset_id))
    features = dataset.data.features
    targets = dataset.data.targets
    if targets is not None:
        df = features.join(targets)
    else:
        df = features
    return pl.from_pandas(df)
```

Feature and target columns are joined into a single DataFrame. If a dataset has no defined target (unsupervised datasets), you just get the feature columns.

## `info()`

UCI is the most fully-populated provider for `DatasetInfo` — every standard field is backed by real metadata from UCI's API, not left as `None`:

```python
info = flux.info(uci_result)

info.instances            # e.g. 150
info.features              # e.g. 4
info.tasks                 # e.g. ["Classification"]
info.target                 # e.g. "class"
info.has_missing_values    # True/False, from UCI's own metadata
info.url                    # UCI's repository page for the dataset
info.extra                  # the full raw metadata dict from ucimlrepo
```

!!! note "Network call on every `info()`"
    `info()` calls `fetch_ucirepo()` — a real network request — every time it's invoked, not just on `pull()`. If you call `flux.info()` repeatedly for the same dataset, expect a fresh request each time. See [Inspecting Datasets](../guide/inspecting-datasets.md#a-note-on-repeated-calls) for the general guidance on this.

## Dataset identifier

UCI datasets are identified by an **integer id** internally (e.g. `53` for Iris), unlike most other providers which use string slugs. `SearchResult.id` will be that integer (or a numeric string) — you don't need to look this up yourself if you're going through `search()` → `info()`/`pull()` normally.