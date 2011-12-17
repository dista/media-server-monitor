'''
Created on 2011-12-18

@author: dista
'''
import asyncore, socket

class HttpClient(asyncore.dispatcher):
    def __init__(self, url):
        self.url = url