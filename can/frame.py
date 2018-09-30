# -*- coding: utf8 -*-


class CANFrame(object):
    def __init__(self, id, tsp, data):
        self.id = id
        self.tsp = tsp
        self.data = data
