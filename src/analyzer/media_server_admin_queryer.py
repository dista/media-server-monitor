'''
Created on 2011-12-17

@author: dista
'''
import asyncore, socket
from http_client import HttpClient

class MediaServerAdminQueryer(HttpClient):
    def __init__(self, analyzer, admin_if_addr):
        HttpClient.__init__(self, admin_if_addr)
        self.analyzer = analyzer
        
    def on_receive_all_data(self, data):
        pass
        