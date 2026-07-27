from pathlib import Path

from dataflux.utils.fingerprint import (
    hash_string,
    hash_bytes,
    hash_file,
    fingerprint,
    cache_key,
    provider_key,
    verify,
)


# ============================================================================
# String Hash
# ============================================================================

def test_hash_string():
    h1 = hash_string("dataflux")
    h2 = hash_string("dataflux")

    assert h1 == h2
    assert isinstance(h1, str)
    assert len(h1) == 64


# ============================================================================
# Bytes Hash
# ============================================================================

def test_hash_bytes():
    h1 = hash_bytes(b"hello")
    h2 = hash_bytes(b"hello")

    assert h1 == h2


# ============================================================================
# File Hash
# ============================================================================

def test_hash_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("Hello DataFlux")

    h1 = hash_file(file)
    h2 = hash_file(file)

    assert h1 == h2


# ============================================================================
# Generic Fingerprint
# ============================================================================

def test_fingerprint_string():
    fp = fingerprint("iris")

    assert isinstance(fp, str)
    assert len(fp) == 64


def test_fingerprint_file(tmp_path):
    file = tmp_path / "iris.csv"
    file.write_text("id,name\n1,Alice")

    fp = fingerprint(file)

    assert isinstance(fp, str)
    assert len(fp) == 64


# ============================================================================
# Verify
# ============================================================================

def test_verify():
    value = "dataflux"

    expected = fingerprint(value)

    assert verify(value, expected)


# ============================================================================
# Cache Key
# ============================================================================

def test_cache_key():
    key1 = cache_key("search", "iris")
    key2 = cache_key("search", "iris")

    assert key1 == key2
    assert len(key1) == 64


# ============================================================================
# Provider Key
# ============================================================================

def test_provider_key():
    key1 = provider_key("sklearn", "iris")
    key2 = provider_key("sklearn", "iris")

    assert key1 == key2
    assert len(key1) == 64


# ============================================================================
# Different Inputs
# ============================================================================

def test_different_inputs():
    assert fingerprint("iris") != fingerprint("wine")