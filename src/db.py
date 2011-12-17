'''
Created on 2011-12-17

@author: dista
'''

class Database:
    def __init__(self, host, port, name, password, logger = None):
        self.host = host
        self.port = port
        self.name = name
        self.password = password
        self.logger = logger
        
    def query(self, sql):
        pass