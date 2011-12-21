from common.uri import Uri

def test_uri_00():
    uri = "http://www.google.com/image"

    tmp = Uri(uri)
    assert tmp.schemal == "http"
    assert tmp.host == "www.google.com"
    assert tmp.path == "/image"
    assert tmp.port == 80

def test_uri_01():
    uri = "www.google.com"

    tmp = Uri(uri)
    assert tmp.schemal == "http"
    assert tmp.host == "www.google.com"
    assert tmp.path == "/"
    assert tmp.port == 80

def test_uri_02():
    uri = "https://www.google.com"

    tmp = Uri(uri)
    assert tmp.schemal == "https"
    assert tmp.host == "www.google.com"
    assert tmp.path == "/"
    assert tmp.port == 80

def test_uri_03():
    uri = " https://www.google.com\r\n"

    tmp = Uri(uri)
    assert tmp.schemal == "https"
    assert tmp.host == "www.google.com"
    assert tmp.path == "/"
    assert tmp.port == 80

def test_uri_04():
    uri = "http://www.google.com:8080/image"

    tmp = Uri(uri)
    assert tmp.schemal == "http"
    assert tmp.host == "www.google.com"
    assert tmp.path == "/image"
    assert tmp.port == 8080


if __name__ == "__main__":
    test_uri_00()
    test_uri_01()
    test_uri_02()
    test_uri_03()
