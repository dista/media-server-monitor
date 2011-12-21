'''
Created on 2011-12-17

@author: dista
'''
class Analyzer:
    def __init__(self):
        pass
    
    def do_analyze(self, http_response, exists_samples):
        ret = {"score": 0, "sample": None}

        if http_response.header['code'] != 200:
            return ret

        ret['sample'] = self._parse_result_to_dict(http_response)

        #TODO: caculate score
        return ret

    def _parse_result_to_dict(self, http_response):
        lines = http_response.body.split("\n")
        ret = dict([line.split(":") for line in lines if line.strip() != ''])

        float_vals_key = ["average_upstream_kbps", "average_downstream_kbps"]
        for key in ret.keys():
            val = ret[key].strip()
            if key in float_vals_key:
                ret[key] = float(val)
            else:
                ret[key] = int(val)

        return ret


