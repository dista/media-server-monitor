import json

config = {
        "monitor_cdn_in_api": True,
        "get_stream_api_url": "",
        "read_token": "",
        "extra_streams_path": " http://10.33.0.57/api/service/media/channels/find",
        "db": {
            "host": "10.33.0.57",
            "port": 3306,
            "user": "tvie",
            "password": "tvierocks",
            "db_name": "tvie_production2"
            },
        "logger": {
            "path": "/usr/local/tvie/var/logs/media-server-monitor.log",
            "level": 7
            }
        }

json.dump(config, open("media-server-monitor.conf", 'w+'), indent=4)
