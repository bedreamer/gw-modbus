# -*- coding: utf8 -*-


_handle_map = dict()
_handle_alloc_seed = 100
_handle_total_count = 0


def new(*args):
    global _handle_map, _handle_alloc_seed, _handle_total_count

    h = _handle_alloc_seed
    _handle_alloc_seed = _handle_alloc_seed + 1
    _handle_total_count = _handle_total_count + 1

    _handle_map[str(h)] = args
    return h


def delete(h):
    global _handle_map, _handle_alloc_seed, _handle_total_count

    if test(h) is None:
        return

    _handle_total_count = _handle_total_count - 1
    del _handle_map[str(h)]


def get(h):
    global _handle_map

    return _handle_map[str(h)] if test(h) is True else None


def test(h):
    global _handle_map

    return True if str(h) in _handle_map else False
