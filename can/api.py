# -*- coding: utf8 -*-
# 使用2018-03-01 v0.00 的版本
# import _api_v0_00 as _api

# 使用2018-08-07 v3.13 的版本
from zlg.usbcan import _api_v3_13 as _api


def get_supported_bps_list():
    """
    返回驱动支持的波特率列表
    :return: string list
    """
    return _api.get_supported_bps_list()


def get_supported_model_list():
    """
    获取支持的设备列表
    :return: string list
    """
    return _api.get_supported_model_list()


def get_device_driver(model_name):
    """
    获取指定设备的驱动
    :param model_name: 设备型号名称
    :return: 返回设备驱动类
    """
    return _api.get_usbcan_driver(model_name)


def open_device(usbcan_device_type_number, device_order_number):
    """
    打开USBCAN设备
    :param usbcan_device_type_number: USBCAN设备类型编号
    :param device_order_number: USBCAN设备顺序号，从0开始，第二个设备编号是1，依次类推
    :return: int, <= 0打开失败
    """
    return _api.c_open_device(usbcan_device_type_number, device_order_number)


def is_device_online(device_handle):
    """
    测试USBCAN设备是否在线
    :param device_handle: 设备句柄
    :return: bool， 若果在线返回True，否则返回False
    """
    return _api.is_device_online(device_handle)


def close_device(device_handle):
    """
    关闭设备
    :param device_handle: 设备句柄
    :return: bool
    """
    return _api.c_close_device(device_handle)


def open_channel(device_handle, channel_number, bps, work_mode=None, acc_code=None, acc_mask=None):
    """
    打开设备通道
    :param device_handle: 设备句柄
    :param channel_number: 通道号，从0开始
    :param bps: 该通道的波特率值
    :param work_mode: 工作模式， 0: 正常，1：仅监听
    :param acc_code: 验收码，
    :param acc_mask: 屏蔽码
    :return: int, 返回通道句柄
    """
    if work_mode is None:
        work_mode = 1

    if acc_code is None:
        acc_code = 0

    if acc_mask is None:
        acc_mask = 0xffffffff

    return _api.c_open_channel(device_handle, channel_number, bps, work_mode, acc_code, acc_mask)


def clear_cache(channel_handle):
    """
    清空接受缓冲区
    :param channel_handle:
    :return: bool
    """
    return _api.c_clear_cache(channel_handle)


def get_cache_counter(channle_handle):
    """
    获取指定通道中已经接受帧的缓存个数
    :param channle_handle: 通道句柄
    :return: int
    """
    return _api.c_get_cache_counter(channle_handle)


def get_frame(channel_handle, count=None, wait_ms=None):
    """
    从通道中获取指定个数的帧
    :param channel_handle: 通道句柄
    :param count: 想要获取的帧个数
    :param wait_ms: 等待的时长，单位是毫秒，若值为-1则表示不超时，一直等待
    :return: canframe.CANFrame list
    """
    if count is None:
        count = 1
    if wait_ms is None:
        wait_ms = -1

    return _api.c_get_frame(channel_handle, count, wait_ms)


def send_frame(channel_handle, frames_list):
    """
    向指定同道中发送帧
    :param channel_handle: 通道句柄
    :param frames_list: canframe.CANFrame list
    :return: int, 发送的帧个数
    """
    return _api.c_send_frame(channel_handle, frames_list)


def close_channel(channel_handle):
    """
    关闭通道
    :param channel_handle: 通道句柄
    :return: bool
    """
    return _api.c_close_channel(channel_handle)


def reset_channel(channel_handle):
    """
    复位通道
    :param channel_handle: 通道句柄
    :return: bool
    """
    return _api.c_reset_channel(channel_handle)