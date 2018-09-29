# -*- coding: utf8 -*-
from ctypes import *


# 最大支持的设备个数
ZLG_SUPPORTED_MAX_CAN_DEVICE_COUNT = 16

# 当前系统支持的设备型号
_zlg_supported_device_model_maps = {
            'USBCAN-I/I+': 3,
            'USBCAN-II/II+': 4,
            'USBCAN-E-U': 20,
            'USBCAN-2E-U/CANalyst-II+': 21,
            'USBCAN-4E-U': 31,
            'USBCAN-8E-U': 34,
        }

# 动态库名称, 需要放在当前脚本目录
_zlg_dll_file_name = 'zlgcan.dll'

# dll 句柄，由windll.LoadLibrary返回
_zlg_dll_handle = None

# CAN 设备句柄
_zlg_device_handle = dict()


def zlg_get_supported_device_model_list(self):
    """
    获取支持的设备名称列表
    :param self:
    :return: list
    """
    global _zlg_supported_device_model_maps
    return _zlg_supported_device_model_maps


def open_can_device(device_model, device_number=None):
    """

    :param device_model: 传入设备类型
    :param device_number: 传入设备号
    :return: int
    """
    global _zlg_dll_file_name
    global _zlg_dll_handle
    global _zlg_device_handle
    global _zlg_supported_device_model_maps

    try:
        device_type = _zlg_supported_device_model_maps[device_model]
    except:
        raise NotImplemented("unsupported device", device_model)

    if device_number is None or device_number < 0 or device_number > ZLG_SUPPORTED_MAX_CAN_DEVICE_COUNT:
        device_number = 0

    # 需要使用这个唯一的标识来存储已经打开的设备
    uniq_device_name = "".join([device_model, "@", str(device_number)])

    # 若已经打开了则不去重复打开
    if _zlg_device_handle[uniq_device_name] is not None:
        return _zlg_device_handle[uniq_device_name]

    # 避免重复加载dll文件
    _zlg_dll_handle = windll.LoadLibrary(_zlg_dll_file_name) if _zlg_dll_handle is None else _zlg_dll_handle

    try:
        device_handle = _zlg_dll_handle.ZCAN_OpenDevice(device_type, device_number, 0)
    except Exception as e:
        print(e)


def close_can_device(device):
    device.ZCAN_CloseDevice()


def zlg_read_frame(self):
    pass


def zlg_write_frame(self):
    pass

