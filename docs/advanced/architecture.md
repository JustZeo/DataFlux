# Architecture

This page covers how DataFlux is put together internally — useful if you're debugging a provider, writing a new one, or just curious what happens between `flux.search("iris")` and a table on your screen.

---

## The pieces

```
Flux                    the public API (search / info / pull / export)
 ├── ProviderRegistry    holds every registered BaseProvider, keyed by name
 └── Resolver            turns a query or provider name into concrete results

BaseProvider             abstract contract every data source implements
 ├── UCIProvider
 ├── SKLearnProvider
 ├── KaggleProvider
 ├── HuggingFaceProvider
 ├── TorchVisionProvider
 ├── SeabornProvider
 ├── StatsModelsProvider
 ├── VegaDatasetsProvider
 └── WorldBankProvider

SearchResult / DatasetInfo   standardized data shapes returned by every provider
```

`Flux` (the class behind the `flux` singleton you import) owns exactly one `ProviderRegistry` and one `Resolver`, created in `Flux.__init__` and populated with all nine built-in providers at that point. Nothing about `Flux` is provider-specific — it delegates.

---

## Request flow

### `flux.search(query)`

1. `Flux.search()` calls `Resolver.resolve_dataset(query)`.
2. `Resolver` asks `ProviderRegistry.providers()` for every registered provider and calls `.search(query)` on each one, collecting results into a single list.
3. If nothing came back from any provider, `Resolver` raises `DatasetNotFoundError`.
4. Otherwise the combined list is passed to `dataflux.utils.search.rank()`, which sorts by relevance score, then provider priority (as a tiebreaker), then name.
5. `Flux.search()` optionally prints the ranked list via `display_search()`, then returns it.

### `flux.info(result)` / `flux.pull(result)`

1. `Flux` calls `Resolver.resolve_provider(result.provider)`.
2. `Resolver` looks the name up in `ProviderRegistry` — raising `ProviderNotFoundError` if it isn't registered.
3. The resolved provider's own `.info(result.id)` or `.pull(result.id)` is called directly. From here, everything is provider-specific: a live API request, a bundled JSON index lookup, or a third-party library call.

There's no cross-provider logic once resolution happens — each provider is fully responsible for its own `search`/`info`/`pull` implementations, as long as it returns the standardized `SearchResult`/`DatasetInfo` shapes.

---

## Why a registry + resolver, and not just a dict

Splitting `ProviderRegistry` (storage) from `Resolver` (lookup + orchestration) keeps two different concerns apart:

- `ProviderRegistry` only knows how to store and validate providers — register, get, check existence.
- `Resolver` knows the *policy* for turning a user-facing query or provider name into results — including what to do when nothing matches, and how to fan a query out across every provider.

This means the ranking algorithm, or the decision to raise `DatasetNotFoundError` on an empty result set, lives in one place (`Resolver`/`rank()`) rather than being duplicated across every provider or baked into `Flux` itself.

---

## Supporting modules

- **`dataflux.utils.search`** — `search_score()` (word-boundary vs. substring matching) and `rank()` (the cross-provider sort used by `Resolver`).
- **`dataflux.utils.download`** — thin `urllib`-based helpers (`download`, `download_json`, etc.) used by providers that hit raw URLs directly, like UCI.
- **`dataflux.utils.filesystem`** — path helpers (`resource_path()`, `cache_path()`, `ensure_dir()`) so providers don't hardcode paths to bundled resources or the cache directory.
- **`dataflux.utils.fingerprint`** — deterministic hashing (`fingerprint()`, `cache_key()`) used for building cache keys.
- **`dataflux.cache.Cache`** — generic JSON cache manager, independent of any single provider.
- **`dataflux.display`** — rendering only; `display_search()` and `display_info()` format results for the console and have no effect on what `search()`/`info()` return.

## Next step

See [Writing a Provider](writing-a-provider.md) to add a new data source, or [Providers Overview](../providers/overview.md) for how the nine built-in providers differ in practice.
