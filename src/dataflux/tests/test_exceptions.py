import pytest

from dataflux.exceptions import (
    DatasetNotFoundError,
    ProviderAlreadyRegisteredError,
)


def test_dataset_not_found():
    with pytest.raises(DatasetNotFoundError):
        raise DatasetNotFoundError("iris")


def test_duplicate_provider():
    with pytest.raises(
        ProviderAlreadyRegisteredError
    ):
        raise ProviderAlreadyRegisteredError(
            "sklearn"
        )