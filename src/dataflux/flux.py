from dataflux.models.search_result import SearchResult
from dataflux.registry import ProviderRegistry
from dataflux.resolver import Resolver
from dataflux.providers.uci import UCIProvider
from dataflux.models.dataset import DatasetInfo
from dataflux.providers.sklearn import SKLearnProvider
from dataflux.providers.kaggle import KaggleProvider
from dataflux.providers.huggingface import HuggingFaceProvider
from dataflux.providers.torchvision import TorchVisionProvider
from dataflux.providers.seaborn import SeabornProvider
from dataflux.providers.statsmodels import StatsModelsProvider
from dataflux.providers.vega_datasets import VegaDatasetsProvider
from dataflux.providers.worldbank import WorldBankProvider
from dataflux.display.search import display_search
from dataflux.display.info import display_info 
from dataflux.export import export
import polars as pl

class Flux:

    def __init__(self):
        self._registry = ProviderRegistry()
        self._resolver = Resolver(self._registry)

        self._registry.register(UCIProvider())
        self._registry.register(SKLearnProvider())
        self._registry.register(KaggleProvider())
        self._registry.register(HuggingFaceProvider())
        self._registry.register(TorchVisionProvider())
        self._registry.register(SeabornProvider())
        self._registry.register(StatsModelsProvider())
        self._registry.register(VegaDatasetsProvider())
        self._registry.register(WorldBankProvider())

    def search(self, query: str,*,raw:bool=False,display:bool=True,limit:int | None=10) -> list[SearchResult]:
        results = self._resolver.resolve_dataset(query)
        if display and not raw:
            display_search(results,limit)
        return results


    def info(self,result:SearchResult,*,raw:bool=False,display:bool=True)-> DatasetInfo:
        provider = self._resolver.resolve_provider(result.provider)
        if display and not raw:
            display_info(provider.info(result.id))
        return provider.info(result.id)

    def pull(self,result:SearchResult)->pl.DataFrame:
        provider = self._resolver.resolve_provider(result.provider)
        return provider.pull(result.id)

    def export(self,df:pl.DataFrame,path:str,**kwargs,):
        return export(df,path,**kwargs)

flux = Flux()