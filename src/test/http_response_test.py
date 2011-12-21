from common.http import HttpResponse


def test_00():
    content = (open("../test_data/http_response.txt")).read()
    response = HttpResponse(content)

    assert response.header['Content-Length'] == len(response.body)

def test_01():
    content = (open("../test_data/http_response_502.txt")).read()
    response = HttpResponse(content)

    print response.header
    assert response.header['Content-Length'] == len(response.body)

if __name__ == "__main__":
    test_00()
    test_01()
