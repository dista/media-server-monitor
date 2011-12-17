'''
Created on 2011-12-17

@author: dista
'''

import threading

class AnalyzeThread(threading.Thread):
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
    
    def notify_obs_changed(self, new_obs):
        pass
    
    def run(self):
        pass