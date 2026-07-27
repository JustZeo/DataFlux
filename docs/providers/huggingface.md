# Hugging Face

The Hugging Face provider, backed by `huggingface_hub` and `datasets` — a live-queried source covering NLP and web-scale datasets.

---

## Search source

`search()` queries the Hugging Face Hub API directly, capped at 20 results per query:

```python
def search(self, query: str) -> list[SearchResult]:
    datasets = self.api.list_datasets(search=query, limit=20)
    ...
```

Because this hits HF's live API, results reflect the current state of the Hub — including recently published datasets — unlike DataFlux's fixed/bundled providers.

!!! note "Result cap"
    Only the first 20 matches from the Hub API are considered per search. For a very broad query, this means DataFlux's Hugging Face results are a narrower slice than what you'd see browsing huggingface.co directly.

## Result format

```python
results = flux.search("imdb", display=False)
hf_result = next(r for r in results if r.provider == "huggingface")

print(hf_result.id)    # "stanfordnlp/imdb" — full HF repo id (owner/name)
print(hf_result.name)  # "Imdb" — derived from the repo name, title-cased
```

`SearchResult.description` is always `None` for Hugging Face results at the search stage — full descriptions are only fetched by `info()`.

## `pull()`

```python
def pull(self, dataset_id: str):
    dataset = load_dataset(dataset_id)
    if hasattr(dataset, "keys"):
        dataset = dataset[list(dataset.keys())[0]]
    return dataset.to_polars()
```

Many HF datasets are split into multiple subsets (`train`, `test`, `validation`, etc.) — `pull()` takes the **first split returned**, not necessarily `train`. If you need a specific split, this is a current limitation to be aware of; there's no way to request a particular split through `pull()` today.

## `info()`

Hugging Face's metadata richness varies a lot by dataset — some fields depend entirely on whether the dataset's card includes structured `dataset_info`:

```python
info = flux.info(hf_result)

info.instances   # populated only if the dataset card has `dataset_info.splits`, else None
info.features    # populated only if the dataset card has `dataset_info.features`, else None
info.tasks       # populated only if the card lists `task_categories`, else None
info.target      # always None
info.url         # always populated — constructed from the dataset id
info.extra       # author, tags, downloads, likes, created_at, last_modified
```

!!! note "Metadata quality depends on the dataset card"
    Unlike UCI (where every field is reliably populated) or scikit-learn (where fields are consistent by design), Hugging Face's `info()` output quality depends entirely on how well the individual dataset's card is filled out on the Hub. Sparse or poorly documented datasets will return mostly `None` for `instances`/`features`/`tasks`.