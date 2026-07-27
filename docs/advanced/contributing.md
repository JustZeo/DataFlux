# Contributing

Thanks for considering contributing to DataFlux. This page covers the project layout and the conventions the existing codebase follows — matching them makes a pull request much faster to review.

---

## Project layout

```
src/dataflux/
├── flux.py              Flux class + the `flux` singleton
├── registry.py          ProviderRegistry
├── resolver.py           Resolver
├── config.py             cache directory constants
├── cache.py              generic JSON Cache
├── export.py             export() and SUPPORTED_EXPORTS
├── exceptions.py         the full DataFluxError hierarchy
├── models/               DatasetInfo, SearchResult
├── providers/            BaseProvider + all nine built-in providers
├── display/               console rendering (search table, info panel)
├── utils/                 search scoring, download, filesystem, fingerprint
├── resources/             bundled data (e.g. kaggle_index.json)
└── tests/                 mirrors the package layout above
```

`docs/` is a separate top-level directory, organized as getting-started → guide → providers → advanced → api-reference — roughly the order a new user encounters each topic.

---

## Setting up

```bash
git clone https://github.com/JustZeo/DataFlux.git
cd DataFlux
pip install -e ".[dev]"
```

## Running tests

Tests live under `src/dataflux/tests/`, mirroring the source layout (`tests/providers/test_uci.py` tests `providers/uci.py`, and so on). Shared fixtures (like `iris_result`, `iris_df`, `sample_df`) live in `tests/conftest.py`.

```bash
pytest
pytest src/dataflux/tests/providers/test_uci.py   # a single file
pytest -k "search"                                  # by test name
```

Some provider tests hit live network endpoints (UCI, Hugging Face, Vega, World Bank) — expect those to be slower and occasionally flaky if the upstream source is unreachable.

---

## Code conventions

These aren't enforced by tooling in this repo yet, but every existing module follows them:

- **Every failure path raises a `DataFluxError` subclass.** Add a new one to `exceptions.py` under the relevant section header (Provider / Dataset / Search / Pull / Cache / Filesystem / Export Errors) rather than raising a bare built-in exception. See [Error Handling](../guide/error-handling.md) for why this matters, and the one known exception to this rule.
- **Providers return standardized shapes.** `search()` → `list[SearchResult]`, `info()` → `DatasetInfo`, `pull()` → `polars.DataFrame`. Never pandas, never a provider-specific object — convert with `pl.from_pandas()` if the underlying library only gives you pandas.
- **Provider-specific metadata goes in `DatasetInfo.extra`**, not into new top-level fields — the standardized shape is the whole point.
- **Use the existing `utils` helpers** rather than re-implementing them: `dataflux.utils.search.search_score()` for matching, `dataflux.utils.filesystem` for paths, `dataflux.utils.download` for raw HTTP.
- **Dataclasses use `slots=True`** (see `SearchResult`, `DatasetInfo`) — keep new models consistent with this.

---

## Adding a provider

See [Writing a Provider](writing-a-provider.md) for the full guide. In short: implement `BaseProvider`, register the instance inside `Flux.__init__`, and add tests under `tests/providers/` following the existing pattern (a module-level `provider = MyProvider()` instance, then `test_search`/`test_info`/`test_pull` functions).

## Adding documentation

Docs are Markdown, built with mkdocs-material (note the `=== "tab"` admonition syntax and `!!! note` callouts used throughout — see `docs/index.md` or `docs/guide/error-handling.md` for examples). Cross-link new pages from the relevant "Next step" section on the page before it, and from `docs/index.md` if it's a new top-level section.

## Submitting a pull request

1. Fork the repo and branch from `main`.
2. Keep the change focused — one provider, one fix, or one doc section per PR.
3. Add or update tests for anything behavioral.
4. Make sure `pytest` passes locally.
5. Open the PR against `JustZeo/DataFlux` with a description of what changed and why.

## Next step

See [Writing a Provider](writing-a-provider.md) if you're adding a new data source, or [Architecture](architecture.md) to understand how the pieces fit together before making a structural change.
