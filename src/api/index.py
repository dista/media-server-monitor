'''
Created on 2011-12-24

@author: dista
'''

import web
import conf
import json
from config_reader import ConfigReader
from common import json_handler

CONFIG_PATH = "/usr/local/tvie/config/media-server-monitor.conf"
cr = ConfigReader()
config = cr.read_config_as_dict(conf.CONFIG_PATH)

urls = (
        "/samples/.*", "samples"
        )

class samples:
    def GET(self):
        path_info_arr = web.ctx.env['PATH_INFO'].split('/')
        offset, page_size = (int(i) for i in path_info_arr[4].split('-'))
        keyword, sort_by, sort_order, sort_by_status_first = path_info_arr[5:]
        sort_by_status_first = int(sort_by_status_first)

        if sort_order.upper() not in ["ASC", "DESC"]:
            raise badrequest()

        db = web.database(dbn='mysql', db='tvie_production2', host='10.33.0.57', user='tvie', pw='tvierocks')

        sql = "SELECT * FROM mms_stream"

        where_in = False
        if keyword != "null":
            sql += ' WHERE unify_name like "%%%%%s%%%%"' % keyword

        if int(sort_by_status_first) == 1:
            sql += " order by score, %s asc" % sort_by
        else:
            sql += " order by %s %s" % (sort_by, sort_order)

        if int(page_size) != 0:
            sql += " limit %d, %d" % (offset, page_size)

        streams = db.query(sql)

        ret_streams = []
        for stream in streams:
            sample_result = db.query("SELECT * FROM mms_samples where mms_stream_id = %d order by id desc limit 1" % stream['id'])

            samples = [ i for i in sample_result ]

            if samples != None and len(samples) > 0:
                stream.update(samples[0])
            else:
                stream.update({"average_upstream_kbps": 0, "average_downstream_kbps": 0, "total_gops": 0, "stream_info_audiodatarate": 0, "stream_info_videodatarate": 0})
            ret_streams.append(stream)
                
        return json.dumps({"total_samples": len(ret_streams), 'samples': ret_streams}, cls=json_handler.ExtendedEncoder)


app = web.application(urls, locals())
