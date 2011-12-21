
from analyzer.media_server_admin_queryer import MediaServerAdminQueryer
from exception import *
import asyncore, socket
from analyzer.analyzer import Analyzer

def test_00():
    url = "http://10.33.0.59/tag_live_monitor/tvie/test1/test2"
    stream_id = 0

    _map = {}
    analyzer = Analyzer()
    http_client = MediaServerAdminQueryer(analyzer, stream_id, url, _map)

    asyncore.loop(map = _map)
    print http_client.response.body

if __name__ == "__main__":
    test_00()
