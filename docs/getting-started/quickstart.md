# Quickstart

This page gets you from install to a working DataFrame in under a minute.

## 1. Import `flux`

DataFlux exposes a single, pre-configured object — `flux` — with every provider already registered. There's nothing to set up.

```python
from dataflux import flux
```

## 2. Search for a dataset

```python
flux.search("iris")
```

By default, `search()` prints a formatted table straight to your console:

```
                     Search Results (10 of 303)
┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃  # ┃ Name           ┃ Provider ┃ ID             ┃ Description    ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│  1 │ Iris           │ uci      │ 53             │ -              │
│  2 │ Iris           │ sklearn  │ iris           │ -              │
│  3 │ Iris Species   │ kaggle   │ uciml/iris     │ Classify iris  │
│    │                │          │                │ plants into    │
│    │                │          │                │ three species  │
└────┴────────────────┴──────────┴────────────────┴────────────────┘

Showing the first 10 of 303 results.
Use raw=True to work with all returned results programmatically.
```

Results are ranked across every provider — curated sources like UCI and scikit-learn surface before crowd-sourced ones like Kaggle for the same query.

## 3. Grab the results as data

The pretty table is just a side effect — `search()` always returns a real `list[SearchResult]` you can index into:

```python
results = flux.search("iris", display=False)  # skip the table, just get the list
first = results[0]

print(first.name)      # "Iris"
print(first.provider)  # "uci"
print(first.id)        # "53"
```

## 4. Inspect before you commit

```python
flux.info(first)
```

Prints a formatted summary — row/feature counts, tasks, target columns, missing-value status — and returns a `DatasetInfo` you can use programmatically.

## 5. Pull the actual data

```python
df = flux.pull(first)
```

`df` is a `polars.DataFrame`, every time, regardless of which provider it came from.

```python
print(df.shape)
print(df.head())
```

## 6. Export it

```python
flux.export(df, "iris.csv")
```

The output format is inferred from the file extension — `.csv`, `.parquet`, `.json`, `.ndjson`, `.ipc`, `.feather`, and `.arrow` are all supported.

## Putting it all together

```python
from dataflux import flux

results = flux.search("iris", display=False)
df = flux.pull(results[0])
flux.export(df, "iris.csv")
```

Four lines, one API, zero provider-specific code.

## Next step

[:octicons-arrow-right-24: Core Concepts](core-concepts.md) — the full mental model behind `search`, `info`, `pull`, and `export`, including the `raw`/`display`/`limit` options you'll want to know about.