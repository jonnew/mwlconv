import json


def intersect(a, b):
    return list(set(a) & set(b))


def flat_parse(keys, json_fd):

    results = {}
    for k in keys:
        results[k] = []

    def _decode_dict(a_dict):
        for k in keys:
            try: results[k].append(a_dict[k])
            except KeyError: pass
        return a_dict

    json.load(json_fd, object_hook=_decode_dict)  # return value ignored
    return results
