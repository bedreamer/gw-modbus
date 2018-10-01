# -*- coding: utf8 -*-


class USBCAN(object):
    # 有错误
    STATUS_ERR = 0
    # 无错误
    STATUS_OK = 1
    # 设备在线
    STATUS_ONLINE = 2
    # 设备离线
    STATUS_OFFLINE = 3

    model_name = None
    model_type = None
    nr_channel = None
    bps_map = None
