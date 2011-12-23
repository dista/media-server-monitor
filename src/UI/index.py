import web
from os import path
import json

urls = (
        "", "home",
        "/env", "env",
        "/samples", "samples",
        "/static/.*", "static"
        )

mms_ui_root = "/root/media-server-monitor/src/UI/"

def get_content_type(path_info):
    last = path_info.split('/')[-1]
    last = last.split('.')[-1]

    mime_map = {
            "js": "application/javascript",
            "css": "text/css",
            "gif": "image/gif"
            }

    return mime_map[last] 

def get_file_contents(file_path):
    f = None
    try:
        f = open(file_path)
        return f.read()
    finally:
        if f != None:
            f.close()

def load_samples():
    samples = web.template.frender(path.join(mms_ui_root, 'templ/samples.html'))

    fake_data = {
            "total_samples": 2,
            "samples": {
                "10001": {
                    'stream_id': 10001,
                    'sample_interface': 'http://test.zz',
                    'unify_name': '10.33.0.28/tvie/channel1/sd',
                    'average_downstream_kbps': {
                        "last_3": 100,
                        "last_10": 200,
                        "last_100": 150,
                        "total": 120
                        },
                    'average_upstream_kbps': {
                        "last_3": 100,
                        "last_10": 200,
                        "last_100": 150,
                        "total": 120
                        },
                    'score': 50,
                    'score_level': 2,
                    'score_detail': {
                        'live_delay': 10,
                        'upstream': 90
                        },
                    'score_level_detail': {
                        'live_delay': 1,
                        'upstream': 3
                        },
                    'sample_time': '2011/12/11 02:23:12',
                    "total_gops": 100123,
                    "upstream_opened_count": 21,
                    "upstream_connected_count": 23,
                    "upstream_connection_fail_count": 23,
                    "upstream_bytes_received": 32252,
                    "clients_connected": 445,
                    "total_clients_served": 234,
                    "total_bytes_sent": 812,
                    "live_delay_ms": 235,
                    "stream_info_audiodatarate": 152,
                    "stream_info_videodatarate": 233,
                    "stream_info_audiocodecid": 658,
                    "stream_info_audiosamplesize": 16,
                    "stream_info_audiosamplerate": 4422,
                    "stream_info_stereo": 235,
                    "stream_info_videocodecid": 2414,
                    "stream_info_framerate": 812,
                    "stream_info_width": 235,
                    "stream_info_height": 235
                    },
                "10002": {
                    'stream_id': 10002,
                    'sample_interface': 'http://test.zz',
                    'unify_name': 'tvie/channel1/sd',
                    'average_downstream_kbps': {
                        "last_3": 100,
                        "last_10": 200,
                        "last_100": 150,
                        "total": 120
                        },
                    'average_upstream_kbps': {
                        "last_3": 100,
                        "last_10": 200,
                        "last_100": 150,
                        "total": 120
                        },
                    'score': 50,
                    'score_level': 2,
                    'score_detail': {
                        'live_delay': 10,
                        'upstream': 90
                        },
                    'score_level_detail': {
                        'live_delay': 1,
                        'upstream': 3
                        },
                    'sample_time': '2011/12/11 02:23:12',
                    "total_gops": 100123,
                    "upstream_opened_count": 21,
                    "upstream_connected_count": 23,
                    "upstream_connection_fail_count": 23,
                    "upstream_bytes_received": 32252,
                    "clients_connected": 445,
                    "total_clients_served": 234,
                    "total_bytes_sent": 812,
                    "live_delay_ms": 235,
                    "stream_info_audiodatarate": 152,
                    "stream_info_videodatarate": 233,
                    "stream_info_audiocodecid": 658,
                    "stream_info_audiosamplesize": 16,
                    "stream_info_audiosamplerate": 4422,
                    "stream_info_stereo": 235,
                    "stream_info_videocodecid": 2414,
                    "stream_info_framerate": 812,
                    "stream_info_width": 235,
                    "stream_info_height": 235
                    }
                }
            }
    return samples(fake_data)

class home:
    def GET(self):
        home = web.template.frender(path.join(mms_ui_root, 'templ/home.html'))

        return home(web, load_samples())

class samples:
    def GET(self):
        return load_samples()

class static:
    def GET(self):
        path_info_arr = web.ctx.env['PATH_INFO'].split('/')
        path_info = "/".join(path_info_arr[4:])
        web.header('Content-Type', get_content_type(path_info))
        return get_file_contents(path.join(mms_ui_root, path_info)) 

class env:
    def GET(self):
        return json.dumps(web.ctx.env)


app = web.application(urls, locals())
