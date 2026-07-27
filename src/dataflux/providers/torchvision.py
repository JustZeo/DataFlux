from dataflux.providers.base import BaseProvider
from dataflux.models.search_result import SearchResult
from dataflux.models.dataset import DatasetInfo
from dataflux.resources.torch_vision_dataset import TORCHVISION_DATASETS
from dataflux.utils.search import search_score
from dataflux.config import TORCHVISION_CACHE
import polars as pl


class TorchVisionProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "torchvision"

    def _load_dataset(self, dataset_id: str):
        return TORCHVISION_DATASETS[dataset_id](
            root=TORCHVISION_CACHE,
            download=True,
        )

    def search(self, query: str) -> list[SearchResult]:
        matches: list[tuple[int, SearchResult]] = []

        for dataset in TORCHVISION_DATASETS:
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

        image_shape = None
        if hasattr(dataset, "data"):
            image_shape = tuple(dataset.data.shape[1:])

        return DatasetInfo(
            id=dataset_id,
            name=dataset_id.replace("_", " ").title(),
            description=None,
            instances=len(dataset),
            features=None,
            tasks=["Image Classification"],
            target=getattr(dataset, "classes", None),
            has_missing_values=False,
            provider=self.name,
            url=None,
            extra={
                "image_shape": image_shape,
                "num_classes": len(dataset.classes) if hasattr(dataset, "classes") else None,
                "class_to_idx": getattr(dataset, "class_to_idx", None),
            },
        )

    def pull(self, dataset_id: str) -> pl.DataFrame:
        dataset = self._load_dataset(dataset_id)

        return pl.DataFrame(
            {
                "image": dataset.data.numpy().tolist(),
                "label": dataset.targets.numpy().tolist(),
            }
        )