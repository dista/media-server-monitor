'''
Created on 2011-12-17

@author: dista
'''
from http_client import HttpClient
from common.http import HttpResponse
from datetime import datetime
from model.stream_model import StreamModel
from model.sample_model import SampleModel

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
            self.analyze_result = self.analyzer.do_analyze(self.sample_time, self.response, self._get_exist_samples())
        else:
            self.analyze_result = {
                                  "score": 0,
                                  "score_level": 1,
                                  "is_failed": True
                                  }
            self.analyze_result['sample'], self.analyze_result['score_detail'], self.analyze_result['score_level_detail'], self.analyze_result['cal_data'] = self.analyzer.get_failed_data(self.sample_time, "socket error")

    def _get_exist_samples(self):
        sm = StreamModel()
        
        stream = sm.get_by_stream_id(self.stream_id)

        if len(stream) == 0:
            return []

        sp_model = SampleModel()
        return sp_model.get_by_mms_stream_id(stream[0]['id'])
