from dataflux.cache import Cache


# ============================================================================
# Write
# ============================================================================

def test_write(tmp_path):
    cache = Cache(tmp_path)

    path = cache.write(
        "search/iris",
        {
            "rows": 150,
        },
    )

    assert path.exists()


# ============================================================================
# Read
# ============================================================================

def test_read(tmp_path):
    cache = Cache(tmp_path)

    expected = {
        "dataset": "iris",
        "rows": 150,
    }

    cache.write("search/iris", expected)

    actual = cache.read("search/iris")

    assert actual == expected


# ============================================================================
# Exists
# ============================================================================

def test_exists(tmp_path):
    cache = Cache(tmp_path)

    cache.write(
        "search/iris",
        {"rows": 150},
    )

    assert cache.exists("search/iris")


# ============================================================================
# Missing Key
# ============================================================================

def test_missing_key(tmp_path):
    cache = Cache(tmp_path)

    assert not cache.exists("missing")
    assert cache.read("missing") is None


# ============================================================================
# Default Value
# ============================================================================

def test_default_value(tmp_path):
    cache = Cache(tmp_path)

    default = {"hello": "world"}

    assert cache.read("missing", default) == default


# ============================================================================
# Delete
# ============================================================================

def test_delete(tmp_path):
    cache = Cache(tmp_path)

    cache.write(
        "search/iris",
        {"rows": 150},
    )

    assert cache.delete("search/iris")
    assert not cache.exists("search/iris")


# ============================================================================
# Delete Missing
# ============================================================================

def test_delete_missing(tmp_path):
    cache = Cache(tmp_path)

    assert cache.delete("missing") is False


# ============================================================================
# List
# ============================================================================

def test_list(tmp_path):
    cache = Cache(tmp_path)

    cache.write("search/iris", {})
    cache.write("search/wine", {})

    keys = [
        key.replace("\\", "/")
        for key in cache.list()
    ]

    assert "search/iris" in keys
    assert "search/wine" in keys
    assert len(keys) == 2


# ============================================================================
# Size
# ============================================================================

def test_size(tmp_path):
    cache = Cache(tmp_path)

    cache.write("a", {})
    cache.write("b", {})
    cache.write("c", {})

    assert cache.size() == 3


# ============================================================================
# Clear
# ============================================================================

def test_clear(tmp_path):
    cache = Cache(tmp_path)

    cache.write("a", {})
    cache.write("b", {})

    assert cache.size() == 2

    cache.clear()

    assert cache.size() == 0


# ============================================================================
# Nested Keys
# ============================================================================

def test_nested_keys(tmp_path):
    cache = Cache(tmp_path)

    cache.write(
        "providers/sklearn/iris",
        {
            "rows": 150,
        },
    )

    assert cache.exists("providers/sklearn/iris")

    data = cache.read("providers/sklearn/iris")

    assert data["rows"] == 150