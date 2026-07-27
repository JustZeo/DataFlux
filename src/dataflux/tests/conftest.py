import polars as pl
import pytest

from dataflux import flux


@pytest.fixture
def iris_result():
    return flux.search("iris", display=False)[0]


@pytest.fixture
def iris_df():
    return flux.pull(
        flux.search(
            "iris",
            display=False,
        )[0]
    )


@pytest.fixture
def sample_df():
    return pl.DataFrame(
        {
            "id": [1, 2, 3],
            "name": [
                "Alice",
                "Bob",
                "Charlie",
            ],
        }
    )