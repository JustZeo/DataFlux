from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from dataflux.config import DATAFLUX_CACHE
from dataflux.utils.filesystem import ensure_dir


class Cache:
    """
    Generic JSON cache manager for DataFlux.

    Examples
    --------
    >>> cache.write("search/iris", data)
    >>> cache.read("search/iris")
    >>> cache.exists("search/iris")
    """

    def __init__(self, root: str | Path = DATAFLUX_CACHE):
        self.root = ensure_dir(root)

    # -------------------------------------------------------------------------
    # Internal
    # -------------------------------------------------------------------------

    def _path(self, key: str) -> Path:
        """
        Convert a cache key into a JSON file path.

        Example
        -------
        search/iris -> ~/.cache/dataflux/search/iris.json
        """
        path = self.root / Path(key).with_suffix(".json")
        ensure_dir(path.parent)
        return path

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def exists(self, key: str) -> bool:
        """Return True if a cache entry exists."""
        return self._path(key).exists()

    def read(self, key: str, default: Any = None) -> Any:
        """
        Read cached JSON data.

        Returns
        -------
        Cached object or `default` if the key doesn't exist.
        """
        path = self._path(key)

        if not path.exists():
            return default

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, key: str, value: Any) -> Path:
        """
        Write JSON-serializable data to cache.
        """
        path = self._path(key)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                value,
                f,
                indent=2,
                ensure_ascii=False,
            )

        return path

    def delete(self, key: str) -> bool:
        """
        Delete a cached object.
        """
        path = self._path(key)

        if not path.exists():
            return False

        path.unlink()
        return True

    def clear(self) -> None:
        """
        Remove every cached object.
        """
        shutil.rmtree(self.root, ignore_errors=True)
        ensure_dir(self.root)

    def list(self, pattern: str = "**/*.json") -> list[str]:
        """
        List cached keys.

        Examples
        --------
        >>> cache.list()
        >>> cache.list("search/*.json")
        """
        return sorted(
            str(path.relative_to(self.root).with_suffix(""))
            for path in self.root.glob(pattern)
        )

    def size(self) -> int:
        """
        Return the total number of cached objects.
        """
        return len(self.list())


cache = Cache()