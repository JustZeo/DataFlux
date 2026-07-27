# Exceptions

`dataflux.exceptions` defines a typed exception hierarchy so callers can catch DataFlux failures specifically, instead of catching raw `urllib` errors, `KeyError`s, or other provider-internal failures. Every exception in this module inherits from `DataFluxError`.

```python
from dataflux.exceptions import DataFluxError
```

See [Error Handling](../guide/error-handling.md) for a practical guide to using these, including a known inconsistency in `KaggleProvider.info()`.

---

## `DataFluxError`

```python
class DataFluxError(Exception)
```

Base exception for all DataFlux errors. Catch this to handle any failure raised by DataFlux itself.

---

## Provider errors

### `InvalidProviderError`

```python
class InvalidProviderError(DataFluxError)
```

Raised when a provider fails validation during registration — either it doesn't inherit from `BaseProvider`, or its `.name` is empty.

### `ProviderAlreadyRegisteredError`

```python
class ProviderAlreadyRegisteredError(DataFluxError)
def __init__(self, provider_name: str)
```

Raised when `ProviderRegistry.register()` is called with a provider whose `.name` is already registered.

| Parameter | Type | Description |
|---|---|---|
| `provider_name` | `str` | The name that was already registered. |

### `ProviderNotFoundError`

```python
class ProviderNotFoundError(DataFluxError)
def __init__(self, provider_name: str)
```

Raised when `info()` or `pull()` reference a provider name that isn't registered.

| Parameter | Type | Description |
|---|---|---|
| `provider_name` | `str` | The provider name that was looked up. |

---

## Dataset errors

### `DatasetNotFoundError`

```python
class DatasetNotFoundError(DataFluxError)
def __init__(self, dataset: str | int)
```

Raised by `search()` when no provider returns any match for the query.

| Parameter | Type | Description |
|---|---|---|
| `dataset` | `str \| int` | The query (or dataset identifier) that produced no match. |

### `InvalidDatasetError`

```python
class InvalidDatasetError(DataFluxError)
def __init__(self, dataset: str | int)
```

Raised when a dataset identifier is malformed for the provider it's being used with.

| Parameter | Type | Description |
|---|---|---|
| `dataset` | `str \| int` | The invalid identifier. |

### `DatasetLoadError`

```python
class DatasetLoadError(DataFluxError)
def __init__(self, dataset: str | int)
```

Raised when a dataset is found but fails to load.

| Parameter | Type | Description |
|---|---|---|
| `dataset` | `str \| int` | The identifier of the dataset that failed to load. |

---

## Search errors

### `SearchError`

```python
class SearchError(DataFluxError)
```

Base class for search-related failures.

### `EmptySearchQueryError`

```python
class EmptySearchQueryError(SearchError)
def __init__(self)
```

Raised when `search()` is called with an empty query string.

---

## Pull errors

### `PullError`

```python
class PullError(DataFluxError)
```

Base class raised when `pull()` fails.

### `DownloadError`

```python
class DownloadError(DataFluxError)
def __init__(self, url: str)
```

Raised when a specific network download fails.

| Parameter | Type | Description |
|---|---|---|
| `url` | `str` | The URL that failed to download. |

---

## Cache and filesystem errors

### `CacheError`

```python
class CacheError(DataFluxError)
```

Raised when a cache read or write operation fails.

### `FileSystemError`

```python
class FileSystemError(DataFluxError)
```

Raised when a filesystem operation fails.

---

## Export errors

### `ExportError`

```python
class ExportError(DataFluxError)
```

Base class for export-related failures.

### `UnsupportedExportFormatError`

```python
class UnsupportedExportFormatError(ExportError)
def __init__(self, extension: str)
```

Raised when `export()` is called with a file extension that isn't supported. See [Exporting Data](../guide/exporting-data.md) for the supported list.

| Parameter | Type | Description |
|---|---|---|
| `extension` | `str` | The unsupported extension. |

### `ExportFileExistsError`

```python
class ExportFileExistsError(ExportError)
def __init__(self, path: str)
```

Raised when `export()`'s target path already exists and `overwrite=False` (the default).

| Parameter | Type | Description |
|---|---|---|
| `path` | `str` | The path that already exists. |

### `InvalidExportDataError`

```python
class InvalidExportDataError(ExportError)
def __init__(self, message: str = "export() expects a Polars DataFrame.")
```

Raised when `export()` is called with something other than a `polars.DataFrame`.

| Parameter | Type | Description |
|---|---|---|
| `message` | `str` | Custom message; defaults to a description of the expected type. |

---

## The full hierarchy

```
DataFluxError
├── InvalidProviderError
├── ProviderAlreadyRegisteredError
├── ProviderNotFoundError
├── DatasetNotFoundError
├── InvalidDatasetError
├── DatasetLoadError
├── SearchError
│   └── EmptySearchQueryError
├── PullError
├── DownloadError
├── CacheError
├── FileSystemError
└── ExportError
    ├── UnsupportedExportFormatError
    ├── ExportFileExistsError
    └── InvalidExportDataError
```

## Next step

See [Error Handling](../guide/error-handling.md) for catch patterns and a known gap where `KaggleProvider.info()` raises a plain `ValueError` instead of a `DataFluxError` subclass.
