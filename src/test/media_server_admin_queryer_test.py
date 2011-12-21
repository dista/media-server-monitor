
from analyzer.media_server_admin_queryer import MediaServerAdminQueryer
from exception import *
import asyncore, socket

def test_00():
    url = "http://10.33.0.59/tag_live_monitor/tvie/test1/test1"
    stream_id = 0

    _map = {}
    http_client = MediaServerAdminQueryer(stream_id, url, _map)

    asyncore.loop(map = _map)

if __name__ == "__main__":
    test_00()
