# -*- coding: utf8 -*-
import os
from ctypes import *
import zlg.can as can


# 动态库名称, 需要放在当前脚本目录
_zlg_dll_file_name = ''.join([os.path.dirname(__file__), '/driver/v3.13/ControlCAN.dll'])

# dll 句柄，由windll.LoadLibrary返回
# 这里用cdll而不用windll的原因是函数声明方式不同
# 解释参见: https://blog.csdn.net/jiangxuchen/article/details/8741613
_zlg_dll = windll.LoadLibrary(_zlg_dll_file_name)


# 句柄计数器
_handle_counter = 100

# USBCAN设备句柄映射
_usbcan_device_handle_maps = dict()

# USBCAN通道句柄映射
_usbcan_channel_handle_maps = dict()


def c_open_device(devtype, devidx):
    global _zlg_dll
    global _handle_counter
    global _usbcan_device_handle_maps

    status = _zlg_dll.VCI_OpenDevice(devtype, devidx, 0)
    handle, _handle_counter = _handle_counter, _handle_counter + 1
    if status == 1:
        _usbcan_device_handle_maps[str(handle)] = (devtype, devidx)
        return handle
    else:
        return 0


# CAN硬件结构体
class _VCI_BOARD_INFO(Structure):
    _fields_ = [('hw_Version', c_uint16),
                ('fw_Version', c_uint16),
                ('dr_Version', c_uint16),
                ('in_Version', c_uint16),
                ('irq_Num', c_uint16),
                ('can_Num', c_byte),
                ('str_Serial_num', c_char * 20),
                ('str_hw_Type', c_char * 40),
                ('Reserved', c_uint16 * 16)]


def is_device_online(device_handle):
    global _zlg_dll
    global _usbcan_device_handle_maps

    devtype, devidx = _usbcan_device_handle_maps[str(device_handle)]
    info = _VCI_BOARD_INFO()
    status = _zlg_dll.VCI_ReadBoardInfo(devtype, devidx, POINTER(info))

    return True if status == 1 else False


def c_close_device(device_handle):
    global _zlg_dll
    global _usbcan_device_handle_maps

    devtype, devidx = _usbcan_device_handle_maps[str(device_handle)]
    return True if 0 == _zlg_dll.VCI_CloseDevice(devtype, devidx) else False


# CAN配置结构体
class _VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', c_ulong),
                ('AccMask', c_ulong),
                ('Reserved', c_ulong),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]


# 波特率映射表， 第一个值，第二个值分别对应Timing0, Timing1
_bps_table = {
    '5Kbps': (0xBF, 0xFF),
    '10Kbps': (0x31, 0x1C),
    '20Kbps': (0x18, 0x1C),
    '40Kbps': (0x87, 0xFF),
    '50Kbps': (0x09, 0x1C),
    '80Kbps': (0x83, 0Xff),
    '100Kbps': (0x04, 0x1C),
    '125Kbps': (0x03, 0x1C),
    '200Kbps': (0x81, 0xFA),
    '250Kbps': (0x01, 0x1C),
    '400Kbps': (0x80, 0xFA),
    '500Kbps': (0x00, 0x1C),
    '666Kbps': (0x80, 0xB6),
    '800Kbps': (0x00, 0x16),
    '1000Kbps': (0x00, 0x14),
}


def get_supported_bps_list():
    global _bps_table
    return _bps_table.keys()


class USBCAN_I_OR_I_PLUS(can.USBCAN):
    model = 'USBCAN-I/I+'
    model_type = 3
    nr_channel = 2


class USBCAN_II_OR_II_PLUS(can.USBCAN):
    model_name = 'USBCAN-II/II+'
    model_type = 4
    nr_channel = 2


class USBCAN_E_U(can.USBCAN):
    model_name = 'USBCAN-E-U'
    model_type = 20
    nr_channel = 2


class USBCAN_2E_U(can.USBCAN):
    model_name = 'USBCAN-2E-U/CANalyst-II+'
    model_type = 21
    nr_channel = 2


class USBCAN_4E_U(can.USBCAN):
    model_name = 'USBCAN-4E-U'
    model_type = 31
    nr_channel = 2


class USBCAN_8E_U(can.USBCAN):
    model_name = 'USBCAN-8E-U'
    model_type = 34
    nr_channel = 2


def get_supported_model_list():
    return [Cls.model_name for Cls in can.USBCAN.__subclasses__()]


def get_usbcan_driver(model_name):
    for Cls in can.USBCAN.__subclasses__():
        if model_name == Cls:
            return Cls
    raise NotImplementedError("Unsurported device model", model_name)


def c_open_channel(device_handle, channel_number, bps, work_mode, acc_code, acc_mask):
    global _zlg_dll
    global _handle_counter
    global _bps_table
    global _usbcan_device_handle_maps
    global _usbcan_channel_handle_maps

    devtype, devidx = _usbcan_device_handle_maps[str(device_handle)]

    channel, _handle_counter = _handle_counter, _handle_counter + 1
    ic = _VCI_INIT_CONFIG()

    ic.AccCode, ic.AccMask = acc_code, acc_mask
    ic.Filter = 0
    ic.Timing0, ic.Timing1 = _bps_table[bps]
    ic.Mode = work_mode

    status = _zlg_dll.VCI_initCAN(devtype, devidx, channel_number, c_void_p(ic))
    if status == 1:
        _usbcan_channel_handle_maps[str(channel)] = (devtype, devidx, channel_number, bps, work_mode)
    else:
        print("configure failed, dev, dev-idx, channel-idx", devtype, devidx, acc_mask)
        return 0


def c_clear_cache(channel_handle):
    global _zlg_dll
    global _usbcan_channel_handle_maps

    devtype, devidx, channel_number, _, _ = _usbcan_channel_handle_maps[str(channel_handle)]
    return True if 0 == _zlg_dll.VCI_ClearBuffer(devtype, devidx, channel_number) else False


def c_get_cache_counter(channel_handle):
    global _zlg_dll
    global _usbcan_channel_handle_maps

    devtype, devidx, channel_number, _, _ = _usbcan_channel_handle_maps[str(channel_handle)]

    return _zlg_dll.VCI_GetReceiveNum(devtype, devidx, channel_number)


class _VCI_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ('TimeStamp', c_uint),
                ('TimeFlag', c_byte),
                ('SendType', c_byte),
                ('RemoteFlag', c_byte),
                ('ExternFlag', c_byte),
                ('DataLen', c_byte),
                ('Data', c_byte * 8),
                ('Reserved', c_byte * 3)]


def c_get_frame(channel_handle, count, wait_ms):
    global _zlg_dll
    global _usbcan_channel_handle_maps

    devtype, devidx, channel_number, _, _ = _usbcan_channel_handle_maps[str(channel_handle)]

    CAN_OBJ_ARRY_TYPE = _VCI_CAN_OBJ() * count
    buffer_list = CAN_OBJ_ARRY_TYPE()

    read_count = _zlg_dll.VCI_Receive(devtype, devidx, channel_number, POINTER(buffer_list), count, wait_ms)
    if read_count in (0xffffffff, -1, 0):
        return list()

    return [zlg.can.CANFrame(id=obj.ID, tsp=obj.TimeStamp, data=obj.Data) for obj in buffer_list]


def c_send_frame(channel_handle, frames_list):
    global _zlg_dll
    global _usbcan_channel_handle_maps

    devtype, devidx, channel_number, _, _ = _usbcan_channel_handle_maps[str(channel_handle)]
    count = 0
    for frame in frames_list:
        o = _VCI_CAN_OBJ()
        o.ID = frame.id
        o.SendType = 0
        o.RemoteFlag = 0
        o.ExternFlag = 0
        o.DataLen = len(frame.data)
        if len(frame.data) < 8:
            frame.data.extern([0] * (8-len(frame.data)))
        elif len(frame.data) > 8:
            frame.data = frame.data[:8]
        else:
            pass
        o.Data = tuple(frame.data)
        status = _zlg_dll.VCI_Transmit(devtype, devidx, channel_number, POINTER(o), 1)
        if status == 1:
            count += 1

    return count


def c_close_channel(channel_handle):
    return c_clear_cache(channel_handle)


def c_reset_channel(channel_handle):
    global _zlg_dll
    global _usbcan_channel_handle_maps

    devtype, devidx, channel_number, _, _ = _usbcan_channel_handle_maps[str(channel_handle)]
    return True if 1 == _zlg_dll.VCI_ResetCAN(devtype, devidx, channel_number) else False
