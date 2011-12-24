'''
Created on 2011-12-17

@author: dista
'''

from config_reader import ConfigReader
from stream_monitor_thread import StreamMonitorThread
from analyzer.analyze_thread import AnalyzeThread
from db import DbPool
from logger import Logger

CONFIG_PATH = "/usr/local/tvie/config/media-server-monitor.conf"

all_threads = {"analyze": None, "stream_monitor": None}

# handle SIGNAL
def terminate_program():
    pass

def main():
    cr = ConfigReader()
    
    config = cr.read_config_as_dict(CONFIG_PATH)
    
    # create the log, so other module can use it
    Logger(config.logger.path, config.logger.level)
    
    # create the pool, so other module can use it
    DbPool(config.db.host, config.db.port, config.db.name, config.db.password)
    
    az_t = AnalyzeThread()
    smt = StreamMonitorThread(config.get_stream_api_url, az_t)
    
    all_threads["analyze_thread"] = az_t
    all_threads["stream_monitor"] = smt 
    
    az_t.start()
    smt.start()
    az_t.join()
    smt.join()
    
if __name__ == "__main__":
    main()