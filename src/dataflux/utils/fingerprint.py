from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


DEFAULT_ALGORITHM = "sha256"
CHUNK_SIZE = 8192


# ============================================================================
# Core Hash Functions
# ============================================================================

def hash_string(
    text: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> str:
    """
    Generate a hash for a string.
    """
    return hashlib.new(
        algorithm,
        text.encode("utf-8"),
    ).hexdigest()


def hash_bytes(
    data: bytes,
    algorithm: str = DEFAULT_ALGORITHM,
) -> str:
    """
    Generate a hash for raw bytes.
    """
    return hashlib.new(
        algorithm,
        data,
    ).hexdigest()


def hash_file(
    path: str | Path,
    algorithm: str = DEFAULT_ALGORITHM,
) -> str:
    """
    Generate a hash for a file without loading it entirely into memory.
    """
    hasher = hashlib.new(algorithm)

    with open(path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)

    return hasher.hexdigest()


# ============================================================================
# Generic Fingerprinting
# ============================================================================

def fingerprint(
    obj: Any,
    algorithm: str = DEFAULT_ALGORITHM,
) -> str:
    """
    Generate a deterministic fingerprint for any supported object.

    Supports
    --------
    - str
    - bytes
    - pathlib.Path
    - Polars DataFrame
    - Any object implementing ``serialize()``
    - Any other object via ``repr()``
    """

    if isinstance(obj, bytes):
        return hash_bytes(obj, algorithm)

    if isinstance(obj, (str, Path)):
        path = Path(obj)

        if path.exists() and path.is_file():
            return hash_file(path, algorithm)

        return hash_string(str(obj), algorithm)

    if hasattr(obj, "serialize"):
        serialized = obj.serialize()

        if isinstance(serialized, bytes):
            return hash_bytes(serialized, algorithm)

        return hash_string(str(serialized), algorithm)

    return hash_string(repr(obj), algorithm)


# ============================================================================
# DataFlux Helpers
# ============================================================================

def cache_key(*parts: Any) -> str:
    """
    Generate a deterministic cache key.

    Example
    -------
    >>> cache_key("search", "iris")
    """
    return hash_string("::".join(map(str, parts)))


def provider_key(
    provider: str,
    dataset: str | int,
) -> str:
    """
    Generate a provider-specific dataset key.

    Example
    -------
    >>> provider_key("sklearn", "iris")
    """
    return cache_key(provider.lower(), dataset)


def verify(
    obj: Any,
    expected: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """
    Verify that an object's fingerprint matches an expected hash.
    """
    return fingerprint(obj, algorithm) == expected


def is_duplicate(
    obj: Any,
    fingerprints: set[str],
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """
    Check whether an object has already been seen.

    Example
    -------
    >>> seen = set()
    >>> if not is_duplicate(df, seen):
    ...     seen.add(fingerprint(df))
    """
    return fingerprint(obj, algorithm) in fingerprints