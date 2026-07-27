import json
from pathlib import Path

import kagglehub
import polars as pl
from kagglehub import KaggleDatasetAdapter

from dataflux.models.dataset import DatasetInfo
from dataflux.models.search_result import SearchResult
from dataflux.providers.base import BaseProvider
from dataflux.utils.search import search_score


class KaggleProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "kaggle"

    def _load_index(self) -> list[dict]:
        with open(
            Path(__file__).parent.parent / "resources" / "kaggle_index.json",
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    def search(self, query: str) -> list[SearchResult]:
        matches: list[tuple[int, SearchResult]] = []

        for dataset in self._load_index():
            score = search_score(
                query,
                dataset["title"],
                dataset["subtitle"],
            )

            if score == -1:
                continue

            matches.append(
                (
                    score,
                    SearchResult(
                        id=f"{dataset['owner_slug']}/{dataset['dataset_slug']}",
                        name=dataset["title"],
                        provider=self.name,
                        description=dataset["subtitle"],
                        relevance=score
                    ),
                )
            )

        matches.sort(key=lambda x: x[0], reverse=True)

        return [result for _, result in matches]

    def info(self, dataset_id: str) -> DatasetInfo:
        for dataset in self._load_index():
            if f"{dataset['owner_slug']}/{dataset['dataset_slug']}" == dataset_id:
                return DatasetInfo(
                    id=dataset_id,
                    name=dataset["title"],
                    description=dataset["subtitle"],
                    instances=None,
                    features=None,
                    tasks=None,
                    target=None,
                    has_missing_values=None,
                    provider=self.name,
                    url=f"https://www.kaggle.com/datasets/{dataset_id}",
                    extra=dataset,
                )

        raise ValueError(f"Dataset '{dataset_id}' not found.")

    def pull(self, dataset_id: str) -> pl.DataFrame:
        dataset_path = Path(kagglehub.dataset_download(dataset_id))
        csv_file = next(dataset_path.rglob("*.csv"))

        return kagglehub.dataset_load(
            KaggleDatasetAdapter.POLARS,
            handle=dataset_id,
            path=csv_file.name,
        ).collect()