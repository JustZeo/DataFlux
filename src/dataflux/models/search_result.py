from dataclasses import dataclass ,field

@dataclass(slots=True)
class SearchResult:
    id:str 
    name:str
    provider:str
    description:str | None = None

    relevance: int = field(default=0, repr=False)
