# Error Handling

DataFlux raises specific, typed exceptions instead of letting raw provider errors (a `urllib` timeout, a `KeyError` from malformed JSON, an `HTTPError`) leak through to your code. Every DataFlux-raised exception inherits from one base class.

```python
from dataflux.exceptions import DataFluxError
```

---

## The exception hierarchy

```
DataFluxError                          # base — catch this to handle any DataFlux failure

├── InvalidProviderError                # a registered provider fails validation
├── ProviderAlreadyRegisteredError       # duplicate provider name at registration
├── ProviderNotFoundError                # info()/pull() referencing an unknown provider

├── DatasetNotFoundError                 # search() found nothing, across every provider
├── InvalidDatasetError                  # a dataset identifier is malformed
├── DatasetLoadError                     # a dataset failed to load

├── SearchError
│   └── EmptySearchQueryError             # search("") — an empty query string

├── PullError                            # pull() failed
├── DownloadError                        # a specific download failed (has the failing URL)

├── CacheError                           # a cache read/write operation failed
├── FileSystemError                      # a filesystem operation failed

└── ExportError
    ├── UnsupportedExportFormatError      # export() called with an unrecognized extension
    ├── ExportFileExistsError             # export() target exists and overwrite=False
    └── InvalidExportDataError            # export() called with something that isn't a Polars DataFrame
```

---

## Catching a specific failure

```python
from dataflux import flux
from dataflux.exceptions import DatasetNotFoundError

try:
    flux.search("asdkfjhaslkdjf")
except DatasetNotFoundError:
    print("No matches across any provider.")
```

## Catching anything DataFlux raises

Since every exception inherits from `DataFluxError`, you can catch broadly when you just want to know "did something in DataFlux go wrong":

```python
from dataflux.exceptions import DataFluxError

try:
    results = flux.search("housing")
    df = flux.pull(results[0])
    flux.export(df, "housing.csv")
except DataFluxError as e:
    print(f"DataFlux operation failed: {e}")
```

## Common exceptions in practice

### No search results

```python
from dataflux.exceptions import DatasetNotFoundError

try:
    flux.search("qwertyuiop")
except DatasetNotFoundError as e:
    print(e)  # "Dataset 'qwertyuiop' was not found."
```

### Export target already exists

```python
from dataflux.exceptions import ExportFileExistsError

try:
    flux.export(df, "housing.csv")  # file already exists
except ExportFileExistsError:
    flux.export(df, "housing.csv", overwrite=True)
```

### Unsupported export format

```python
from dataflux.exceptions import UnsupportedExportFormatError

try:
    flux.export(df, "housing.xlsx")
except UnsupportedExportFormatError as e:
    print(e)  # lists the supported extensions
```

---

## A known inconsistency to be aware of

Almost every failure path across the nine providers raises a proper `DataFluxError` subclass. There's currently one exception: `KaggleProvider.info()` raises a plain built-in `ValueError` when a dataset id isn't found in its bundled index, rather than a `DataFluxError` subclass like `DatasetNotFoundError` or `InvalidDatasetError`.

```python
# Today, this specific case does NOT raise a DataFluxError subclass:
flux.info(some_result_with_a_bad_kaggle_id)  # raises plain ValueError, not caught by `except DataFluxError`
```

If you're writing code that should robustly catch *any* DataFlux-related failure, catch `(DataFluxError, ValueError)` together until this is unified:

```python
try:
    flux.info(result)
except (DataFluxError, ValueError) as e:
    print(f"Failed to get info: {e}")
```

!!! note "This is expected to be fixed"
    This is tracked as a known gap rather than intended behavior — future versions should raise a proper `DataFluxError` subclass here for consistency with every other provider.

## Next step

You've now covered the full guide. Head to [Providers Overview](../providers/overview.md) to see how each of the nine data sources works under the hood, or jump straight to the [API Reference](../api-reference/flux.md) for full signatures.