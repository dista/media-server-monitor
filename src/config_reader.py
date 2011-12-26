'''
Created on 2011-12-17

@author: dista
'''

import os
import sys
import json

from json import JSONEncoder as Encoder

class ConfigReader:
    def __init__(self):
        self.path = ''
        self.cdn_path = ''
        self.encoder = Encoder()
    
    def read_config_as_dict(self, config_path):
        file_obj_config = None
        file_obj_cdn = None

        file_dict = {}
        cdn_stream_dict = {}

        self.path = config_path            
        if self.path == None:
            print 'File path is empty, failed to read config file\n'
            return None
        elif not os.path.exists(self.path):
            print 'File %s is no exists, please check the directory\
            or file name\n' % (self.path)

        try:
            file_obj_config = open(git@github.com:dista/media-server-monitor.gitself.path, 'r')
            file_dict = json.loads(self.get_config_json(file_obj_config))
        except IOError, err:
            print 'IO Error, can not read file %s' % (self.path)
            print 'Error %d : %s' % (err.args[0], err.args[1])
            return None
        except ValueError, err:
            print "Value Error, can not read file %s" % (self.path)
            print 'Error %d : %s' % (err.args[0], err.args[1])
        finally:
            file_obj_config.close()


        self.cdn_path = file_dict['cdn_streams'];
        file_dict.pop('cdn_streams')
        file_dict['cdn_streams'] = None

        if self.cdn_path == None:
            return

        try:
            file_obj_cdn = open(self.cdn_path, 'r')
            cdn_stream_dict = json.loads(self.get_config_json(file_obj_cdn))
        except IOError, err:
            print 'IO Error, can not read file %s' % (self.cdn_path)
            print 'Error %d : %s' % (err.args[0], err.args[1])
            return None
        except ValueError, err:
            print "Valutempe Error, can not read file %s" % (self.cdn_path)
            print 'Error %d : %s' % (err.args[0], err.args[1])
        finally:
            file_obj_cdn.close()

        file_dict['cdn_streams'] = cdn_stream_dict
      
        return json.dumps(file_dict)


    def get_config_json(self, file_obj):
        file_content = ''
        file_dict = {}

        if file_obj == None:
            print 'Invalid file object\n'
            return file_content
        
        while True:
            one_line = file_obj.readline()
            if not one_line:
                break;
            
            line_content = one_line.strip().strip('\n')
            if line_content.find(':') > -1:
                list_content = line_content.split(':', 1)
                if len(list_content) > 1:
                    print list_content
                    left_content = list_content[0].strip()
                    right_content = list_content[1].strip()

                    file_content = file_content + \
                    self.encoder.encode(left_content) + ':'

                    if right_content.find(',') == -1:
                        if right_content == '{':
                            file_content = file_content + '{'
                        else:
                            file_content = file_content + \
                            self.encoder.encode(right_content)
                    else:
                        file_content = file_content + \
                        self.encoder.encode(right_content.strip(',')) + \
                       ','                                                    
                else:
                    file_content = file_content + list_content + ':'
            else:
                file_content = file_content + line_content

        file_dict = json.loads(file_content)     

        return json.dumps(file_dict)