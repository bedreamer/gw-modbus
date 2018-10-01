# -*- coding: utf8 -*-
from ctypes import *
import zlg.usbcan.can as zlg
import handle


# 波特率映射表， 第一个值，第二个值分别对应Timing0, Timing1
class USBCAN_2E_U(zlg.USBCAN):
    model_name = 'USBCAN-2E-U'
    model_type = 21
    nr_channel = 2
    bps_map = {
        '5Kbps': c_uint32(0x1c01c1),
        '10Kbps': c_uint32(0x1c00e0),
        '20Kbps': c_uint32(0x1600b3),
        '50Kbps': c_uint32(0x1c002c),
        '100Kbps': c_uint32(0x160023),
        '125Kbps': c_uint32(0x1c0011),
        '250Kbps': c_uint32(0x1c0008),
        '500Kbps': c_uint32(0x060007),
        '800Kbps': c_uint32(0x060004),
        '1000Kbps': c_uint32(0x060003),
    }


def get_supported_model_list():
    """
    获取支持的设备型号名列表
    :return: string list
    """
    return [Cls.model_name for Cls in zlg.USBCAN.__subclasses__()]


def get_usbcan_driver_by_model(model_name):
    """
    根据型号名获取设备驱动类
    :param model_name: 型号名
    :return: driver class
    """
    for Cls in zlg.USBCAN.__subclasses__():
        if model_name == Cls.model_name:
            return Cls
    raise NotImplementedError("Unsurported device model", model_name)


def get_usbcan_driver_by_type(model_type):
    """
    根据型号值获取设备驱动类
    :param model_type: 型号值
    :return: driver class
    """
    for Cls in zlg.USBCAN.__subclasses__():
        if model_type == Cls.model_type:
            return Cls
    raise NotImplementedError("Unsurported device type", model_type)


def get_supported_bps_list_by_handle(device_handle):
    """
    根据设备句柄获取支持的波特率列表
    :param device_handle: 设备句柄，通过c_open_device返回
    :return: string list
    """
    devtype, devidx = handle.get(device_handle)
    driver = get_usbcan_driver_by_type(devtype)
    return driver.bps_map.keys()


def get_supported_bps_list_by_model(model_name):
    """
    根据设备型号名获取支持的波特率列表
    :param model_name: 设备型号名
    :param bps: 波特率值字符串
    :return: string list.
    """
    driver = get_usbcan_driver_by_model(model_name)
    return driver.bps_map.keys()


def get_supported_bps_list_by_type(model_type):
    """
    根据设备型号值获取支持的波特率列表
    :param model_type: 设备型号值
    :param bps: 波特率值字符串
    :return: string list.
    """
    driver = get_usbcan_driver_by_type(model_type)
    return driver.bps_map.keys()


def get_bps_config_data_by_handle(device_handle, bps):
    """
    根据设备句柄获取指定波特率的配置字
    :param device_handle: 设备句柄，通过c_open_device返回
    :param bps: 波特率值字符串
    :return: config value.
    """
    devtype, devidx = handle.get(device_handle)
    driver = get_usbcan_driver_by_type(devtype)
    return driver.bps_map[bps]


def get_bps_config_data_by_model(model_name, bps):
    """
    根据设备型号名获取指定波特率的配置字
    :param model_name: 设备型号名
    :param bps: 波特率值字符串
    :return: config value.
    """
    driver = get_usbcan_driver_by_model(model_name)
    return driver.bps_map[bps]


def get_bps_config_data_by_type(model_type, bps):
    """
    根据设备型号值获取指定波特率的配置字
    :param model_type: 设备型号值
    :param bps: 波特率值字符串
    :return: config value.
    """
    driver = get_usbcan_driver_by_type(model_type)
    return driver.bps_map[bps]
