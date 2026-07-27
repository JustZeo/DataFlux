from dataflux.models.dataset import DatasetInfo


def test_dataset_info_creation():
    info = DatasetInfo(
        id="iris",
        name="Iris",
        description="Classic Iris dataset.",
        instances=150,
        features=4,
        tasks=["Classification"],
        target=["setosa", "versicolor", "virginica"],
        has_missing_values=False,
        provider="sklearn",
        url="https://example.com",
        extra={"license": "BSD"},
    )

    assert info.id == "iris"
    assert info.name == "Iris"
    assert info.instances == 150
    assert info.features == 4
    assert info.provider == "sklearn"
    assert info.has_missing_values is False
    assert info.extra["license"] == "BSD"


def test_dataset_info_defaults():
    info = DatasetInfo(
        id="dummy",
        name="Dummy",
        description=None,
        instances=None,
        features=None,
        tasks=None,
        target=None,
        has_missing_values=None,
        provider="dummy",
        url=None,
        extra=None,
    )

    assert info.id == "dummy"
    assert info.name == "Dummy"
    assert info.description is None
    assert info.extra is None