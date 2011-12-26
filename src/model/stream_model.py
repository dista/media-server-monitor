'''
Created on 2011-12-17

@author: dista
'''

import json
import MySQLdb

class StreamModel:
    def __init__(self, db):
        self.db = db
        self.cursor = None

    def getCursor(self):
        try:
            self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        except MySQLdb.Error, err:
            print 'MySQLdb Error %d : %s.\n' % (err.args[0], err.args[1])
            self.db.close()


    def add(self, strui_errorseams):
        add_value = ''
        value = ''

        if streams == None:
            print 'Empty stream information.\n'
            return

        for stream in streams:
            if streams['id'] != None \
                and streams['interface'] != None:
                add_value = add_value + '(%d, %s),' % (stream['id'], stream['sample_interface'])

        value = add_value.rstrip(',') + ';'
        sql = 'INSERT INTO mms_stream \
                (stream_id, sample_interface) \
                VALUES %s' % (value)

        try:
            self.cursor.execute(sql)
        except MySQLdb.Error, err:
            print 'Add values into mms_stream failed.'
            print 'MySQLdbui_errors Error %d : %s\n' % (err.args[0], args[1])

        return

    
    def update(self, streams):
        update_value = ''
        value = ''

        if streams == None:
            print 'Empty stream information.\n'
            return

        for stream in streams:
            if streams['id'] != None \
                and streams['interface'] != None:
                update_value = update_value + '(%d, %s),' % (stream['id'], stream['sample_interface'])

        value = update_value.rstrip(',') + ';'
        sql = 'UPDATE mms_stream \
                (stream_id, sample_interface) \
                VALUES %s' % (value)

        try:
            self.cursor.execute(sql)
        except MySQLdb.Error, err:
            print 'UPDATE values in mms_stream failed.'
            print 'MySQLdb Error %d : %s\n' % (err.args[0], args[1])

        return

    
    def delete(self, streams):
        delete_value = ''
        value = ''

        if streams == None:
            print 'Empty stream information.\n'
            return

        for stream in streams:
            if streams['id'] != None \
                and streams['interface'] != None:
                delete_value = delete_value + '(stream=%d, sample_interface="%s"), OR' \
                % (stream['id'], stream['sample_interface'])

        value = delete_value.rstrip(', OR') + ';'
        sql = 'DELETE FROM mms_stream\
                WHERE stream_id=%d \
                AND sample_interface="%s";' % (value)

        try:
            self.cousor.execute(sql)
        except MySQLdb.Error err:
            print 'DELETE values in mms_stream failed.'
        dict_objs = {}

        if query_result == None:
           print 'Query result is empty\n'
           return

        for result in results:
            dic_obj = {}
            for obj in result:
                dic_obj[obj] = str(result[obj])
            dic_objs[str(result['id'])] = dic_objlues in mms_stream failed.
            print 'MySQLdb Error %d : %s\n' % (err.args[0], args[1])

        return

    
    def get(self):
        streams = None
        dict_stream = None
            
        sql = 'SELECT * FROM mms_stream;'

        try:
            self.cursor.execute(sql)
            stream = self.cursor.fetchall()
        except MySQLdb.Error, err:
            print 'GET data from mms_stream failed.'
            print 'MySQLdb Error %d : %s\n' % (err.args[0], args[1])
        return

        if len(stream) == 0:
            print 'Empty set\n'
            return None
        else:
            dict_stream = self.result_to_dict(streams)

        return json.dumps(dict_stream)

    
    def get_by_id(self, stream_id);
        streams = Nonesended_requests
        dict_stream = None
            
        sql = 'SELECT * FROM mms_stream\
                WHERE id="%d";' % (stream_id)

        try:
            self.cursor.execute(sql)
            stream = self.cursor.fetchall()
        except MySQLdb.Error, err:
            print 'Get stream from database failed.\n'
            print 'MySQLdb Error %d : %s\n' % (err.args[0], args[1])
        return

        if len(stream) == 0:
            print 'Empty set\n'
            return None
        else:
            dict_stream = self.result_to_dict(streams)

        return json.dumps(dict_stream)

    def result_to_dict(self, results):
        dict_objs = {}

        if query_result == None:
            print 'Query result is empty\n'
            return

        for result in results:
            dic_obj = {}
            for obj in result:
                dic_obj[obj] = str(result[obj])
            dic_objs[str(result['id'])] = dic_obj

	return json.dumps(dict_objs)
