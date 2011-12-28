'''
Created on 2011-12-17

@author: dista
'''

import os
import sys
import json

class ConfigReader:
    def __init__(self):
        pass
    
    def read_config_as_dict(self, config_path):
        config_fd, stream_fd = None, None
        config = None

        try:
            config_fd = open(config_path, 'r')

            config = json.load(config_fd)

            if config['extra_streams_path'] != "":
                stream_fd = open(config['extra_streams_path'], 'r')
                config['extra_streams'] = json.load(stream_fd)
            else:
                config['extra_streams'] = []
        finally:
            if config_fd != None:
                config_fd.close()
            if stream_fd != None:
                stream_fd.close()

        return config


