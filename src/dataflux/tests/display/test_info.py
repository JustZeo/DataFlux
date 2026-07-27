from dataflux.display.info import display_info
from dataflux.models.dataset import DatasetInfo


# ============================================================================
# Minimal DatasetInfo
# ============================================================================

def test_minimal_info():
    info = DatasetInfo(
        id="iris",
        name="Iris",
        description=None,
        instances=150,
        features=4,
        tasks=None,
        target=None,
        has_missing_values=False,
        provider="sklearn",
        url=None,
        extra=None,
    )

    display_info(info)


# ============================================================================
# Full DatasetInfo
# ============================================================================

def test_full_info():
    info = DatasetInfo(
        id="iris",
        name="Iris",
        description="The famous Iris flower dataset.",
        instances=150,
        features=4,
        tasks=["Classification"],
        target=[
            "setosa",
            "versicolor",
            "virginica",
        ],
        has_missing_values=False,
        provider="sklearn",
        url="https://scikit-learn.org",
        extra={
            "Feature Names": [
                "sepal_length",
                "sepal_width",
                "petal_length",
                "petal_width",
            ],
            "License": "BSD-3",
        },
    )

    display_info(info)


# ============================================================================
# Empty Extra
# ============================================================================

def test_empty_extra():
    info = DatasetInfo(
        id="iris",
        name="Iris",
        description="Dataset",
        instances=150,
        features=4,
        tasks=None,
        target=None,
        has_missing_values=False,
        provider="sklearn",
        url=None,
        extra={},
    )

    display_info(info)


# ============================================================================
# Mapping Extra
# ============================================================================

def test_mapping_extra():
    info = DatasetInfo(
        id="iris",
        name="Iris",
        description="Dataset",
        instances=150,
        features=4,
        tasks=None,
        target=None,
        has_missing_values=False,
        provider="sklearn",
        url=None,
        extra={
            "Dtypes": {
                "sepal_length": "Float64",
                "species": "String",
            }
        },
    )

    display_info(info)


# ============================================================================
# Sequence Extra
# ============================================================================

def test_sequence_extra():
    info = DatasetInfo(
        id="iris",
        name="Iris",
        description="Dataset",
        instances=150,
        features=4,
        tasks=None,
        target=None,
        has_missing_values=False,
        provider="sklearn",
        url=None,
        extra={
            "Columns": [
                "sepal_length",
                "sepal_width",
                "petal_length",
                "petal_width",
                "species",
            ]
        },
    )

    display_info(info)


# ============================================================================
# Missing Values
# ============================================================================

def test_missing_values():
    info = DatasetInfo(
        id="iris",
        name="Iris",
        description=None,
        instances=None,
        features=None,
        tasks=None,
        target=None,
        has_missing_values=None,
        provider="sklearn",
        url=None,
        extra=None,
    )

    display_info(info)