def build_insert_values(obj):
    keys = "( %s )" % (", ".join(obj.keys()))
    values = ""

    for o in obj:
        val = "( "
        for v in o.items():
            if any([isinstance(o[key], cls) for cls in [str, unicode]]):
                val += "'%s', " % v
            else:
                val += "%s, " % v

        val.rstrip(', ') + " )"
    values  += val + ","

    values.rstrip(",")

    return "% VALUES %s" % (keys, values)
