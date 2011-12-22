from common.http import HttpResponse
from analyzer.analyzer import Analyzer
from common import parser
from datetime import datetime
import os

def get_sample_names(_dir):
    sample_names = os.listdir(_dir)
    sample_names.sort()
    sample_names.reverse()

    return sample_names

def _test(_dir):
    sample_names = get_sample_names(_dir)
    monitor_data = []

    first_http_response = None
    for sample_name in sample_names:
        http_response = HttpResponse(open("%s/%s" % (_dir, sample_name)).read())

        if first_http_response == None:
            first_http_response = http_response
        parsed_data = parser.parse_ms_monitor_result(http_response.body)
        parsed_data['sample_time'] = datetime.fromtimestamp(int(sample_name.split('.')[0]))

        monitor_data.append(parsed_data)

    az = Analyzer()
    result = az.do_analyze(monitor_data[0]['sample_time'], first_http_response, monitor_data[1:])

    return result
    
def test_00():
    _dir = "../test_data/analyzer/upstream_up"
    result = _test(_dir)

    print "stream up:", result['score'], "\n"

def test_01():
    _dir = "../test_data/analyzer/upstream_down"
    result = _test(_dir)
    print 'stream down:', result['score'], "\n"

def test_02():
    _dir = "../test_data/analyzer/upstream_limit_10k"
    result = _test(_dir)
    print 'limit 10k:', result['score'], "\n"

def test_03():
    _dir = "../test_data/analyzer/upstream_limit_5k"
    result = _test(_dir)

    print 'limit 5k:', result['score'], "\n"

def test_04():
    _dir = "../test_data/analyzer/upstream_limit_200k"
    result = _test(_dir)

    print 'limit 200k:', result['score'], "\n"

def test_05():
    _dir = "../test_data/analyzer/upstream_limit_100k"
    result = _test(_dir)

    print 'limit 100k:', result['score'], "\n"
def test_06():
    _dir = "../test_data/analyzer/upstream_limit_60k"
    result = _test(_dir)

    print 'limit 60k:', result['score'], "\n"
if __name__ == "__main__":
    test_00()
    test_01()
    test_02()
    test_03()
    test_04()
    test_05()
    test_06()
