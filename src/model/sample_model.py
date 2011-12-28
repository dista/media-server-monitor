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
        
    def delete_by_stream_ids(self, mms_stream_ids):
        if mms_stream_ids == None or len(mms_stream_ids) == 0:
            return True

        db.execute("DELETE FROM %s WHERE mms_stream_id in (%s)" % (self.model_name, ", ".join([str(i) for i in mms_stream_ids])))
    
    def get_by_mms_stream_id(self, mms_stream_id):
        return db.execute("SELECT * FROM %s WHERE mms_stream_id = %d" % (self.model_name, mms_stream_id))
    
    def get_by_id(self, id):
        pass

    def insert(self, sample):
        insert_value = helper.build_insert_values([sample])
        db.execute("INSERT INTO %s %s" % (self.model_name, insert_value))

        self._delete_if_exceed(sample['mms_stream_id'], 100)

    def _delete_if_exceed(self, mms_stream_id, num):
        result = db.execute("SELECT count(*) FROM %s where mms_stream_id = %d" % (self.model_name, mms_stream_id))
        exists_num = result[0]['count(*)']

        if exists_num <= num:
            return

        result = db.execute("SELECT id FROM %s order by id asc limit 1" % self.model_name)
        db.execute("DELETE FROM %s where id=%d" % (self.model_name, result[0]['id']))
            
