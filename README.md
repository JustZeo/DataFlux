# DataFlux

**One API. Every dataset.**

DataFlux is a universal dataset library for Python. Instead of learning a different package, auth flow, and return type for every dataset source, you interact with one consistent interface — `search()`, `info()`, `pull()` — and DataFlux handles the rest.

```python
from dataflux import flux

results = flux.search("iris")
info = flux.info(results[0])
df = flux.pull(results[0])
```

Whether the dataset lives on scikit-learn, UCI, Kaggle, Hugging Face, TorchVision, Seaborn, Statsmodels, Vega, or the World Bank — you never have to care. You get back the same shapes every time: a list of `SearchResult`, a `DatasetInfo`, and a `polars.DataFrame`.

---

## Why DataFlux

Every dataset provider does things differently:

```python
# scikit-learn
from sklearn.datasets import load_iris
iris = load_iris(as_frame=True)

# UCI
from ucimlrepo import fetch_ucirepo
iris = fetch_ucirepo(id=53)

# Hugging Face
from datasets import load_dataset
dataset = load_dataset(...)

# Kaggle
# requires auth, zip downloads, manual extraction...
```

Different function names, different auth requirements, different metadata formats, different return types. DataFlux hides all of that behind one contract:

```python
results = flux.search("housing")
info = flux.info(results[0])
df = flux.pull(results[0])
```

---

## Installation

```bash
pip install dataflux-core
```

or, if you're using [uv](https://github.com/astral-sh/uv):

```bash
uv add dataflux-core
```

---

## Quick Start

```python
from dataflux import flux

# Search across every registered provider at once
flux.search("housing")

# Get results without the pretty console output
results = flux.search("housing", display=False)

# Inspect a dataset before committing to a download
flux.info(results[0])

# Pull the dataset as a Polars DataFrame
df = flux.pull(results[0])

# Export it to disk in whatever format you need
flux.export(df, "housing.csv")
```

---

## Core Concepts

### `search(query, *, raw=False, display=True, limit=10)`

Searches every registered provider for the query, merges and ranks the results, and returns a `list[SearchResult]`.

- **`display`** — when `True` (default), prints a formatted, colorized table via `rich`. Set to `False` to search silently (e.g. inside a script or pipeline).
- **`raw`** — when `True`, skips the pretty output entirely regardless of `display`.
- **`limit`** — caps how many results are shown in the pretty table (default `10`). The full, unranked result set is still returned; only the *displayed* table is capped.

Results are ranked across providers so that curated, canonical sources (like scikit-learn and UCI) surface above noisier, crowd-sourced sources (like Kaggle) for the same query.

If nothing matches, `search()` raises `DatasetNotFoundError` rather than silently returning an empty list.

```python
results = flux.search("iris")
```

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

### `info(result, *, raw=False, display=True)`

Takes a `SearchResult` and returns a `DatasetInfo` describing it — row/feature counts, tasks, target columns, missing-value status, license/URL, and any provider-specific extras.

```python
info = flux.info(results[0])
```

### `pull(result)`

Takes a `SearchResult` and returns a `polars.DataFrame` with the actual dataset loaded into memory. Every provider — regardless of its native format (pandas, CSV, JSON, image folders, etc.) — is normalized into the same Polars shape.

```python
df = flux.pull(results[0])
```

### `export(df, path, *, overwrite=False, mkdir=True)`

Writes a Polars DataFrame to disk. The format is inferred from the file extension.

```python
flux.export(df, "housing.csv")
flux.export(df, "housing.parquet")
flux.export(df, "nested/housing.json", overwrite=True)
```

Supported extensions: `.csv`, `.parquet`, `.json`, `.ndjson`, `.ipc`, `.feather`, `.arrow`.

---

## Data Models

Every provider returns the exact same two data shapes, so downstream code never has to branch on provider.

### `SearchResult`

```python
@dataclass(slots=True)
class SearchResult:
    id: str
    name: str
    provider: str
    description: str | None = None
    relevance: int = 0
```

### `DatasetInfo`

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

---

## Supported Providers

| Provider | Category | Notes |
|---|---|---|
| **UCI** | Classical ML benchmarks | Live search against the UCI ML Repository API |
| **scikit-learn** | Toy datasets & tabular baselines | Bundled, always available offline |
| **Kaggle** | Community & competition datasets | Uses a periodically refreshed **offline index** — no login required (see below) |
| **Hugging Face** | NLP & web-scale datasets | Live search via the HF Hub |
| **TorchVision** | Computer vision datasets | Hand-maintained registry of well-known vision datasets |
| **Seaborn** | Statistical & visualization datasets | Small, fixed catalog |
| **Statsmodels** | Econometrics & time series | Small, fixed catalog |
| **Vega** | Data visualization benchmarks | Small, fixed catalog |
| **World Bank** | Global economic & social indicators | Country/time-series indicator data |

### A note on Kaggle

Kaggle's dataset **search** API requires authentication even for public datasets — but DataFlux's core promise is that no provider should force you to log in just to discover what's available. To honor that, `KaggleProvider` ships with a **bundled, periodically refreshed offline index** instead of hitting Kaggle's live search endpoint. `pull()` still downloads the actual dataset live and auth-free, since Kaggle's public download endpoint doesn't gate on login.

The tradeoff: Kaggle search results are only as fresh as the last index refresh (updated on a recurring schedule via CI), not real-time. Every other provider's search is fully live.

If you specifically need live, up-to-the-minute Kaggle search, that's a deliberate scope decision left open for a future opt-in mode — not something DataFlux does by default.

---

## Provider Architecture

Every provider is independent and implements the same three-method contract:

```python
class BaseProvider(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique provider name."""

    @abstractmethod
    def search(self, query: str) -> list[SearchResult]:
        """Search datasets."""

    @abstractmethod
    def info(self, dataset: str) -> DatasetInfo:
        """Return dataset metadata."""

    @abstractmethod
    def pull(self, dataset: str) -> pl.DataFrame:
        """Download the requested dataset and return it as a DataFrame."""
```

Providers are registered once, at startup, via a `ProviderRegistry`:

```python
self._registry.register(UCIProvider())
self._registry.register(SKLearnProvider())
self._registry.register(KaggleProvider())
self._registry.register(HuggingFaceProvider())
self._registry.register(TorchVisionProvider())
self._registry.register(SeabornProvider())
self._registry.register(StatsModelsProvider())
self._registry.register(VegaDatasetsProvider())
self._registry.register(WorldBankProvider())
```

A `Resolver` sits on top of the registry and handles two jobs:

- **`resolve_dataset(query)`** — fans a query out to every registered provider, merges the results, and ranks them (curated sources like UCI/scikit-learn are weighted above crowd-sourced sources like Kaggle for the same query).
- **`resolve_provider(name)`** — looks up a specific provider by name (used internally by `info()`/`pull()` to route a `SearchResult` back to the provider that produced it).

Adding a new provider means writing one class that implements `search()`/`info()`/`pull()` and registering it — nothing else in the library needs to change.

---

## Why Polars

DataFlux is Polars-first. Every dataset, regardless of source format, is normalized into a `polars.DataFrame`:

- Faster loading, lower memory usage than pandas for most workloads
- One consistent dataframe API across every provider
- Seamless handoff into other Polars-based tooling (e.g. [QualityClean](https://pypi.org/project/qualityclean/))

```python
import dataflux as flux
import qualityclean as qc

df = flux.pull(flux.search("housing")[0])
clean_df = qc.clean(df)
```

---

## Error Handling

DataFlux raises specific, catchable exceptions rather than leaking raw provider errors:

```python
from dataflux.exceptions import (
    DataFluxError,             # base exception for everything below
    ProviderNotFoundError,
    DatasetNotFoundError,
    InvalidDatasetError,
    DatasetLoadError,
    SearchError,
    EmptySearchQueryError,
    PullError,
    DownloadError,
    CacheError,
    FileSystemError,
    ExportError,
    UnsupportedExportFormatError,
    ExportFileExistsError,
    InvalidExportDataError,
)
```

```python
from dataflux import flux
from dataflux.exceptions import DatasetNotFoundError

try:
    flux.search("something that doesn't exist anywhere")
except DatasetNotFoundError:
    print("No matches across any provider.")
```

---

## Caching

DataFlux caches provider downloads locally under `~/.dataflux/`, namespaced per provider:

```
~/.dataflux/
├── uci/
├── kaggle/
├── huggingface/
├── torchvision/
└── tensorflow/
```

Repeated `pull()` calls for the same dataset avoid re-downloading where the provider supports it.

---

## Project Status

DataFlux is at **v0.1.0** — all nine planned providers for this release are implemented and passing their own test suite (`tests/providers/`), alongside tests for the registry, resolver, models, display layer, and shared utilities (filesystem, caching, hashing/fingerprinting, download).

### Roadmap

- [x] Provider contract (`BaseProvider`, `SearchResult`, `DatasetInfo`)
- [x] UCI, scikit-learn, Kaggle, Hugging Face, TorchVision, Seaborn, Statsmodels, Vega, World Bank providers
- [x] Ranked, multi-provider search
- [x] `export()` to CSV/Parquet/JSON/NDJSON/IPC/Feather/Arrow
- [x] Pretty (`rich`-based) console output for `search()`/`info()`
- [ ] Additional providers (TensorFlow Datasets, Zenodo, government open-data portals, local/custom datasets)
- [ ] Optional authenticated live-search mode for Kaggle
- [ ] Expanded documentation site

### Design Principles

- One API for every dataset source — no provider-specific code required from the user.
- No provider should require authentication to search or discover data by default.
- Provider-agnostic architecture — adding a new source never touches existing ones.
- Polars-first for consistent, high-performance data handling.
- Standardized metadata (`SearchResult`, `DatasetInfo`) across every provider.
- Fail loudly and specifically (typed exceptions) rather than leaking raw provider errors.

---

## License

*(add your chosen license here — MIT, Apache-2.0, etc.)*

## Contributing

*(add contribution guidelines here once ready to accept external PRs)*