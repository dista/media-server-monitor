'''
Created on 2011-12-17

@author: dista
'''
from http_client import HttpClient
from common.http import HttpResponse
from datetime import datetime

class MediaServerAdminQueryer(HttpClient):
    def __init__(self, analyzer, stream_id, admin_if_addr, _map):
        self.response = None
        self.stream_id = stream_id
        self.analyzer = analyzer
        self.analyze_result = None
        HttpClient.__init__(self, admin_if_addr, _map)

    def on_done(self, has_error):
        self.sample_time = datetime.now()

        if not has_error:
            self.response = HttpResponse(self.data) 
            self.analyze_result = self.analyzer.do_analyze(self.response)
            self.analyze_result['sample']['mms_stream_id'] = self.stream_id
        else:
            self.analyze_result = {
                                  "score": 0,
                                  "is_failed": True
                                  }
            self.analyze_result['sample'], self.analyze_result['score_detail'], self.analyze_result['score_level'], self.analyze_result['cal_data'] = self.analyzer.get_failed_data(self.sample_time, "socket error")
