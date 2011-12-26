'''
Created on 2011-12-17

@author: dista
'''

import threading
import MySQLdb
import traceback
import logger
from MySQLdb import connections

class DbConnection(connections.Connection):
    timeout = 60
    
    def __init__(self, id, host, port, name, password, db_name):
        self.id = id
        self.logger = logger.get_logger()
        self._is_used = False
        
        connections.Connection.__init__(self, host = host, user = name, passwd = password, db = db_name, port = port, connect_timeout = DbConnection.timeout, \
                                    charset = "utf8", use_unicode = False)
    
        self._is_alive = True
        
    def is_alive(self):
        return self._is_alive
    
    def get_id(self):
        return self.id
    
    def set_alive(self, is_alive):
        '''
        it is the user's duty to set it to un alive if
        they encount Mysql error about connection
        '''
        self._is_alive = is_alive
        
    def is_used(self):
        return self._is_used
    
    def set_used_status(self, is_used):
        self._is_used = is_used
        
    def close(self):
        pass
    
pool = None

def get_pool():
    return pool
    
class DbPool:
    '''
    Python Mysqldb is not thread safe, we must make sure that
    threads won't share DbConnection.
    do not call this twice, use get_pool to get pool after created
    '''
    def __init__(self, max_db, host, port, name, password, db_name):
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
        pool = self
    
    def get_one(self):
        self.logger.debug("%s AC lock" % threading.current_thread())
        self.lock.acquire()
        self.logger.debug("%s ACED lock" % threading.current_thread())
        
        ret = self._get_alive_connection(self.pools)
        
        if ret:
            ret.set_used_status(True)
            self.lock.release()
            return ret
        
        ret = self._gen_one_connection()
        self.logger.debug("%s RL lock" % threading.current_thread())
        self.lock.release()
        self.logger.debug("%s RLED lock" % threading.current_thread())

        if ret != None:
            return ret
        
        while True:
            ev = threading.Event()
            
            self.logger.debug("%s AC queue lock" % threading.current_thread())
            self.event_queue_lock.acquire()
            self.logger.debug("%s ACED queue lock" % threading.current_thread())
            self.event_queue.append(ev)
            self.logger.debug("%s RL queue lock" % threading.current_thread())
            self.event_queue_lock.release()
            self.logger.debug("%s RLED queue lock" % threading.current_thread())
            
            self.logger.debug("wait for event")
            ev.wait()
            self.logger.debug("event wait done")
            
            self.logger.debug("%s AC top pool lock" % threading.current_thread())
            self.top_pools_lock.acquire()
            self.logger.debug("%s ACED top pool lock" % threading.current_thread())
            ret = self._get_alive_connection(self.top_pools)
            self.logger.debug("GOT connection from top_pools")
            if ret:
                ret.set_used_status(True)
            self.logger.debug("%s RL top pool lock" % threading.current_thread())
            self.top_pools_lock.release()
            self.logger.debug("%s RLED top pool lock" % threading.current_thread())
            if ret:
                return ret
            else:
                # the connection user released may lost connection
                self.logger.debug("%s AC lock" % threading.current_thread())
                self.lock.acquire()
                self.logger.debug("%s ACED lock" % threading.current_thread())
                ret = self._gen_one_connection()
                self.logger.debug("%s RL lock" % threading.current_thread())
                self.lock.release()
                self.logger.debug("%s RLED lock" % threading.current_thread())

                if ret:
                    return ret

    def _gen_one_connection(self):
        if self.current_dbc_number < self.max_db:
            con_id = self._gen_con_id()
            
            ret = None
            try:
                ret = DbConnection(con_id, self.host, self.port, self.name, self.password, self.db_name, self.logger)
                self.current_dbc_number += 1
                self.pools.append(ret)
                ret.set_used_status(True)
            except MySQLdb.MySQLError:
                self.logger.debug("Mysql Error, %s" % traceback.format_exc())
            
            return ret
        else:
            return None
            
    def release(self, db_connection):
        in_top = self._is_connection_in_top(db_connection)
        
        self.logger.debug("%s AC lock" % threading.current_thread())
        self.lock.acquire()
        self.logger.debug("%s ACED lock" % threading.current_thread())
        self.logger.debug("%s AC queue lock" % threading.current_thread())
        self.event_queue_lock.acquire()
        self.logger.debug("%s ACED queue lock" % threading.current_thread())
        self.logger.debug("%s AC top pool lock" % threading.current_thread())
        self.top_pools_lock.acquire()
        self.logger.debug("%s ACED top pool lock" % threading.current_thread())
        
        db_connection.set_used_status(False)
        
        if len(self.event_queue) > 0:
            ev = self.event_queue.pop()
            
            if not in_top:
                self.top_pools.append(db_connection)
                self.pools.remove(db_connection)
                
            self.logger.debug("event is notified")
            ev.set()
        else:
            if in_top:
                self.top_pools.remove(db_connection)
                self.pools.append(db_connection)
                

        self.logger.debug("%s RL top pool lock" % threading.current_thread())
        self.top_pools_lock.release()
        self.logger.debug("%s RLED top pool lock" % threading.current_thread())
        self.logger.debug("%s RL queue lock" % threading.current_thread())
        self.event_queue_lock.release()
        self.logger.debug("%s RLED queue lock" % threading.current_thread())
        self.logger.debug("%s RL lock" % threading.current_thread())
        self.lock.release()
        self.logger.debug("%s RLED lock" % threading.current_thread())
            
    def _is_connection_in_top(self, connection):
        try:
            self.top_pools.index(connection)
            return True
        except:
            return False
    
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
    
    def _remove_un_alive_connections(self, pool, un_alive_connections):
        for con in un_alive_connections:
            pool.remove(con)
            self.current_dbc_number -= 1
            try:
                con.close()
            except Exception:
                pass           
