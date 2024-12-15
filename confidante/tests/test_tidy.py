from confidante.tidy import tidy_data

def test_tidy_data():
    data = {"b":2,"a":1}
    tidy = tidy_data(data)
    assert list(tidy.keys()) == ["a","b"]
