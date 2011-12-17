'''
Created on 2011-12-17

@author: dista
'''
import asyncore, socket

class MediaServerAdminQueryer(asyncore.dispatcher):
    def __init__(self, analyzer, admin_if_addr):
        self.analyzer = analyzer
        self.admin_if_addr = admin_if_addr
        