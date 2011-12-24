'''
Created on 2011-12-18

@author: dista
'''
import asyncore, socket
from common.uri import Uri
import sys

class HttpClient(asyncore.dispatcher):
    def __init__(self, url, _map = None):
        asyncore.dispatcher.__init__(self, map = _map)
        self.url = Uri(url)
        self.socket_error = False
        self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % self.url.path
        self.data = ""
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.url.host, self.url.port))

    def handle_connect(self):
        pass

    def handle_close(self):
        try:
            self.close()
        except Exception, e:
            self.socket_error = True
            print >> sys.stderr, "[ERROR][handle_close] %s" % e

        self.on_done(self.socket_error)

    def handle_read(self):
        try:
            self.data += self.recv(1024)
        except Exception, e:
            self.socket_error = True
            print >> sys.stderr, "[ERROR][handle_read] %s" % e

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        try:
            sent = self.send(self.buffer)
            self.buffer = self.buffer[sent:]
        except Exception, e:
            self.socket_error = True
            print >> sys.stderr, "[ERROR][handle_write] %s" % e

    def on_done(self, has_error):
        pass
