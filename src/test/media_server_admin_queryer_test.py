
from analyzer.media_server_admin_queryer import MediaServerAdminQueryer
from exception import *
import asyncore, socket
from common.http import HttpResponse
from analyzer.analyzer import Analyzer
from common import parser
from datetime import datetime
import os

def test_00():
    url = "http://10.33.0.57/tag_live_monitor/tvie/zhso/xfw"
    stream_id = 0

    _map = {}
    analyzer = Analyzer()
    http_client = MediaServerAdminQueryer(analyzer, stream_id, url, _map)

    asyncore.loop(map = _map)
    print http_client.response.body

if __name__ == "__main__":
    test_00()
