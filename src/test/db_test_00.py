'''
Created on 2011-12-20

@author: dista
'''

from db import *
import threading
import time
from logger import Logger

host = "10.33.0.228"
port = 3306
name = "tvie"
password = "tvierocks"
db_name = "tvie_production2"
#print debug log
logger = Logger(None, 1)

class TestThread(threading.Thread):
    def __init__(self, db_pool, thread_name):
        threading.Thread.__init__(self)
        self.db_pool = db_pool
        self.thread_name = thread_name
        
        
    def run(self):
        print "%s try to get connection" % self.thread_name
        db_connection = self.db_pool.get_one()
        print "%s got connection, the connection id is %d" % (self.thread_name, \
                                                             db_connection.get_id())
        time.sleep(3)
        
def two_connections_pool_and_two_threads():
    max_db = 2
    db_pool = DbPool(max_db, host, port, name, password, db_name, logger)
    
    th1 = TestThread(db_pool, "thread 1")
    th2 = TestThread(db_pool, "thread 2")
    
    th1.start()
    th2.start()
    
if __name__ == "__main__":
    two_connections_pool_and_two_threads()
