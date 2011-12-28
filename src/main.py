'''
Created on 2011-12-17

@author: dista
'''

from config_reader import ConfigReader
from stream_monitor_thread import StreamMonitorThread
from analyzer.analyze_thread import AnalyzeThread
from db import DbPool
from logger import Logger
import conf
import signal, sys

all_threads = {"analyze": None, "stream_monitor": None}

# handle SIGNAL
def terminate_program(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, terminate_program)

def main():
    cr = ConfigReader()
    
    config = cr.read_config_as_dict(conf.CONFIG_PATH)
    
    # create the log, so other module can use it
    #Logger(config['logger']['path'], config['logger']['level'])
    Logger(None, 7)
    
    # create the pool, so other module can use it
    DbPool(4, config['db']['host'], config['db']['port'], config['db']['user'], config['db']['password'], config['db']['db_name'])
    
    az_t = AnalyzeThread()
    smt = StreamMonitorThread(config['get_stream_api_url'], config['read_token'], config['monitor_cdn_in_api'], az_t, config['extra_streams'])
    
    all_threads["analyze_thread"] = az_t
    all_threads["stream_monitor"] = smt 
    
    az_t.start()
    smt.start()
    az_t.join()
    smt.join()
    
if __name__ == "__main__":
    main()
