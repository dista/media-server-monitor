from db import *
import threading
import time
import sys
import db
from logger import Logger

host = "10.33.0.57"
port = 3306
name = "tvie"
password = "tvierocks"
db_name = "tvie_production2"
#print debug log
logger = Logger(None, 0)

def test_01():
    DbPool(4, host, port, name, password, db_name)

    result = db.execute("SELECT * FROM mms_stream where id=88")
    print len(result) == 0

if __name__ == "__main__":
    test_01()
