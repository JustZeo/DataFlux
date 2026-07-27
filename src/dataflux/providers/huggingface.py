from dataflux.providers.base import BaseProvider
from dataflux.models.search_result import SearchResult
from dataflux.models.dataset import DatasetInfo
from huggingface_hub import HfApi
from datasets import load_dataset
from dataflux.utils.search import search_score
import polars as pl


class HuggingFaceProvider(BaseProvider):

    def __init__(self):
        self.api = HfApi()

    @property
    def name(self) -> str:
        return "huggingface"

    def search(self, query: str) -> list[SearchResult]:
        matches:list[tuple[int,SearchResult]] =[]

        datasets = self.api.list_datasets(
            search=query,
            limit=20
        )
        for dataset in datasets:
            score = search_score(
                query,
                dataset.id
            )
            if score == -1:
                continue
            matches.append(
                ( score,
                SearchResult(
                    id=dataset.id,
                    name=dataset.id.split("/")[-1].replace("-"," ").title(),
                    provider=self.name,
                    description=None,
                    relevance=score,
                )
            )
        )
        matches.sort(key=lambda x:x[0],reverse=True)
        return [result for _, result in matches]


    def info(self, dataset_id: str) -> DatasetInfo:
        dataset = self.api.dataset_info(dataset_id)
        return DatasetInfo(
            id=dataset_id,
            name=dataset.id.split("/")[-1].replace("-"," ").title(),
            description=dataset.description,
            instances=(
                dataset.card_data["dataset_info"]["splits"][0]["num_examples"]
                if dataset.card_data and "dataset_info" in dataset.card_data
                else None
            ),
            features=(
                len(dataset.card_data["dataset_info"]["features"])
                if dataset.card_data and "dataset_info" in dataset.card_data
                else None
            ),
            tasks=(
                dataset.card_data.get("task_categories")
                if dataset.card_data
                else None
            ),
            target=None,
            has_missing_values=None,
            provider=self.name,
            url=f"https://huggingface.co/datasets/{dataset_id}",
            extra={
                "author":dataset.author,
                "tags":dataset.tags,
                "downloads":dataset.downloads,
                "likes":dataset.likes,
                "created_at":str(dataset.created_at),
                "last_modified": str(dataset.last_modified),
            }
        )

        

    def pull(self, dataset_id: str):
        dataset = load_dataset(dataset_id)
        if hasattr(dataset,"keys"):
            dataset = dataset[list(dataset.keys())[0]]

        return dataset.to_polars()

