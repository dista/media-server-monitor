from logger import Logger


DEBUG_LOG_MSG = "debug log should be printed"
WARN_LOG_MSG = "warn log should be printed"
ERROR_LOG_MSG = "error log should be printed"

def test_normal_file_logger():
    lg = Logger("/tmp/media-monitor-test.log", 1)
    lg.debug(DEBUG_LOG_MSG)
    lg.warn(WARN_LOG_MSG)
    lg.error(ERROR_LOG_MSG)
    lg.close()

if __name__ == "__main__":
    test_normal_file_logger()
