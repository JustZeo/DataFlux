import polars as pl

from dataflux.models.dataset import DatasetInfo
from dataflux.models.search_result import SearchResult
from dataflux.providers.torchvision import TorchVisionProvider


provider = TorchVisionProvider()


# ============================================================================
# Search
# ============================================================================

def test_search():
    results = provider.search("mnist")

    assert isinstance(results, list)
    assert len(results) > 0

    result = results[0]

    assert isinstance(result, SearchResult)
    assert result.provider == "torchvision"

    assert result.id == "mnist"
    assert result.name == "Mnist"


# ============================================================================
# Info
# ============================================================================

def test_info():
    info = provider.info("mnist")

    assert isinstance(info, DatasetInfo)

    assert info.provider == "torchvision"
    assert info.id == "mnist"
    assert info.name == "Mnist"

    assert info.instances > 0
    assert info.tasks == ["Image Classification"]


# ============================================================================
# Pull
# ============================================================================

def test_pull():
    df = provider.pull("mnist")

    assert isinstance(df, pl.DataFrame)

    assert df.height > 0
    assert df.width == 2


# ============================================================================
# Metadata
# ============================================================================

def test_metadata():
    info = provider.info("mnist")

    assert "image_shape" in info.extra
    assert "num_classes" in info.extra
    assert "class_to_idx" in info.extra


# ============================================================================
# Search Ranking
# ============================================================================

def test_search_returns_best_match():
    results = provider.search("mnist")

    assert results[0].id == "mnist"


# ============================================================================
# Case Insensitive Search
# ============================================================================

def test_case_insensitive_search():
    lower = provider.search("mnist")
    upper = provider.search("MNIST")

    assert lower == upper