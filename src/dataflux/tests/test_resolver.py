import pytest

from dataflux.providers.base import BaseProvider
from dataflux.registry import ProviderRegistry
from dataflux.resolver import Resolver
from dataflux.models.search_result import SearchResult
from dataflux.exceptions import (
    DatasetNotFoundError,
    ProviderNotFoundError,
)


class DummyProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "dummy"

    def search(self, query):
        if query.lower() == "iris":
            return [
                SearchResult(
                    id="iris",
                    name="Iris",
                    provider=self.name,
                )
            ]
        return []

    def info(self, dataset_id):
        return None

    def pull(self, dataset_id):
        return None


def test_resolve_dataset():
    registry = ProviderRegistry()
    registry.register(DummyProvider())

    resolver = Resolver(registry)

    results = resolver.resolve_dataset("iris")

    assert len(results) == 1
    assert results[0].name == "Iris"
    assert results[0].provider == "dummy"


def test_dataset_not_found():
    registry = ProviderRegistry()
    registry.register(DummyProvider())

    resolver = Resolver(registry)

    with pytest.raises(DatasetNotFoundError):
        resolver.resolve_dataset("unknown_dataset")


def test_resolve_provider():
    registry = ProviderRegistry()
    registry.register(DummyProvider())

    resolver = Resolver(registry)

    provider = resolver.resolve_provider("dummy")

    assert provider.name == "dummy"


def test_provider_not_found():
    registry = ProviderRegistry()

    resolver = Resolver(registry)

    with pytest.raises(ProviderNotFoundError):
        resolver.resolve_provider("unknown")