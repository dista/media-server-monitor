from model import helper
import json

def test_01():
    streams = json.load(open("../../test_data/streams.json"))
    print helper.build_insert_values(streams)


if __name__ == "__main__":
    test_01()
