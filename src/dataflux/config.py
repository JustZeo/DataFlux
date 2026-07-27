from pathlib import Path

DATAFLUX_CACHE = Path.home() / ".dataflux"

UCI_CACHE = DATAFLUX_CACHE / "uci"
KAGGLE_CACHE = DATAFLUX_CACHE / "kaggle"
HF_CACHE = DATAFLUX_CACHE / "huggingface"
TORCHVISION_CACHE = DATAFLUX_CACHE / "torchvision"
TFDS_CACHE = DATAFLUX_CACHE / "tensorflow"

for cache in (
    UCI_CACHE,
    KAGGLE_CACHE,
    HF_CACHE,
    TORCHVISION_CACHE,
    TFDS_CACHE,
):
    cache.mkdir(parents=True, exist_ok=True)