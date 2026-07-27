from dataflux.providers.base import BaseProvider
from dataflux.models.search_result import SearchResult
from dataflux.models.dataset import DatasetInfo
from dataflux.utils.search import search_score
from vega_datasets import data
import polars as pl


class VegaDatasetsProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "vega"

    def _load_df(self, dataset_id: str):
        return data(str(dataset_id).replace("-", "_"))

    def search(self, query: str) -> list[SearchResult]:
        matches: list[tuple[int, SearchResult]] = []

        for dataset in data.list_datasets():
            score = search_score(query, dataset)

            if score == -1:
                continue

            matches.append(
                (
                    score,
                    SearchResult(
                        id=dataset,
                        name=dataset.replace("_", " ").replace("-", " ").title(),
                        provider=self.name,
                        relevance=score
                    ),
                )
            )

        matches.sort(key=lambda x: x[0], reverse=True)

        return [result for _, result in matches]

    def info(self, dataset_id: str | int) -> DatasetInfo:
        dataset = self._load_df(dataset_id)

        return DatasetInfo(
            id=dataset_id,
            name=str(dataset_id).replace("_", " ").replace("-", " ").title(),
            description=None,
            instances=dataset.shape[0],
            features=dataset.shape[1],
            tasks=None,
            target=None,
            has_missing_values=dataset.isnull().values.any(),
            provider=self.name,
            url=None,
            extra={
                "columns": list(dataset.columns),
                "dtypes": {k: str(v) for k, v in dataset.dtypes.items()},
            },
        )

    def pull(self, dataset_id: str | int) -> pl.DataFrame:
        return pl.from_pandas(self._load_df(dataset_id))