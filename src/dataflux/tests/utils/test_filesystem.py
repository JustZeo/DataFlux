from pathlib import Path

from dataflux.utils.filesystem import (
    CACHE_DIR,
    PACKAGE_ROOT,
    PROJECT_ROOT,
    RESOURCE_DIR,
    TEMP_DIR,
    cache_path,
    ensure_dir,
    expand,
    package_root,
    project_root,
    resource_path,
    temp_path,
)


# ============================================================================
# Package Root
# ============================================================================

def test_package_root():
    assert package_root() == PACKAGE_ROOT
    assert package_root().exists()


# ============================================================================
# Project Root
# ============================================================================

def test_project_root():
    assert project_root() == PROJECT_ROOT
    assert project_root().exists()


# ============================================================================
# Resource Path
# ============================================================================

def test_resource_path():
    path = resource_path("dummy.txt")

    assert path == RESOURCE_DIR / "dummy.txt"


# ============================================================================
# Cache Path
# ============================================================================

def test_cache_path():
    path = cache_path("datasets", "iris")

    assert path == CACHE_DIR / "datasets" / "iris"


# ============================================================================
# Temp Path
# ============================================================================

def test_temp_path():
    path = temp_path("downloads")

    assert path == TEMP_DIR / "downloads"


# ============================================================================
# Ensure Directory
# ============================================================================

def test_ensure_dir(tmp_path):
    path = tmp_path / "datasets"

    returned = ensure_dir(path)

    assert path.exists()
    assert path.is_dir()
    assert returned == path


# ============================================================================
# Existing Directory
# ============================================================================

def test_existing_directory(tmp_path):
    path = tmp_path / "cache"

    path.mkdir()

    returned = ensure_dir(path)

    assert returned == path
    assert path.exists()


# ============================================================================
# Nested Directory
# ============================================================================

def test_nested_directory(tmp_path):
    path = tmp_path / "a" / "b" / "c"

    ensure_dir(path)

    assert path.exists()
    assert path.is_dir()


# ============================================================================
# Expand
# ============================================================================

def test_expand():
    path = expand("~")

    assert isinstance(path, Path)
    assert path.exists()


# ============================================================================
# Expand Relative Path
# ============================================================================

def test_expand_relative():
    path = expand(".")

    assert isinstance(path, Path)
    assert path.is_absolute()