from dataflux.models.dataset import DatasetInfo
from dataflux.models.search_result import SearchResult


def test_dataset_info():
    info = DatasetInfo(
        id="iris",
        name="Iris",
        description=None,
        instances=150,
        features=4,
        tasks=None,
        target=None,
        has_missing_values=False,
        provider="sklearn",
        url=None,
        extra={},
    )

    assert info.id == "iris"


def test_search_result():
    result = SearchResult(
        id="iris",
        name="Iris",
        provider="sklearn",
    )

    assert result.provider == "sklearn"