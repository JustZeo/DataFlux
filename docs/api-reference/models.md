# Models

`dataflux.models` defines the two data shapes every provider returns, regardless of source. This standardization is the core of DataFlux's contract — your code never needs to branch on which provider a result came from.

```python
from dataflux.models.search_result import SearchResult
from dataflux.models.dataset import DatasetInfo
```

Both are `@dataclass(slots=True)` — plain, immutable-in-shape data containers with no behavior of their own.

---

## `SearchResult`

```python
@dataclass(slots=True)
class SearchResult:
    id: str
    name: str
    provider: str
    description: str | None = None
    relevance: int = field(default=0, repr=False)
```

One match returned by `flux.search()`. Every provider produces these, and `Flux.info()` / `Flux.pull()` both take a `SearchResult` as input — you pass one straight through from `search()` to the next call.

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Provider-specific dataset identifier. Opaque to your code — pass it straight to `info()`/`pull()` via the `SearchResult` itself, don't parse it. |
| `name` | `str` | Human-readable dataset name. |
| `provider` | `str` | Which provider produced this result (e.g. `"uci"`, `"kaggle"`). Used internally to route `info()`/`pull()` to the right provider. |
| `description` | `str \| None` | Short description, when the provider's search API exposes one. `None` otherwise. |
| `relevance` | `int` | Internal match-quality score used for ranking (`-1` to `2`); not part of `repr()`. See [Searching](../guide/searching.md). |

**Example**

```python
results = flux.search("iris", display=False)
result = results[0]
print(result.name, result.provider)
```

---

## `DatasetInfo`

```python
@dataclass(slots=True)
class DatasetInfo:
    id: str | int
    name: str
    description: str | None
    instances: int | None
    features: int | None
    tasks: list[str]
    target: list[str]
    has_missing_values: bool | None
    provider: str
    url: str | None
    extra: dict[str, Any]
```

Returned by `flux.info()`. Represents everything DataFlux knows about a dataset without downloading it.

| Field | Type | Description |
|---|---|---|
| `id` | `str \| int` | Provider-specific dataset identifier. |
| `name` | `str` | Dataset name. |
| `description` | `str \| None` | Dataset description or abstract, if the provider has one. |
| `instances` | `int \| None` | Row count, if known ahead of download. |
| `features` | `int \| None` | Column/feature count, if known ahead of download. |
| `tasks` | `list[str]` | Associated ML task types (e.g. `["Classification"]`), if the provider categorizes datasets this way. |
| `target` | `list[str]` | Target/label column name(s), if applicable. |
| `has_missing_values` | `bool \| None` | Whether the dataset has missing values, if known. |
| `provider` | `str` | Which provider this metadata came from. |
| `url` | `str \| None` | Link to the dataset's page on the source site, if one exists. |
| `extra` | `dict[str, Any]` | Anything provider-specific that doesn't map onto the standard fields above — the shape of this dict varies by provider. |

!!! note "Not every field is populated by every provider"
    A standardized shape doesn't mean every field is always filled in — some are legitimately `None` depending on the source. See the [Providers Overview](../providers/overview.md#what-varies-in-info) table for exactly which fields each of the nine providers populates.

**Example**

```python
info = flux.info(result)
print(info.instances, info.features, info.has_missing_values)
print(info.extra)  # provider-specific metadata
```

## Next step

See [Exceptions](exceptions.md) for what gets raised when a result or identifier is invalid, or [Base Provider](base-provider.md) for how providers construct these objects.
