'''
Created on 2011-12-17

@author: dista
'''
import threading
import time

from model.stream_model import StreamModel
from model.api_server_model import ApiServerModel

class StreamMonitorThread(threading.Thread):
    def __init__(self, get_stream_api_url, analyze_thread, db, logger):
        self.api_server_model = ApiServerModel(get_stream_api_url)
        self.analyze_thread = analyze_thread
        self.db = db
        self.stream_db = StreamModel(db)
        self.logger = logger
        
    def run(self):
        while True:
            streams = self.get_streams()
            
            if not streams:
                self.logger.error("StreamMonitorThread: fail to get streams, exit the thread")
                return
            
            if not self.update_db_and_notify(streams):
                self.logger.error("StreamMonitorThread: fail to update db and notify, exit the thread")
                return
            
    def update_db_and_notify(self, streams):
        pass
                
    def get_streams(self):
        sleep_time = 2
        
        streams = self.api_server_model.get()
        
        while not streams:
            self.logger.warn("StreamMonitorThread: fail to get streams, wait for %d seconds to retry" % sleep_time)
            if sleep_time >= 3 * 60:
                return None
            time.sleep(sleep_time)
            streams = self.api_server_model.get()
            
        return streams
        