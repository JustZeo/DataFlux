import polars as pl

from dataflux.models.dataset import DatasetInfo
from dataflux.models.search_result import SearchResult
from dataflux.providers.seaborn import SeabornProvider


provider = SeabornProvider()


# ============================================================================
# Search
# ============================================================================

def test_search():
    results = provider.search("iris")

    assert isinstance(results, list)
    assert len(results) > 0

    result = results[0]

    assert isinstance(result, SearchResult)
    assert result.provider == "seaborn"
    assert result.id == "iris"
    assert result.name == "Iris"


# ============================================================================
# Info
# ============================================================================

def test_info():
    info = provider.info("iris")

    assert isinstance(info, DatasetInfo)

    assert info.id == "iris"
    assert info.name == "Iris"

    assert info.instances == 150
    assert info.features == 5

    assert info.provider == "seaborn"


# ============================================================================
# Pull
# ============================================================================

def test_pull():
    df = provider.pull("iris")

    assert isinstance(df, pl.DataFrame)

    assert df.height == 150
    assert df.width == 5


# ============================================================================
# Schema
# ============================================================================

def test_schema():
    df = provider.pull("iris")

    assert df.schema["species"] == pl.String


# ============================================================================
# Search Ranking
# ============================================================================

def test_search_returns_best_match():
    results = provider.search("iris")

    assert results[0].id == "iris"


# ============================================================================
# Case Insensitive Search
# ============================================================================

def test_case_insensitive_search():
    lower = provider.search("iris")
    upper = provider.search("IRIS")

    assert lower == upper