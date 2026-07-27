# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-27

### Added
- **Core API (`flux.py`)**: `flux` singleton exposing high-level methods: `search`, `info`, `pull`, and `export`.
- **Data Processing**: Native integration with Polars (`pl.DataFrame`) for all dataset loading and export operations.
- **Providers**: Built-in providers for:
  - HuggingFace (`datasets`, `huggingface_hub`)
  - Kaggle (`kaggle`, `kagglehub`)
  - Scikit-learn
  - Seaborn
  - Statsmodels
  - TorchVision
  - UCI Machine Learning Repository (`ucimlrepo`)
  - Vega Datasets
  - World Bank (`wbgapi`)
- **Data Models (`models/`)**: Standardized representations using modern Python `dataclasses`:
  - `SearchResult`: Summary metadata from provider searches.
  - `DatasetInfo`: Detailed dataset metadata (features, instances, missing values).
- **Caching System (`cache.py`)**: Automatic JSON-based disk cache (defaulting to `~/.cache/dataflux/`) to minimize redundant network requests.
- **Exception Hierarchy (`exceptions.py`)**: Comprehensive custom exception types for detailed error handling across Providers, Datasets, Search, Pulling, Caching, and Exporting.
- **Type Hinting**: Extensive use of modern Python type hints and strict keyword-only arguments (`*`) for cleaner API usage.
- **Documentation**: Initial comprehensive documentation structure.