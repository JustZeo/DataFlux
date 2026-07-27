import polars as pl

from dataflux import flux


def test_search():
    results = flux.search("iris", display=False)

    assert len(results) > 0
    assert results[0].provider == "sklearn"


def test_info():
    result = flux.search("iris", display=False)[0]
    info = flux.info(result, display=False)

    assert info.name == "Iris"
    assert info.instances == 150
    assert info.features == 4


def test_pull():
    result = flux.search("iris", display=False)[0]
    df = flux.pull(result)

    assert isinstance(df, pl.DataFrame)
    assert df.height == 150
    assert df.width == 5


def test_export(tmp_path):
    result = flux.search("iris", display=False)[0]
    df = flux.pull(result)

    output = tmp_path / "iris.csv"

    exported = flux.export(df, output)

    assert output.exists()
    assert exported == output