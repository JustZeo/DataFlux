# Inspecting Datasets

Before pulling a full dataset — which can mean a real network download — `info()` lets you check what you're about to get.

```python
flux.info(result: SearchResult, *, raw: bool = False, display: bool = True) -> DatasetInfo
```

---

## Basic usage

```python
results = flux.search("iris", display=False)
info = flux.info(results[0])
```

By default this prints a formatted summary to the console and returns a `DatasetInfo`:

```python
print(info.name)                # "Iris"
print(info.instances)           # 150
print(info.features)            # 4
print(info.tasks)                # ["Classification"]
print(info.has_missing_values)  # False
print(info.url)                 # "https://archive.ics.uci.edu/dataset/53/iris"
```

## `display` and `raw`

Same pattern as `search()`:

```python
info = flux.info(results[0], display=False)  # no console output, same return value
info = flux.info(results[0], raw=True)       # skip pretty formatting regardless of display
```

## The `extra` field

Not every provider's metadata maps cleanly onto the standardized `DatasetInfo` fields. Anything provider-specific that doesn't fit is preserved in `extra`:

```python
info = flux.info(results[0])
print(info.extra)  # dict — full raw metadata from the source provider
```

This is worth checking if you need something unusual for a specific dataset that isn't one of the standard fields.

---

## A note on repeated calls

`info()` fetches the dataset's metadata from its source provider — for some providers (like UCI) this means a real network request, not just a local lookup. If you call `flux.info()` multiple times for the same result, expect it to hit the network again each time rather than being cached automatically. If you need the same info repeatedly, store the returned `DatasetInfo` in a variable rather than re-calling `info()`:

```python
info = flux.info(results[0])  # fetch once
# reuse `info` from here on, rather than calling flux.info(results[0]) again
```

## Next step

[:octicons-arrow-right-24: Pulling Datasets](pulling-datasets.md) — loading the actual data as a Polars DataFrame.