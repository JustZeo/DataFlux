# DataFlux

**One API. Every dataset.**

DataFlux is a universal dataset library for Python. It lets you discover, inspect, and load datasets from multiple providers through a single, consistent interface — so you never have to learn a different package, authentication flow, or return type for every dataset source.

```python
from dataflux import flux

results = flux.search("iris")
info = flux.info(results[0])
df = flux.pull(results[0])
```

Whether the dataset lives on scikit-learn, UCI, Kaggle, Hugging Face, TorchVision, Seaborn, Statsmodels, Vega, or the World Bank — you never have to care. Every provider returns the exact same shapes: a list of `SearchResult`, a `DatasetInfo`, and a `polars.DataFrame`.

---

## Why DataFlux exists

Every dataset provider does things differently today:

=== "scikit-learn"
    ```python
    from sklearn.datasets import load_iris
    iris = load_iris(as_frame=True)
    ```

=== "UCI"
    ```python
    from ucimlrepo import fetch_ucirepo
    iris = fetch_ucirepo(id=53)
    ```

=== "Hugging Face"
    ```python
    from datasets import load_dataset
    dataset = load_dataset(...)
    ```

=== "Kaggle"
    ```python
    # requires authentication, zip downloads, manual extraction...
    ```

Different function names. Different auth requirements. Different metadata shapes. Different return types. DataFlux collapses all of it into one contract:

```python
results = flux.search("housing")
info = flux.info(results[0])
df = flux.pull(results[0])
```

---

## What you get

- :material-magnify: **One `search()`** across nine providers at once, ranked so the best match surfaces first
- :material-information-outline: **One `info()`** to inspect a dataset before committing to a download
- :material-download: **One `pull()`** that always returns a `polars.DataFrame` — no provider-specific objects, no pandas
- :material-file-export: **One `export()`** to write that DataFrame to CSV, Parquet, JSON, and more
- :material-shield-check: **No forced authentication** — every provider, including Kaggle, works out of the box with zero login

---

## Quick example

```python
from dataflux import flux

# Search across every registered provider
flux.search("housing")

# Inspect the first result
info = flux.info(flux.search("housing", display=False)[0])

# Pull it as a Polars DataFrame
df = flux.pull(flux.search("housing", display=False)[0])

# Export it to disk
flux.export(df, "housing.csv")
```

---

## Where to go next

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Getting Started**

    ---

    Install DataFlux and run your first search in under a minute.

    [:octicons-arrow-right-24: Installation](getting-started/installation.md)

-   :material-book-open-variant:{ .lg .middle } **Core Concepts**

    ---

    Understand `search`, `info`, `pull`, and `export` — and how they fit together.

    [:octicons-arrow-right-24: Core Concepts](getting-started/core-concepts.md)

-   :material-database-search:{ .lg .middle } **Providers**

    ---

    See every supported data source, and how Kaggle works without requiring a login.

    [:octicons-arrow-right-24: Providers Overview](providers/overview.md)

-   :material-code-tags:{ .lg .middle } **API Reference**

    ---

    Full signatures for `flux`, the data models, and the exception hierarchy.

    [:octicons-arrow-right-24: API Reference](api-reference/flux.md)

</div>

---

## Project status

DataFlux is at **v0.1.0**. All nine planned providers for this release are implemented, tested, and ready to use. See the [changelog](changelog.md) for what's next.