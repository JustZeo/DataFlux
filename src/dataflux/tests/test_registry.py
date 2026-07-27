import pytest

from dataflux.exceptions import (
    InvalidProviderError,
    ProviderAlreadyRegisteredError,
    ProviderNotFoundError,
)
from dataflux.providers.base import BaseProvider
from dataflux.registry import ProviderRegistry


class DummyProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "dummy"

    def search(self, query):
        return []

    def info(self, dataset_id):
        return None

    def pull(self, dataset_id):
        return None


class EmptyNameProvider(BaseProvider):

    @property
    def name(self) -> str:
        return ""

    def search(self, query):
        return []

    def info(self, dataset_id):
        return None

    def pull(self, dataset_id):
        return None


class InvalidProvider:
    pass


# ============================================================================
# Register
# ============================================================================

def test_register_provider():
    registry = ProviderRegistry()
    provider = DummyProvider()

    registry.register(provider)

    assert registry.get("dummy") is provider


# ============================================================================
# Duplicate Registration
# ============================================================================

def test_duplicate_registration():
    registry = ProviderRegistry()
    provider = DummyProvider()

    registry.register(provider)

    with pytest.raises(ProviderAlreadyRegisteredError):
        registry.register(provider)


# ============================================================================
# Get Provider
# ============================================================================

def test_get_provider():
    registry = ProviderRegistry()
    provider = DummyProvider()

    registry.register(provider)

    assert registry.get("dummy") is provider


# ============================================================================
# Provider Not Found
# ============================================================================

def test_provider_not_found():
    registry = ProviderRegistry()

    with pytest.raises(ProviderNotFoundError):
        registry.get("unknown")


# ============================================================================
# Exists
# ============================================================================

def test_exists():
    registry = ProviderRegistry()
    provider = DummyProvider()

    registry.register(provider)

    assert registry.exists("dummy")
    assert not registry.exists("unknown")


# ============================================================================
# Providers List
# ============================================================================

def test_providers():
    registry = ProviderRegistry()

    provider = DummyProvider()

    registry.register(provider)

    providers = registry.providers()

    assert len(providers) == 1
    assert providers[0] is provider


# ============================================================================
# Invalid Provider Type
# ============================================================================

def test_invalid_provider():
    registry = ProviderRegistry()

    with pytest.raises(InvalidProviderError):
        registry.register(InvalidProvider())


# ============================================================================
# Empty Provider Name
# ============================================================================

def test_empty_provider_name():
    registry = ProviderRegistry()

    with pytest.raises(InvalidProviderError):
        registry.register(EmptyNameProvider())