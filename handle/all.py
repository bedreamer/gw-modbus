# -*- coding: utf8 -*-


_handle_map = dict()
_handle_alloc_seed = 100
_handle_total_count = 0


class Token(object):
    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def payload(self):
        return tuple(self.args)


def new(token):
    global _handle_map, _handle_alloc_seed, _handle_total_count

    if issubclass(token.__class__, Token) is False:
        raise TypeError("token must be a Token child.")

    h = _handle_alloc_seed
    _handle_alloc_seed = _handle_alloc_seed + 1
    _handle_total_count = _handle_total_count + 1

    _handle_map[str(h)] = token
    print("+ new handle:", h)
    return h


def delete(h):
    global _handle_map, _handle_alloc_seed, _handle_total_count

    if test(h) is None:
        return

    _handle_total_count = _handle_total_count - 1
    del _handle_map[str(h)]
    print("- delete handle:", h)


def get(h):
    global _handle_map

    return _handle_map[str(h)].payload()[0] if test(h) is True else None


def test(h):
    global _handle_map

    return True if str(h) in _handle_map else False


def find(payload):
    global _handle_map

    for key, value in _handle_map.items():
        if value == payload:
            return int(key)

    return None


def all():
    global _handle_map
    return _handle_map.items()
