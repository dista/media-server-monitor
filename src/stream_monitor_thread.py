'''
Created on 2011-12-17

@author: dista
'''
import threading
import time

import logger
import copy
from model.stream_model import StreamModel
from model.api_server_model import ApiServerModel
from excepton import ApiCallError, InvalidApiData

class StreamMonitorThread(threading.Thread):
    def __init__(self, get_stream_api_url, read_token, monitor_cdn_in_api, analyze_thread, extra_streams):
        self.api_server_model = ApiServerModel(get_stream_api_url, read_token, monitor_cdn_in_api)
        self.analyze_thread = analyze_thread
        self.stream_db = StreamModel()
        self.logger = logger.get_logger()
        self.extra_streams = extra_streams
        self.api_return_streams = None
        
    def run(self):
        while True:
            streams = self.get_streams()
            
            if not streams:
                self.logger.error("StreamMonitorThread: fail to get streams, exit the thread")
                return

            current_streams_ids = [stream['id'] for stream in streams]

            original_streams_ids = []
            if self.api_return_streams != None:
                original_streams_ids = [stream['id'] for stream in self.api_return_streams]

            need_update = len(set(current_streams_ids) - set(original_streams_ids)) != 0
            
            if need_update:
                self.api_return_streams = streams
                new_obs = copy.copy(self.api_return_streams).extend(self.extra_streams)
                self.analyze_thread.notify_obs_changed(new_obs)
            
    def get_streams(self):
        sleep_time = 2
        streams = None
        
        while True:
            streams = None

            try:
                streams = self.api_server_model.get()
            except ApiCallError, e:
                self.logger.debug("api request failed with %s" % e)
            except InvalidApiData, e:
                self.logger.debug("api request failed with %s" % e)
                return None

            if streams != None:
                break

            self.logger.warn("StreamMonitorThread: fail to get streams, wait for %d seconds to retry" % sleep_time)
            if sleep_time >= 3 * 60:
                return None

            time.sleep(sleep_time)
            sleep_time = sleep_time ** 2
            
        return streams
