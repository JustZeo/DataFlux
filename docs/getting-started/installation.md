# Installation

## Requirements

- Python 3.10 or later
- No accounts, API keys, or authentication required for any provider — including Kaggle

## Install with pip

```bash
pip install dataflux
```

## Install with uv

```bash
uv add dataflux
```

## Verify it worked

```python
import dataflux
print(dataflux.version)
```

```
0.1.0
```

## Optional: provider-specific extras

DataFlux normalizes every provider's output into a `polars.DataFrame`, but a couple of providers rely on their own underlying package to actually fetch data. These are installed automatically as dependencies of `dataflux`, so in most cases you don't need to do anything extra. They're listed here only so you know what's happening under the hood:

| Provider | Underlying package |
|---|---|
| UCI | `ucimlrepo` |
| scikit-learn | `scikit-learn` |
| Kaggle | `kagglehub` (used only by `pull()` — `search()` uses a bundled offline index, no package or auth needed) |
| Hugging Face | `huggingface_hub` / `datasets` |
| TorchVision | `torchvision` |
| Seaborn | `seaborn` |
| Statsmodels | `statsmodels` |
| Vega | `vega_datasets` |
| World Bank | none — queried directly over HTTP |

!!! note "No login required, anywhere"
    Unlike using these providers directly, DataFlux never asks you to create an account, generate an API key, or authenticate — for any provider, including Kaggle. See [Providers Overview](../providers/overview.md) for how this works.

## Next step

[:octicons-arrow-right-24: Quickstart](quickstart.md) — run your first search, pull a dataset, and export it, in under a minute.