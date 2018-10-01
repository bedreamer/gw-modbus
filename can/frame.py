# -*- coding: utf8 -*-


class CANFrame(object):
    def __init__(self, id, tsp, data, size=None):
        self.id = id
        self.tsp = tsp
        if isinstance(data, list) or isinstance(data, tuple):
            self.data = data
        else:
            self.data = list(data)[: size]

    def __str__(self):
        data = " ".join(["%02X" % data for data in self.data])
        sid = "%08X:" % self.id
        return "".join([str(self.tsp), " ", sid, ' [', data, ']'])
