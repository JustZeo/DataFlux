import json
import urllib.request

import polars as pl
from ucimlrepo import API_LIST_URL, fetch_ucirepo

from dataflux.models.dataset import DatasetInfo
from dataflux.models.search_result import SearchResult
from dataflux.providers.base import BaseProvider
from dataflux.utils.search import search_score


class UCIProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "uci"

    def _datasets(self) -> list[dict]:
        with urllib.request.urlopen(API_LIST_URL) as response:
            payload = json.load(response)
        return payload["data"]

    def search(self, query: str) -> list[SearchResult]:
        matches: list[tuple[int, SearchResult]] = []

        for dataset in self._datasets():
            score = search_score(query, dataset["name"])

            if score == -1:
                continue

            matches.append(
                (
                    score,
                    SearchResult(
                        id=dataset["id"],
                        name=dataset["name"],
                        provider=self.name,
                        relevance=score
                    ),
                )
            )

        matches.sort(key=lambda x: x[0], reverse=True)

        return [result for _, result in matches]

    def pull(self, dataset_id: int | str) -> pl.DataFrame:
        dataset = fetch_ucirepo(id=int(dataset_id))

        features = dataset.data.features
        targets = dataset.data.targets

        if targets is not None:
            df = features.join(targets)
        else:
            df = features

        return pl.from_pandas(df)

    def info(self, dataset_id: int | str) -> DatasetInfo:
        dataset = fetch_ucirepo(id=int(dataset_id))
        meta = dataset.metadata

        return DatasetInfo(
            id=meta["uci_id"],
            name=meta["name"],
            description=meta["abstract"],
            instances=meta["num_instances"],
            features=meta["num_features"],
            tasks=meta["tasks"],
            target=meta["target_col"],
            has_missing_values=meta["has_missing_values"] == "yes",
            provider=self.name,
            url=meta["repository_url"],
            extra=meta,
        )