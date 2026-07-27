# Caching

DataFlux has cache infrastructure in place, but — as of v0.1.0 — it's only fully wired into one provider. This page documents what exists today and what to expect as it expands.

---

## What's wired in today

### TorchVision

TorchVision is the only provider that currently uses DataFlux's cache directory end-to-end:

```
~/.dataflux/torchvision/
```

Repeated `pull()` calls for the same TorchVision dataset reuse this local copy rather than re-downloading.

### Everything else

- **Kaggle** relies on `kagglehub`'s own local cache (outside DataFlux's cache directory entirely). Repeated pulls are typically fast because of `kagglehub` itself, not because DataFlux manages it.
- **UCI, Hugging Face, and the remaining providers** currently re-fetch on every `pull()` call — there's no caching layer sitting in front of them yet.

---

## The cache infrastructure that exists

Two pieces of general-purpose caching machinery exist in the codebase, ready to be adopted more broadly:

### `dataflux.cache.Cache`

A generic JSON cache manager, rooted at `~/.dataflux/`:

```python
from dataflux.cache import cache

cache.write("search/iris", data)
cache.read("search/iris")
cache.exists("search/iris")
cache.delete("search/iris")
cache.clear()  # wipes the entire cache
```

### `dataflux.utils.filesystem` cache helpers

A second, separate set of path helpers rooted at `~/.cache/dataflux/`:

```python
from dataflux.utils.filesystem import cache_path, temp_path

cache_path("datasets", "iris")   # ~/.cache/dataflux/datasets/iris
temp_path("downloads")           # ~/.cache/dataflux/temp/downloads
```

!!! warning "Two separate cache roots exist today"
    `dataflux.cache.Cache` defaults to `~/.dataflux/`, while `dataflux.utils.filesystem.cache_path()` points at `~/.cache/dataflux/` — a different directory. Neither of these is currently called from provider `pull()` logic (aside from TorchVision using its own dedicated constant from `config.py`). If you're extending DataFlux and reaching for a cache helper, be aware these are two independent systems today, not one unified cache.

---

## Provider-specific cache directories (defined, not all wired in)

`config.py` reserves a cache subdirectory per provider under `~/.dataflux/`, and creates them on import:

```
~/.dataflux/
├── uci/
├── kaggle/
├── huggingface/
├── torchvision/    ← actually used today
└── tensorflow/
```

Only `torchvision/` is currently populated by provider logic. The others exist as reserved space for caching that hasn't been implemented yet.

---

## Manually clearing the cache

If you want to force a fresh pull for TorchVision datasets, delete its cache directory directly:

```bash
rm -rf ~/.dataflux/torchvision
```

or, from Python, via the general-purpose cache manager:

```python
from dataflux.cache import cache
cache.clear()  # clears everything under ~/.dataflux/
```

## Next step

[:octicons-arrow-right-24: Error Handling](error-handling.md) — the exception hierarchy, and how to catch specific failure modes.