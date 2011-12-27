'''
Created on 2011-12-18

@author: dista
'''
import os
import sys
import urllib
import urllib2
import json
import config_reader
from exception import InvalidApiData, ApiCallError

from urllib2 import URLError, HTTPError

class ApiServerModel:
    def __init__(self, get_stream_api_url, read_token, monitor_cdn_in_api):
        self.get_stream_api_url = get_stream_api_url
        self.readtoken = read_token
        self.monitor_cdn_in_api = monitor_cdn_in_api
        
    def get(self):
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
            raise ApiCallError(err)

        try:            
            all_info = json.loads(temp)
        except ValueError as err:
            raise InvalidApiData("API returns: %s" % temp)

        streams = self._get_streams_info(all_info)

        return streams

    def _get_streams_info(self,all_info):
        streams_result = []

        channels = all_info['channels'];

        for channel in channels:
            server = channel['server'][0]
            streams = channel['streams']
            for stream in streams:
                streams_result.append({"stream_id": stream['id'],                                     
                                      "unify_name": self._build_unify_name(server, channel, stream),
                                      "sample_interface": self._build_sample_interface(server, channel, stream)
                                      })
         
        return streams_result


    def _build_unify_name(self, server, channel, stream, is_cdn):
        return "%s/%s/%s/%s" % (server.name, channel.customer_name, channel.display_name, stream.name)

    def _build_sample_interface(self, server, channel, stream, interface, is_cdn):
        return "http://"
