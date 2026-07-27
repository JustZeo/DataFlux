# Writing a Provider

A DataFlux provider is any class implementing the three-method `BaseProvider` contract: `search`, `pull`, and `info`. This page walks through building one end-to-end, using the real `UCIProvider` as a reference.

See [`BaseProvider`](../api-reference/base-provider.md) for the abstract signatures, and [Architecture](architecture.md) for how a provider fits into the rest of DataFlux once registered.

---

## The contract

```python
from dataflux.providers.base import BaseProvider

class MyProvider(BaseProvider):

    @property
    def name(self) -> str:
        ...

    def search(self, query: str) -> list[SearchResult]:
        ...

    def pull(self, dataset: str) -> pl.DataFrame:
        ...

    def info(self, dataset: str) -> DatasetInfo:
        ...
```

`name` must be a unique, non-empty, lowercase string — it's the key used everywhere: registry lookup, `SearchResult.provider`, `DatasetInfo.provider`, and the provider-priority tiebreaker in ranking.

---

## Step 1 — `search()`

Take a free-text query, score it against whatever catalog your source exposes, and return `SearchResult` objects for anything that matches.

```python
import json
import urllib.request

from dataflux.models.search_result import SearchResult
from dataflux.providers.base import BaseProvider
from dataflux.utils.search import search_score


class UCIProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "uci"

    def _datasets(self) -> list[dict]:
        with urllib.request.urlopen(API_LIST_URL) as response:
            payload = json.load(response)
        return payload["data"]

    def search(self, query: str) -> list[SearchResult]:
        matches = []

        for dataset in self._datasets():
            score = search_score(query, dataset["name"])

            if score == -1:
                continue

            matches.append((
                score,
                SearchResult(
                    id=dataset["id"],
                    name=dataset["name"],
                    provider=self.name,
                    relevance=score,
                ),
            ))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [result for _, result in matches]
```

Use `dataflux.utils.search.search_score(query, *texts)` to score candidates consistently with every other provider — it returns `2` for an exact word match, `1` for a substring match, `-1` for no match at all. Filter out `-1`, and set `relevance` on the `SearchResult` to whatever `search_score()` returned — this feeds into cross-provider ranking (see [Searching](../guide/searching.md)).

If your catalog is small and fixed (like scikit-learn's or Seaborn's), you can hardcode a list instead of hitting a network endpoint — see `SKLearnProvider` or `SeabornProvider` for that pattern. If it's large but doesn't change often, bundle a JSON index under `dataflux/resources/` and load it with `dataflux.utils.filesystem.resource_path()` — that's what `KaggleProvider` does.

---

## Step 2 — `info()`

Return a fully-populated `DatasetInfo`, leaving any field you can't populate as `None` (or an empty list/dict, matching the field's type).

```python
from dataflux.models.dataset import DatasetInfo

def info(self, dataset_id: int | str) -> DatasetInfo:
    dataset = fetch_ucirepo(id=int(dataset_id))
    meta = dataset.metadata

    return DatasetInfo(
        id=meta["uci_id"],
        name=meta["name"],
        description=meta["abstract"],
        instances=meta["num_instances"],
        features=meta["num_features"],
        tasks=meta["tasks"],
        target=meta["target_col"],
        has_missing_values=meta["has_missing_values"] == "yes",
        provider=self.name,
        url=meta["repository_url"],
        extra=meta,
    )
```

Put anything provider-specific that doesn't map cleanly onto the standard fields into `extra` — every built-in provider does this rather than dropping information on the floor.

Raise a `DataFluxError` subclass (e.g. `DatasetNotFoundError`) when the identifier doesn't resolve to anything — don't let a raw `KeyError` or `ValueError` escape. See [Error Handling](../guide/error-handling.md) for why this matters and a known exception to this rule in `KaggleProvider`.

---

## Step 3 — `pull()`

Return a `polars.DataFrame` — never pandas, never a provider-specific object.

```python
import polars as pl

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

If the underlying library only gives you pandas (as `ucimlrepo` does), convert with `pl.from_pandas()` before returning. This is the one hard rule every provider must follow — `Flux.pull()` and `flux.export()` both assume a Polars DataFrame downstream.

---

## Step 4 — register it

Providers aren't auto-discovered — register an instance inside `Flux.__init__` (in `dataflux/flux.py`):

```python
from dataflux.providers.myprovider import MyProvider

class Flux:
    def __init__(self):
        self._registry = ProviderRegistry()
        self._resolver = Resolver(self._registry)

        self._registry.register(UCIProvider())
        ...
        self._registry.register(MyProvider())
```

`ProviderRegistry.register()` raises `InvalidProviderError` if your class doesn't inherit from `BaseProvider` or has an empty `name`, and `ProviderAlreadyRegisteredError` if the name collides with one already registered.

---

## Checklist

- [ ] `name` is unique, lowercase, non-empty
- [ ] `search()` returns `SearchResult` objects with `relevance` set from `search_score()`
- [ ] `info()` returns a fully-shaped `DatasetInfo`, unknown fields left `None`
- [ ] `pull()` returns a `polars.DataFrame`, converting from pandas if needed
- [ ] Failure paths raise `DataFluxError` subclasses, not raw built-in exceptions
- [ ] Registered inside `Flux.__init__`
- [ ] Tests added under `dataflux/tests/providers/`, following the pattern in `test_uci.py`

## Next step

See [Contributing](contributing.md) for how to submit this as a pull request, or [Providers Overview](../providers/overview.md) to see how the nine built-in providers each made these tradeoffs differently.
