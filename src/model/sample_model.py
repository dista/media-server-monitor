'''
Created on 2011-12-17

@author: dista
'''
import db
import MySQLdb
from model import helper

class SampleModel:
    def __init__(self):
        self.model_name = "mms_samples"
        
    def add(self, stream):
        pass
    
    def update(self, id, stream):
        pass
    
    def delete_by_stream_ids(self, mms_stream_ids):
        if mms_stream_ids == None || len(mms_stream_ids) == 0:
            return True

        db.excute("DELETE FROM %s WHERE mms_stream_id in (%s)" % (self.model_name, ", ".joins(mms_stream_ids))
    
    def get_by_stream_id(self, stream_id):
        pass
    
    def get_by_id(self, id):
        pass

    def insert(self, sample):
        insert_value = helper.build_insert_values([sample])
        db.excute("INSERT INTO %s %s" % (self.model_name, insert_value))

        self._delete_if_exceed(sample['mms_stream_id'], 100)

    def _delete_if_exceed(self, mms_stream_id, num):
        result = db.excute("SELECT count(*) FROM %s where mms_stream_id = %d" % mms_stream_id)
        exists_num = result[0]['count(*)']

        if exists_num <= num:
            return

        result = db.excute("SELECT id FROM %s order by id asc limit 1" % self.model_name)
        db.excute("DELETE FROM %s where id=%d" % (self.model_name, result[0]['id']))
            
