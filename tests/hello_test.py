def hello():
    return "Hello, World!"


def test_hello():
    result = hello()
    assert result == "Hello, World!", "Test case failed"
