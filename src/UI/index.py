import web
from os import path
import json
import urllib2
import json
import conf
import config_reader

cr = config_reader.ConfigReader()
config = cr.read_config_as_dict(conf.CONFIG_PATH)


urls = (
        "", "home",
        "/env", "env",
        "/samples", "samples",
        "/static/.*", "static"
        )

mms_ui_root = config['ui_dir']

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

    url = "http://localhost:%d/mms/api/samples/0-0/null/stream_id/asc/1" % config['port']
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)

    samples_data = json.loads(response.read()) 
    return samples(samples_data)

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
