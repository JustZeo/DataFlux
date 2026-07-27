from dataflux.resources.seaborn_dataset import SEABORN_DATASETS
from dataflux.resources.sklearn_dataset import SKLEARN_DATASETS
from dataflux.resources.statsmodels_dataset import STATSMODELS_DATASETS
from dataflux.resources.torch_vision_dataset import TORCHVISION_DATASETS


# ============================================================================
# Seaborn
# ============================================================================

def test_seaborn_resource():
    assert isinstance(SEABORN_DATASETS, set)
    assert len(SEABORN_DATASETS) > 0
    assert "iris" in SEABORN_DATASETS


# ============================================================================
# Scikit-Learn
# ============================================================================

def test_sklearn_resource():
    assert isinstance(SKLEARN_DATASETS, dict)
    assert len(SKLEARN_DATASETS) > 0
    assert "iris" in SKLEARN_DATASETS


# ============================================================================
# StatsModels
# ============================================================================

def test_statsmodels_resource():
    assert isinstance(STATSMODELS_DATASETS, set)
    assert len(STATSMODELS_DATASETS) > 0
    assert "longley" in STATSMODELS_DATASETS


# ============================================================================
# TorchVision
# ============================================================================

def test_torchvision_resource():
    assert isinstance(TORCHVISION_DATASETS, dict)
    assert len(TORCHVISION_DATASETS) > 0
    assert "mnist" in TORCHVISION_DATASETS


# ============================================================================
# Values Are Callable
# ============================================================================

def test_sklearn_loaders():
    for loader in SKLEARN_DATASETS.values():
        assert callable(loader)


def test_torchvision_loaders():
    for loader in TORCHVISION_DATASETS.values():
        assert callable(loader)


# ============================================================================
# Keys
# ============================================================================

def test_resource_keys_are_strings():
    resources = (
        SEABORN_DATASETS,
        SKLEARN_DATASETS,
        STATSMODELS_DATASETS,
        TORCHVISION_DATASETS,
    )

    for resource in resources:
        if isinstance(resource, dict):
            keys = resource.keys()
        else:
            keys = resource

        for key in keys:
            assert isinstance(key, str)