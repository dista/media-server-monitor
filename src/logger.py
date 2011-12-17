'''
Created on 2011-12-17

@author: dista
'''
from exception import *

import time, sys

class Logger:
    def __init__(self, log_path, level):
        self.log_fd = None
        try:
            self.log_fd = open(log_path)
        except IOError, e:
            raise LogError(e)
    
    def close(self):
        if self.log_fd != None:
            try:
                self.log_fd.close()
            except IOError, e:
                raise LogError(e)
                
    
    def log(self, msg):
        if self.log_fd == None:
            return
        
        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            self.log_fd.write("[%s]%s" % (tm, msg))
        except IOError:
            print sys.stderr, "Write log failed!" 
           
    def warn(self, msg):
        self.log("[warn] %s" % msg)
    
    def error(self, msg):
        self.log("[error] %s" % msg)