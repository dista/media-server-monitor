import json

config = {
        "monitor_cdn_in_api": True,
        "get_stream_api_url": "http://#API_HOST_NAME/api/service/media/channels/find", 
        "read_token": "#READ_TOKEN",
        "port": 10294,
        "ui_dir": "/usr/local/tvie/www/mms/UI",
        "extra_streams_path": "",
        "db": {
            "host": "#DB_HOST",
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
