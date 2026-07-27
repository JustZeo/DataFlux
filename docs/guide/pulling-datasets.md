# Pulling Datasets

`pull()` is the only DataFlux verb that always triggers real data movement — a download, a local file read, or an HTTP fetch, depending on the provider.

```python
flux.pull(result: SearchResult) -> polars.DataFrame
```

---

## Basic usage

```python
results = flux.search("iris", display=False)
df = flux.pull(results[0])
```

`df` is always a `polars.DataFrame`, regardless of the provider's native format:

```python
print(df.shape)
print(df.columns)
df.head()
```

## Why always Polars

Every provider's native return type is normalized before it reaches you:

| Provider | Native format | Normalized via |
|---|---|---|
| UCI | pandas DataFrame(s) | `pl.from_pandas()` |
| Kaggle | CSV file inside a downloaded folder | Loaded directly as Polars |
| scikit-learn | numpy arrays / pandas | Converted to Polars |
| Others | provider-specific | Converted to Polars |

You never need a branch in your code for "if this came from provider X, handle it differently." One shape, every time.

## Column shape for supervised datasets

For providers with a clear features/target split (like UCI), `pull()` joins features and target columns into a single DataFrame rather than returning them separately:

```python
df = flux.pull(results[0])  # feature columns + target column(s), one DataFrame
```

If you need to know which columns are the target versus features, check `info()` first — `DatasetInfo.target` lists the target column name(s).

---

## Caching — what's actually cached today

This is worth being precise about, since caching behavior currently **varies by provider** rather than being a single guaranteed behavior across DataFlux.

- **TorchVision** — pulled datasets are cached under `~/.dataflux/torchvision/`. Repeated `pull()` calls for the same dataset reuse the local copy instead of re-downloading.
- **Kaggle** — relies on `kagglehub`'s own local caching, which lives outside DataFlux's own cache directory. A second `pull()` for the same dataset will typically be fast because `kagglehub` itself avoids re-downloading, not because DataFlux manages it.
- **UCI, Hugging Face, and the rest** — currently re-fetch on every `pull()` call. If you're pulling the same dataset repeatedly in a loop or notebook, consider storing the returned `DataFrame` in a variable rather than calling `pull()` again.

```python
df = flux.pull(results[0])   # fetch once
# reuse `df` from here on — don't call pull() again for the same result
```

!!! note "This is expected to change"
    A unified, provider-agnostic caching layer for `pull()` is on the roadmap — see [Caching](caching.md) for the cache infrastructure that already exists and how it's expected to be wired in more broadly.

---

## Errors during `pull()`

A failed pull (bad dataset id, network failure, missing file in an archive) raises `PullError` or a more specific subclass such as `DownloadError`. See [Error Handling](error-handling.md) for the full hierarchy.

## Next step

[:octicons-arrow-right-24: Exporting Data](exporting-data.md) — writing the DataFrame you just pulled to disk.