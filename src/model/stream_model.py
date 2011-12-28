'''
Created on 2011-12-17

@author: dista
'''

import json
import db
import MySQLdb
from model import helper

class StreamModel:
    def __init__(self):
        self.model_name = "mms_stream"

    def get_by_stream_ids(self, stream_ids):
        if stream_ids == None or len(stream_ids) == 0:
            return []

        return db.execute("SELECT * FROM %s WHERE stream_id in (%s)" % (self.model_name, ", ".join([str(i) for i in stream_ids])))

    def get_all(self):
        return db.execute("SELECT * FROM %s" % self.model_name)
    
    def get_by_stream_id(self, stream_id):
        return db.execute("SELECT * FROM %s WHERE stream_id = %d" % (self.model_name, stream_id))

    def delete_by_ids(self, ids):
        if ids == None or len(ids) == 0:
            return True

        db.execute("DELETE FROM %s WHERE id in (%s)" % (self.model_name, ", ".join([str(i) for i in ids])))

    def update_by_stream_id(self, stream):
        set_state = "SET "
        for key in stream.keys():
            if key == 'stream_id':
                continue
            val = stream[key] 
            if any([isinstance(stream[key], cls) for cls in [str, unicode]]):
                set_state += "%s='%s', " % (key, val)
            else:
                set_state += "%s=%s, " %(key, val)

        if set_state.endswith(", "):
            set_state = set_state[:-2]

        db.execute("UPDATE %s %s where stream_id=%d" % (self.model_name, set_state, stream['stream_id']))

    def add(self, streams):
        if streams == None or len(streams) == 0:
            return

        insert_value = helper.build_insert_values(streams)

        db.execute("INSERT INTO %s %s" % (self.model_name, insert_value))
