from dataflux.providers.base import BaseProvider
from dataflux.models.search_result import SearchResult
from dataflux.models.dataset import DatasetInfo
from dataflux.resources.sklearn_dataset import SKLEARN_DATASETS
from dataflux.utils.search import search_score
import polars as pl


class SKLearnProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "sklearn"

    def _load_dataset(self, dataset_id: str, *, as_frame: bool = False):
        loader = SKLEARN_DATASETS[dataset_id]
        return loader(as_frame=as_frame) if as_frame else loader()

    def search(self, query: str) -> list[SearchResult]:
        matches: list[tuple[int, SearchResult]] = []

        for dataset in SKLEARN_DATASETS:
            score = search_score(query, dataset)

            if score == -1:
                continue

            matches.append(
                (
                    score,
                    SearchResult(
                        id=dataset,
                        name=dataset.replace("_", " ").title(),
                        provider=self.name,
                        relevance=score
                    ),
                )
            )

        matches.sort(key=lambda x: x[0], reverse=True)

        return [result for _, result in matches]

    def info(self, dataset_id: str) -> DatasetInfo:
        dataset = self._load_dataset(dataset_id)

        return DatasetInfo(
            id=dataset_id,
            name=dataset_id.replace("_", " ").title(),
            description=dataset.DESCR,
            instances=dataset.data.shape[0],
            features=dataset.data.shape[1],
            tasks=None,
            target=list(dataset.target_names),
            has_missing_values=False,
            provider=self.name,
            url=None,
            extra={
                "feature_names": dataset.feature_names,
                "filename": dataset.filename,
                "data_module": dataset.data_module,
            },
        )

    def pull(self, dataset_id: str) -> pl.DataFrame:
        dataset = self._load_dataset(dataset_id, as_frame=True)
        return pl.from_pandas(dataset.frame)