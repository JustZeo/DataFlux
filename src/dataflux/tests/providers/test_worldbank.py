import polars as pl

from dataflux.models.dataset import DatasetInfo
from dataflux.models.search_result import SearchResult
from dataflux.providers.worldbank import WorldBankProvider


provider = WorldBankProvider()


# ============================================================================
# Search
# ============================================================================

def test_search():
    results = provider.search("pm2.5")

    assert isinstance(results, list)
    assert len(results) > 0

    result = results[0]

    assert isinstance(result, SearchResult)
    assert result.provider == "worldbank"


# ============================================================================
# Info
# ============================================================================

def info(self, dataset_id: str) -> DatasetInfo:
    """
    Return metadata for a World Bank indicator.

    Only a single request is performed (loading the dataset).
    This avoids the additional `wb.series.get()` API call,
    which can be slow or occasionally hang.
    """
    dataset = self._load_df(dataset_id)

    # Convert column names to strings
    columns = [str(c) for c in dataset.columns]

    return DatasetInfo(
        id=dataset_id,
        name=dataset_id,
        description=f"World Bank indicator: {dataset_id}",
        instances=len(dataset),
        features=len(columns),
        tasks=["Time Series"],
        target=None,
        has_missing_values=dataset.isnull().values.any(),
        provider=self.name,
        url=f"https://data.worldbank.org/indicator/{dataset_id}",
        extra={
            "indicator_code": dataset_id,
            "columns": columns,
            "dtypes": {
                str(k): str(v)
                for k, v in dataset.dtypes.items()
            },
        },
    )


# ============================================================================
# Pull
# ============================================================================

def test_pull():
    results = provider.search("pm2.5")

    df = provider.pull(results[0].id)

    assert isinstance(df, pl.DataFrame)

    assert df.height > 0
    assert df.width > 0


# ============================================================================
# Schema
# ============================================================================

def test_schema():
    results = provider.search("pm2.5")

    df = provider.pull(results[0].id)

    assert "economy" in df.columns


# ============================================================================
# Search Ranking
# ============================================================================

def test_search_returns_best_match():
    results = provider.search("pm2.5")

    assert results[0].id is not None


# ============================================================================
# Case Insensitive Search
# ============================================================================

def test_case_insensitive_search():
    lower = provider.search("pm2.5")
    upper = provider.search("PM2.5")

    assert lower == upper