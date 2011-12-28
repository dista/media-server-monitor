'''
Created on 2011-12-17

@author: dista
'''

import threading
import asyncore
from media_server_admin_queryer import MediaServerAdminQueryer
from analyzer import Analyzer
import time
import logger
from model.stream_model import StreamModel
from model.sample_model import SampleModel
import MySQLdb

class AnalyzeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = logger.get_logger()
        self.obs = None
        self.sleep_time = 3
        self.analyzer = Analyzer()
        self.obs_lock = threading.Lock()
        self.stream_model = StreamModel() 
        self.sample_model = SampleModel()
    
    def notify_obs_changed(self, new_obs):
        self.obs_lock.acquire()
        self.obs = new_obs
        self.obs_lock.release()

    def _get_obs(self):
        ret = None
        self.obs_lock.acquire()
        ret = self.obs
        self.obs_lock.release()

        return ret 

    def _get_map_stream_ids(self, _map):
        return [msq.stream_id for msq in _map.items]
    
    def run(self):
        while True:
            all_streams = self._get_obs()
            streams_in_db = self.stream_model.get_all()
            if all_streams == None:
                all_streams = streams_in_db
            
            sended_requests = []
            _map = {}
            for stream in all_streams:
                sended_requests.append(MediaServerAdminQueryer(self.analyzer, stream['stream_id'], stream['sample_interface'], _map))

            asyncore.loop(map = _map)
            
            delete_streams, update_streams, add_streams = self._get_changed_streams(streams_in_db, all_streams)

            try:
                self._update_db(delete_streams, update_streams, add_streams, sended_requests)
            except MySQLdb.Error, e:
                self.logger.warn("update_db failed")

            time.sleep(self.sleep_time)

    def _get_changed_streams(self, streams_before_run, streams_after_run):
        before_ids = set([stream['stream_id'] for stream in streams_before_run])
        after_ids = set([stream['stream_id'] for stream in streams_after_run])

        delete_ids, update_ids, add_ids =  before_ids - after_ids, before_ids & after_ids, after_ids - before_ids
        
        delete_streams = [stream for stream in streams_before_run if (stream['stream_id'] in delete_ids)]
        update_streams_after = [stream for stream in streams_after_run if (stream['stream_id'] in update_ids)]
        update_streams_before = [stream for stream in streams_before_run if (stream['stream_id'] in update_ids)]
        add_streams  = [stream for stream in streams_after_run if (stream['stream_id'] in add_ids)]

        return (delete_streams, self._get_update_streams(update_streams_after, update_streams_before), add_streams)

    def _get_update_streams(self, update_streams_after, update_streams_before):
        ret = []
        for s1 in update_streams_after:
            for s2 in update_streams_before:
                if s2['stream_id'] == s1['stream_id']:
                    if s1['sample_interface'] != s2['sample_interface'] or s1['unify_name'] != s2['unify_name']:
                        ret.append(s1)
                    break

        return ret
            
    def _update_db(self, delete_streams, update_streams, add_streams, sended_requests):
        '''
        HERE WE UPDATE DB!! AND ONLY HERE WE DO THAT
        '''
        mms_streams = self.stream_model.get_by_stream_ids([stream['stream_id'] for stream in delete_streams])

        mms_streams_ids = [stream['id'] for stream in mms_streams]
        self.sample_model.delete_by_stream_ids(mms_streams_ids)
        self.stream_model.delete_by_ids(mms_streams_ids)

        for stream in update_streams:
            self.stream_model.update_by_stream_id(stream)

        self.stream_model.add(add_streams)

        for request in sended_requests:
            analyze_result = request.analyze_result
            stream = analyze_result['cal_data']
            stream['stream_id'] = request.stream_id
            stream['score'] = analyze_result['score']
            stream['score_level'] = analyze_result['score_level']
            stream['score_upstream'] = analyze_result['score_detail']['upstream_value']
            stream['score_level_upstream'] = analyze_result['score_level_detail']['upstream']
            stream['score_live_delay'] = analyze_result['score_detail']['live_delay_value']
            stream['score_level_live_delay'] = analyze_result['score_level_detail']['live_delay']
            stream['last_sample_time'] = request.sample_time.strftime("%Y-%m-%d %H:%M:%S")
            
            self.stream_model.update_by_stream_id(stream)
            
            stream_in_db = self.stream_model.get_by_stream_id(request.stream_id)
            analyze_result['sample']['mms_stream_id'] = stream_in_db[0]['id']
            analyze_result['sample']['sample_time'] = analyze_result['sample']['sample_time'].strftime("%Y-%m-%d %H:%M:%S")

            self.sample_model.insert(analyze_result['sample'])
