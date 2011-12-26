'''
Created on 2011-12-18

@author: dista
'''
import os
import sys
import urllib
import urllib2
import json

from urllib2 import URLError, HTTPError

class ApiServerModel:
    def __init__(self, get_stream_api_url):
        self.get_stream_api_url = get_stream_api_url
        self.readtoke = '12345679'
        
def get(self):

        if self.get_stream_api_url == None:
            return None

        data = """   <find>
                        <user_key>%s</user_key>
                        <action>find_all_channels</action>
                       <select>
                           <page_size>0</page_size>
                             <offset>0</offset>
                             <sort_by>id</sort_by>
                             <sort_order>asc</sort_order>
                         </select>
                     </find>
               """ % (self.readtoken)
 
        request = urllib2.Request(self.get_stream_api_url, data.encode('utf-8'), {'Content-Type': 'text/xml'})

        try:
            response = urllib2.urlopen(request)
            temp = response.read()
        except URLError as err:
            print 'URL Error happend while sendsended_requestsing request'
            print 'Error %d : %s' % (err.args[0], err.args[1])
            return None

        try:            
            all_info = json.loads(temp)
        except ValueError as err:
            print 'Value Error happend while loads all_info'
            print 'Error %d : %s' % (err.args[0], err.args[1])
            return None

        streams = self.get_streams_info(all_info)

        return streams

def get_streams_info(self,all_info):
        stream_id = 0
        streams = {}
        streams_result = {}

        if all_info == None:
            print 'empty infomation'
            return

        channels = all_info['channels'];
        if channels == None:
            print 'empty channels information'

        for channel in channels:
            streams = channel['streams']
            for stream in streams:
                stream_id = stream['id']
            streams_result[str(stream_id)] = stream

        print streams_result

        return json.dumps(streams_result)