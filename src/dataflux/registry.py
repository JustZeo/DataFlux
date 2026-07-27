from dataflux.providers.base import BaseProvider
from dataflux.exceptions import (
    InvalidProviderError,
    ProviderAlreadyRegisteredError,
    ProviderNotFoundError
)

class ProviderRegistry:

    def __init__(self):
        self._providers: dict[str, BaseProvider] = {}

    def register(self, provider: BaseProvider) -> None:
        if not isinstance(provider,BaseProvider):
           raise InvalidProviderError(
                "Provider must inherit from BaseProvider."
           )
        if not provider.name:
           raise InvalidProviderError(
               "Provider name cannot be empty"
           )
        if provider.name in self._providers:
            raise ProviderAlreadyRegisteredError(provider.name)

        self._providers[provider.name] = provider

    def get(self, name: str) -> BaseProvider:
        if name not in self._providers:
            raise ProviderNotFoundError(
                f"Provider '{name}' not found "
            )
        return self._providers[name]

    def exists(self, name: str) -> bool:
        return name in self._providers

    def providers(self) -> list[BaseProvider]:
        return list(self._providers.values())