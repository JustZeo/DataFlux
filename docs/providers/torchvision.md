# TorchVision

The TorchVision provider — a hand-maintained registry of well-known vision datasets, and the only provider that currently uses DataFlux's own cache directory end-to-end.

---

## Search source

`search()` matches against a fixed, bundled registry of dataset names (`TORCHVISION_DATASETS`) mapping to their corresponding `torchvision.datasets` classes (e.g. MNIST, CIFAR-10/100, FashionMNIST):

```python
def search(self, query: str) -> list[SearchResult]:
    for dataset in TORCHVISION_DATASETS:
        score = search_score(query, dataset)
        ...
```

No network call happens during `search()` — the registry is static and bundled with DataFlux.

## Result format

```python
results = flux.search("mnist", display=False)
tv_result = next(r for r in results if r.provider == "torchvision")

print(tv_result.id)    # "mnist" — the internal registry key
print(tv_result.name)  # "Mnist" — title-cased for display
```

## Caching — the one provider that's fully wired in

```python
def _load_dataset(self, dataset_id: str):
    return TORCHVISION_DATASETS[dataset_id](
        root=TORCHVISION_CACHE,
        download=True,
    )
```

`TORCHVISION_CACHE` points at `~/.dataflux/torchvision/`. The first `pull()` (or `info()`, since both call `_load_dataset()`) downloads the dataset to this directory; subsequent calls reuse the local copy instead of re-downloading. This is currently the **only** provider with this behavior wired in — see [Caching](../guide/caching.md) for the full picture across all nine providers.

## `pull()`

```python
def pull(self, dataset_id: str) -> pl.DataFrame:
    dataset = self._load_dataset(dataset_id)
    return pl.DataFrame({
        "image": dataset.data.numpy().tolist(),
        "label": dataset.targets.numpy().tolist(),
    })
```

!!! warning "Image data as nested lists, not a typical tabular shape"
    Unlike every other provider, TorchVision's `pull()` returns a DataFrame where the `image` column contains raw pixel data as nested Python lists (converted from numpy arrays via `.tolist()`), not scalar values. This is a fundamentally different shape from the row-per-record tabular data every other provider returns — expect to reshape or reconstruct images from this column yourself rather than treating it like a typical tabular column. Large vision datasets will also produce very large DataFrames this way, since each row embeds a full image as nested data.

## `info()`

```python
info = flux.info(tv_result)

info.instances            # len(dataset)
info.features               # always None
info.tasks                  # always ["Image Classification"]
info.target                 # class names, if the dataset exposes `.classes`
info.has_missing_values    # always False
info.url                    # always None
info.extra                  # image_shape, num_classes, class_to_idx
```

!!! note "`info()` triggers a full download too"
    Because `info()` calls the same `_load_dataset()` method as `pull()`, requesting info on a TorchVision dataset you haven't pulled yet will trigger the same download (and populate the same cache) as calling `pull()` directly. There's no lightweight metadata-only path for this provider.