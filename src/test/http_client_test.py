from analyzer.http_client import HttpClient
from exception import *
import asyncore, socket
import time


#source is 2012

def http_client_test_00():
    uri_error_happend = False

    try:
        http_client = HttpClient(9)
    except URIError:
        uri_error_happend = True

    assert uri_error_happend

def http_client_test_01():
    url = "http://10.33.0.225/tag_live_monitor/tvie/anhui1b/anhui1b"

    _map = {}
    http_client = HttpClient(url, _map)

    asyncore.loop(map = _map)

def http_client_test_02():
    url = "http://10.33.0.225/tag_live_monitor/tvie/anhui1b/anhui1b"

    i = 0
    while i < 100:
        _map = {}
        http_client = HttpClient(url, _map)

        asyncore.loop(map = _map)
        f = open('/root/media-server-monitor/src/test_data/analyzer/upstream_up/%d.txt' % time.time(), 'w+')
        f.write(http_client.data)
        f.close()

        time.sleep(3)

        i += 1

def http_client_test_03():
    url = "http://10.33.0.225/tag_live_monitor/tvie/xj/sd"

    i = 0
    while i < 100:
        _map = {}
        http_client = HttpClient(url, _map)

        asyncore.loop(map = _map)
        f = open('/root/media-server-monitor/src/test_data/analyzer/upstream_down/%d.txt' % time.time(), 'w+')
        f.write(http_client.data)
        f.close()

        time.sleep(3)

        i += 1

def http_client_test_04():
    url = "http://10.33.0.225/tag_live_monitor/tvie/ms-monitor-test/sd"

    i = 0
    while i < 100:
        _map = {}
        http_client = HttpClient(url, _map)

        asyncore.loop(map = _map)
        f = open('/root/media-server-monitor/src/test_data/analyzer/upstream_limit_200k/%d.txt' % time.time(), 'w+')
        f.write(http_client.data)
        f.close()

        time.sleep(3)

        i += 1

if __name__ == "__main__":
    http_client_test_02()
    #http_client_test_01()
    #http_client_test_03()
    #http_client_test_04()
