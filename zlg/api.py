# -*- coding: utf8 -*-

# 使用2018-03-01 v0.00 的版本
import _api_v0_00 as _api

# 使用2018-08-07 v3.13 的版本
# import _api_v3_13 as _api


def open_device(usbcan_device_type_number, device_order_number):
    """
    打开USBCAN设备
    :param usbcan_device_type_number: USBCAN设备类型编号
    :param device_order_number: USBCAN设备顺序号，从0开始，第二个设备编号是1，依次类推
    :return: int, <= 0打开失败
    """
    pass


def is_device_online(device_handle):
    """
    测试USBCAN设备是否在线
    :param device_handle: 设备句柄
    :return: bool， 若果在线返回True，否则返回False
    """
    pass


def close_device(device_handle):
    """
    关闭设备
    :param device_handle: 设备句柄
    :return: None
    """
    pass


def open_channel(device_handle, channel_number):
    """
    打开设备通道
    :param device_handle: 设备句柄
    :param channel_number: 通道号，从0开始
    :return: int, 返回通道句柄
    """


def get_cache_counter(channle_handle):
    """
    获取指定通道中已经接受帧的缓存个数
    :param channle_handle: 通道句柄
    :return: int
    """
    pass


def get_frame(channel_handle, count):
    """
    从通道中获取指定个数的帧
    :param channel_handle: 通道句柄
    :param count: 想要获取的帧个数
    :return: list
    """
    pass


def send_frame(channel_handle, frames_list):
    """
    向指定同道中发送帧
    :param channel_handle: 通道句柄
    :param frames_list: 帧列表
    :return: int, 发送的帧个数
    """
    pass


def close_channel(channel_handle):
    """
    关闭通道
    :param channel_handle: 通道句柄
    :return: None
    """
    pass
