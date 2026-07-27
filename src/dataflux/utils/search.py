import re

from dataflux.models.search_result import SearchResult


PROVIDER_PRIORITY = {
    "sklearn": 100,
    "uci": 95,
    "torchvision": 90,
    "huggingface": 80,
    "kaggle": 70,
    "statsmodels": 60,
    "seaborn": 50,
    "vega": 40,
    "worldbank": 30,
}


def search_score(query: str, *texts: str) -> int:
    """
    Returns:
        2 -> exact word match
        1 -> partial match
       -1 -> no match
    """
    query = query.lower().strip()
    best = -1

    for text in texts:
        if not text:
            continue

        text = str(text).lower()

        # Exact word match
        if re.search(rf"\b{re.escape(query)}\b", text):
            best = max(best, 2)

        # Partial match
        elif query in text:
            best = max(best, 1)

    return best



def rank(results: list[SearchResult]) -> list[SearchResult]:
    def score(result:SearchResult):
        documentation_bonus = (
            5
            if result.description and result.description.strip()
            else 0
        )
        return (
            result.relevance*1000
            + PROVIDER_PRIORITY.get(result.provider,0)
            + documentation_bonus
        )
    return sorted(
        results,
        key=lambda result: (
            score(result),
            result.name.lower(),
        ),
        reverse=True,
    )