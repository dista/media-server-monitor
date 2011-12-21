from analyzer.http_client import HttpClient
from exception import *
import asyncore, socket

def http_client_test_00():
    uri_error_happend = False

    try:
        http_client = HttpClient(9)
    except URIError:
        uri_error_happend = True

    assert uri_error_happend

def http_client_test_01():
    url = "http://10.33.3.59/tag_live_monitor/tvie/test1/test1"

    _map = {}
    http_client = HttpClient(url, _map)

    asyncore.loop(map = _map)
    print _map
    print "loop finished"

if __name__ == "__main__":
    http_client_test_00()
    http_client_test_01()
