# `BaseProvider`

```python
from dataflux.providers.base import BaseProvider
```

`BaseProvider` is the abstract contract every DataFlux provider implements. It's what makes `flux.search()`, `flux.info()`, and `flux.pull()` work identically regardless of which of the nine data sources you're talking to. See [Writing a Provider](../advanced/writing-a-provider.md) for a full walkthrough of implementing a new one.

```python
class BaseProvider(ABC)
```

---

## `name`

```python
@property
@abstractmethod
def name(self) -> str
```

The provider's unique, lowercase identifier — e.g. `"uci"`, `"kaggle"`, `"huggingface"`. Used as the registry key in `ProviderRegistry` and stored on every `SearchResult`/`DatasetInfo` this provider produces.

Must be non-empty and unique across all registered providers — `ProviderRegistry.register()` raises `InvalidProviderError` or `ProviderAlreadyRegisteredError` otherwise.

---

## `search`

```python
@abstractmethod
def search(self, query: str) -> Any
```

Search this provider's catalog for `query` and return matches as `SearchResult` objects, best-match first.

| Parameter | Type | Description |
|---|---|---|
| `query` | `str` | The search term, as passed to `flux.search()`. |

**Returns:** `list[SearchResult]` in every built-in implementation, though the abstract signature is typed `Any`.

Implementations typically use `dataflux.utils.search.search_score()` to score candidates against the query, filter out non-matches (`score == -1`), and sort descending by score. See any built-in provider (e.g. `UCIProvider.search()`) for the pattern.

---

## `pull`

```python
@abstractmethod
def pull(self, dataset: str) -> Path
```

Download the dataset and return its local path.

| Parameter | Type | Description |
|---|---|---|
| `dataset` | `str` | The dataset identifier, taken from `SearchResult.id`. |

**Returns:** `Path` per the abstract signature — though note built-in providers actually return `polars.DataFrame` directly rather than a path, since `Flux.pull()` expects a DataFrame. Custom providers should match what `Flux.pull()` needs: a `polars.DataFrame`.

---

## `info`

```python
@abstractmethod
def info(self, dataset: str) -> Any
```

Return metadata for a dataset without downloading it.

| Parameter | Type | Description |
|---|---|---|
| `dataset` | `str` | The dataset identifier, taken from `SearchResult.id`. |

**Returns:** `DatasetInfo` in every built-in implementation.

---

## Implementing a provider

At minimum:

```python
from dataflux.providers.base import BaseProvider
from dataflux.models.search_result import SearchResult
from dataflux.models.dataset import DatasetInfo


class MyProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "myprovider"

    def search(self, query: str) -> list[SearchResult]:
        ...

    def pull(self, dataset: str):
        ...  # returns a polars.DataFrame

    def info(self, dataset: str) -> DatasetInfo:
        ...
```

Then register an instance with the `ProviderRegistry` (built-in providers are registered inside `Flux.__init__`).

## Next step

Read [Writing a Provider](../advanced/writing-a-provider.md) for the full guide, including how registration, resolution, and caching fit together.
