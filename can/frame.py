# -*- coding: utf8 -*-


class CANFrame(object):
    def __init__(self, id, tsp, data):
        self.id = id
        self.tsp = tsp
        self.data = data

    def __str__(self):
        data = " ".join(["%02X" % data for data in self.data])
        sid = "%08X:" % self.id
        return "".join([sid, ' [', data, ']'])
