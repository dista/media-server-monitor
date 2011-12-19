'''
Created on 2011-12-17

@author: dista
'''

import threading
import MySQLdb

class DbConnection(MySQLdb.Connection):
    timeout = 60
    
    def __init__(self, id, host, port, name, password, db_name, logger = None):
        self.id = id
        self.host = host
        self.port = port
        self.name = name
        self.password = password
        self.db_name = db_name
        self.logger = logger
        self.is_used = False
        
        MySQLdb.Connection.__init__(self, host, name, password, db_name, DbConnection.timeout, \
                                    charset = "utf8", use_unicode = False)
    
        self.is_alive = True
        
    def is_alive(self):
        return self.is_alive
    
    def get_id(self):
        return self.id
    
    def set_alive(self, is_alive):
        '''
        it is the user's duty to set it to un alive if
        they encount Mysql error about connection
        '''
        self.is_alive = is_alive
        
    def is_used(self):
        return self.is_used
    
    def set_used_status(self, is_used):
        self.is_used = is_used
        
    def close(self):
        pass
    
class DbPool:
    '''
    Python Mysqldb is not thread safe, we must make sure that
    threads won't share DbConnection
    '''
    def __init__(self, max_db, host, port, name, password, db_name, logger):
        self.host = host
        self.port = port
        self.name = name
        self.db_name = db_name
        self.password = password
        self.logger = logger
        self.max_db = max_db
        self.top_pools = []
        self.event_queue = [] 
        self.pools = []
        self.current_dbc_number= 0
        self.con_id = 0
        self.lock = threading.Lock()
        self.top_pools_lock = threading.Lock()
        self.event_queue_lock = threading.Lock()
    
    def get_one(self):
        self.lock.acquire()
        
        ret = self._get_alive_connection(self.pools)
        
        if not ret:
            ret.set_used_status(True)
            self.lock.release()
            return ret
        
        if self.current_dbc_number < self.max_db:
            con_id = self._gen_con_id()
            
            ret = None
            try:
                ret = DbConnection(con_id, self.host, self.port, self.name, self.password, self.db_name, self.logger)
                self.current_dbc_number += 1
                self.pools.append(ret)
            except MySQLdb.MySQLError:
                pass
            finally:
                self.lock.release()
            
            return ret
        
        
        while True:
            ev = threading.Event()
            
            self.event_queue_lock.acquire()
            self.event_queue.append(ev)
            self.event_queue_lock.release()
            
            ev.wait()
            
            self.top_pools_lock.acquire()
            ret = self._get_alive_connection(self.top_pools)
            self.top_pools_lock.release()
            if ret:
                return ret
                
            
    def release(self, db_connection):
        if not db_connection.is_alive():
            return
        
        in_top = self._is_connection_in_top(db_connection)
        
        self.event_queue_lock.acquire()
        self.lock.acquire()
        self.top_pools_lock.acquire()
        
        db_connection.set_used_status(False)
        
        if len(self.event_queue) > 0:
            ev = self.event_queue.pop()
            
            if not in_top:
                self.top_pools.append(db_connection)
                self.pools.remove(db_connection)
                
            ev.set()
        else:
            if in_top:
                self.top_pools.remove(db_connection)
                self.pools.append(db_connection)
                

        self.top_pools_lock.lock()
        self.event_queue_lock.release()
        self.lock.release()
            
    def _is_connection_in_top(self, connection):
        try:
            if self.top_pools.index(connection):
                return True
        except:
            return False
    
    def _release_to_pool(self, db_connection, pool):
        pass        
    
    def _gen_con_id(self):
        self.con_id += 1
        return self.con_id
    
    def _get_alive_connection(self, connection_pool):
        ret = None
        un_alive_connections = []
        for con in connection_pool:
            if not con.is_used():
                if not con.is_alive():
                    un_alive_connections.append(con)
                else:
                    ret = con
                    break
                
        self._remove_un_alive_connections(connection_pool, un_alive_connections)
        
        return ret
    
    def _remove_un_active_connections(self, pool, un_alive_connections):
        for con in un_alive_connections:
            pool.remove(con)
            try:
                con.close()
            except Exception:
                pass           