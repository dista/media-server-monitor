'''
Created on 2011-12-17

@author: dista
'''
from exception import *

import time, sys
import threading

class Logger:
    line_sep_chars = "\n"

    def __init__(self, log_path = None, level = 0):
        '''
        level: 0 -- suppress all
               1 -- debug
               2 -- error
               3 -- warn
        '''
        self.lock = threading.Lock()
        self.level = level
        self.log_path = log_path
        
        if log_path == None:
            self.log_fd = sys.stderr
            return
            
        self.log_fd = None
        try:
            # if the log file is not exits, it will be created
            self.log_fd = open(log_path, 'a+')
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
        
        self.lock.acquire()
        
        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            self.log_fd.write("[%s]%s%s" % (tm, msg, Logger.line_sep_chars))
        except IOError:
            print sys.stderr, "Write log failed!"
        finally:
            self.lock.release()
            
    def debug(self, msg):
        if self.level > 0:
            self.log("[debug] %s" % msg) 
           
    def warn(self, msg):
        if self.level > 2:
            self.log("[warn] %s" % msg)
    
    def error(self, msg):
        if self.level > 1:
            self.log("[error] %s" % msg)
