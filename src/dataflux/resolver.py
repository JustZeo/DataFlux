from dataflux.registry import ProviderRegistry
from dataflux.exceptions import ProviderNotFoundError , DatasetNotFoundError
from dataflux.models.search_result import SearchResult
from dataflux.utils.search import rank
class Resolver:

    def __init__(self, registry: ProviderRegistry):
        self._registry = registry

    def resolve_provider(self, source: str):
        if not source:
            return None
        if not self._registry.exists(source):
            raise ProviderNotFoundError(
                f"Provider '{source} not found' "
            )
        return self._registry.get(source)


    def resolve_dataset(self,query:str)-> list[SearchResult]:
        providers = self._registry.providers()
        results=[]
        for provider in providers:
            providers_result = provider.search(query)
            results.extend(providers_result)
        if not results:
            raise DatasetNotFoundError(
                f"Dataset '{query}' not found"
            )
        return rank(results)