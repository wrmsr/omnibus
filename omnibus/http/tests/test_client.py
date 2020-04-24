import urllib.request


def test_client():
    with urllib.request.urlopen('http://www.python.org/') as f:
        print(f.read(300))
