def build_insert_values(obj_list):
    if obj_list == None or len(obj_list) == 0:
        raise Exception("parameter should be a list contains dict")

    keys = "( %s )" % (", ".join(obj_list[0].keys()))
    values = ""

    for o in obj_list:
        val = "( "
        for k in o.keys():
            v = o[k]
            if any([isinstance(v, cls) for cls in [str, unicode]]):
                val += "'%s', " % v
            else:
                val += "%s, " % v


        val = val.rstrip(", ") + " )"
        values  += val + ","

    values = values.rstrip(",")

    return "%s VALUES %s" % (keys, values)
