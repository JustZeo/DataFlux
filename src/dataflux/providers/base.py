from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseProvider(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique provider name."""

    @abstractmethod
    def search(self, query: str) -> Any:
        """Search datasets."""

    @abstractmethod
    def pull(self, dataset: str) -> Path:
        """Download the requested dataset and return its local path."""

    @abstractmethod
    def info(self, dataset: str) -> Any:
        """Return dataset metadata."""