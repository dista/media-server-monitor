def parse_ms_monitor_result(http_body):
    lines = http_body.split("\n")
    ret = dict([line.split(":") for line in lines if line.strip() != ''])

    float_vals_key = ["average_upstream_kbps", "average_downstream_kbps"]
    for key in ret.keys():
        val = ret[key].strip()
        if key in float_vals_key:
            ret[key] = float(val)
        else:
            ret[key] = int(val)

    return ret
