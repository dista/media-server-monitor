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

class AnalyzeThread(threading.Thread):
    def __init__(self, sleep_time):
        self.logger = logger.get_logger()
        self.obs = None
        self.sleep_time = sleep_time
        self.analyzer = Analyzer()
        self.obs_lock = threading.Lock()
    
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
            sended_requests = []
            _map = {}
            for stream in all_streams:
                sended_requests.append(MediaServerAdminQueryer(self.analyzer, stream['id'], stream['sample_interface'], _map)

            asyncore.loop(map = _map)
            self._update_db(all_streams, sended_requests)
            time.sleep(self.sleep_time)

    def _update_db(self, all_streams, sended_requests):
    '''
        HERE WE UPDATE DB!! AND ONLY HERE WE DO THAT
    '''
        pass
