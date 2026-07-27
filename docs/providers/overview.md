# Providers Overview

DataFlux ships with nine providers in v0.1.0. Every one of them implements the same three-method contract (`search`, `info`, `pull`) — see [Writing a Provider](../advanced/writing-a-provider.md) for the interface itself. This page covers what each provider actually searches against, how live or static its data is, and what to expect from `info()`.

---

## At a glance

| Provider | Category | Search source | Requires auth? |
|---|---|---|---|
| [scikit-learn](sklearn.md) | Toy datasets & tabular baselines | Fixed, bundled list of dataset names | No |
| [UCI](uci.md) | Classical ML benchmarks | Live query to the UCI ML Repository API | No |
| [Kaggle](kaggle.md) | Community & competition datasets | Bundled offline index (refreshed periodically) | No — even for `pull()` |
| [Hugging Face](huggingface.md) | NLP & web-scale datasets | Live query to the HF Hub API | No |
| [TorchVision](torchvision.md) | Computer vision datasets | Fixed, hand-maintained registry of dataset classes | No |
| [Seaborn](seaborn.md) | Statistical & visualization datasets | Fixed, bundled list of dataset names | No |
| [Statsmodels](statsmodels.md) | Econometrics & time series | Fixed, bundled list of dataset names | No |
| [Vega](vega.md) | Data visualization benchmarks | Live enumeration via `vega_datasets.data.list_datasets()` | No |
| [World Bank](worldbank.md) | Global economic & social indicators | Live query to the World Bank indicator API | No |

**No provider requires authentication for `search()` or `pull()`, by design.** This is a core commitment of DataFlux, not an accident — see the [Kaggle](kaggle.md) page for how this holds even for a provider whose native API normally requires a login.

---

## Two different kinds of "search"

Providers fall into two groups depending on how their catalog is discovered:

### Live-queried providers
UCI, Hugging Face, Vega, and World Bank hit a real endpoint or library call every time you search — results reflect whatever exists on the source right now.

### Fixed/bundled providers
scikit-learn, Kaggle, TorchVision, Seaborn, and Statsmodels search against a list that ships with DataFlux itself (either a small hardcoded set of dataset names, or — for Kaggle specifically — a larger periodically-refreshed JSON index). These are instant and offline, but only as current as the last time that list was updated.

This distinction matters if you're searching for something obscure or very recently published — a fixed/bundled provider won't know about it until its list is refreshed, while a live-queried provider will.

---

## How results are ranked across all nine

See [Searching](../guide/searching.md) for the full breakdown, but in short: relevance to your query dominates the score, and provider priority only breaks ties between equally-relevant results. The priority order used as a tiebreaker is:

```
sklearn (100) > uci (95) > torchvision (90) > huggingface (80)
> kaggle (70) > statsmodels (60) > seaborn (50) > vega (40) > worldbank (30)
```

Curated, single-canonical-entry sources are weighted above crowd-sourced ones — but only when the match quality is otherwise equal.

---

## What varies in `info()`

Not every provider can populate every `DatasetInfo` field — the standardized shape exists so your code never has to check which provider a result came from, but some fields will legitimately be `None` depending on the source:

| Provider | `tasks` | `target` | `has_missing_values` | `url` |
|---|---|---|---|---|
| scikit-learn | `None` | populated | always `False` | `None` |
| UCI | populated | populated | populated | populated |
| Kaggle | `None` | `None` | `None` | populated |
| Hugging Face | sometimes populated | `None` | `None` | populated |
| TorchVision | `["Image Classification"]` | class names | always `False` | `None` |
| Seaborn | `None` | `None` | populated | `None` |
| Statsmodels | `None` | `None` | populated | `None` |
| Vega | `None` | `None` | populated | `None` |
| World Bank | `None` | `None` | populated | populated |

Anything not captured by the standard fields is available in `DatasetInfo.extra` — check the individual provider page for what each one puts there.

## Next step

Pick a provider to read about in depth, or start with [Kaggle](kaggle.md) — it's the one with the most interesting design tradeoff (an offline index instead of live search, to avoid requiring authentication).