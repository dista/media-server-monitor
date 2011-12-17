'''
Created on 2011-12-17

@author: dista
'''
from exception import *

import time, sys

class Logger:
    def __init__(self, log_path = None, level = 0):
        '''
        level: 0 -- suppress all
               1 -- debug
               2 -- error
               3 -- warn
        '''
        self.level = level
        self.log_path = log_path
        
        if log_path == None:
            self.log_fd = sys.stderr
            
        self.log_fd = None
        try:
            self.log_fd = open(log_path)
        except IOError, e:
            raise LogError(e)
    
    def close(self):
        if self.log_path == None:
            return
        
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
            
    def debug(self, msg):
        if self.level > 0:
            self.log("[debug] %s" % msg) 
           
    def warn(self, msg):
        if self.level > 2:
            self.log("[warn] %s" % msg)
    
    def error(self, msg):
        if self.level > 1:
            self.log("[error] %s" % msg)