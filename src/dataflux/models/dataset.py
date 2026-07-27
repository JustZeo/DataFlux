from dataclasses import dataclass
from typing import Any
@dataclass(slots=True)
class DatasetInfo:
    id: str | int
    name: str
    description: str | None
    instances: int | None
    features: int | None
    tasks: list[str]
    target: list[str]
    has_missing_values: bool | None
    provider: str
    url: str | None
    extra: dict[str, Any]