# -*- coding: utf8 -*-
import os
from ctypes import *
import can
import zlg.can as zlg


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


def get_bps_config_data(device_handle, bps):
    global _usbcan_device_handle_maps
    global _bps_table

    devtype, devidx = _usbcan_device_handle_maps[str(device_handle)]
    driver = get_usbcan_driver_by_type(devtype)
    try:
        return driver.bps_map[bps]
    except Exception as e:
        return _bps_table[bps]


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
    del _usbcan_device_handle_maps[str(device_handle)]
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


def get_supported_model_list():
    return [Cls.model_name for Cls in zlg.USBCAN.__subclasses__()]


def get_usbcan_driver(model_name):
    for Cls in zlg.USBCAN.__subclasses__():
        if model_name == Cls.model_name:
            return Cls
    raise NotImplementedError("Unsurported device model", model_name)


def get_usbcan_driver_by_type(model_type):
    for Cls in zlg.USBCAN.__subclasses__():
        if model_type == Cls.model_type:
            return Cls
    raise NotImplementedError("Unsurported device type", model_type)


def c_open_channel(device_handle, channel_number, bps, work_mode, acc_code, acc_mask):
    global _zlg_dll
    global _handle_counter
    global _bps_table
    global _usbcan_device_handle_maps
    global _usbcan_channel_handle_maps

    devtype, devidx = _usbcan_device_handle_maps[str(device_handle)]

    ic = _VCI_INIT_CONFIG()

    ic.Mode = work_mode
    #ic.AccCode, ic.AccMask = acc_code, acc_mask
    #ic.Filter = 0
    #ic.Timing0, ic.Timing1 = _bps_table[bps]

    bps_config_data = get_bps_config_data(device_handle, bps)
    status = _zlg_dll.VCI_SetReference(devtype, devidx, channel_number, 0, pointer(bps_config_data))
    if status != 1:
        print("set bps to", bps, "failed!")
        return 0
    else:
        print("set bps to", bps, "successed!")

    status = _zlg_dll.VCI_InitCAN(devtype, devidx, channel_number, pointer(ic))
    if status != 1:
        print("configure failed, dev, dev-idx, channel-idx", devtype, devidx, acc_mask)
        return 0

    status = _zlg_dll.VCI_StartCAN(devtype, devidx, channel_number)
    if status != 1:
        print("start channel", channel_number, "failed!")
        return 0
    else:
        print("start channel", channel_number, "successed!")

    # reset CAN for the first.
    #_zlg_dll.VCI_ResetCAN(devtype, devidx, channel_number)

    channel, _handle_counter = _handle_counter, _handle_counter + 1
    _usbcan_channel_handle_maps[str(channel)] = (devtype, devidx, channel_number, bps, work_mode)
    return channel


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
                ('TimeFlag', c_uint8),
                ('SendType', c_uint8),
                ('RemoteFlag', c_uint8),
                ('ExternFlag', c_uint8),
                ('DataLen', c_uint8),
                ('Data', c_uint8 * 8),
                ('Reserved', c_uint8 * 3)]


def c_get_frame(channel_handle, count, wait_ms):
    global _zlg_dll
    global _usbcan_channel_handle_maps

    devtype, devidx, channel_number, _, _ = _usbcan_channel_handle_maps[str(channel_handle)]

    CAN_OBJ_ARRY_TYPE = _VCI_CAN_OBJ * count
    buffer_list = CAN_OBJ_ARRY_TYPE()

    read_count = _zlg_dll.VCI_Receive(devtype, devidx, channel_number, pointer(buffer_list), count, wait_ms)
    if read_count in (0xffffffff, -1, 0):
        return list()

    return [can.CANFrame(id=obj.ID, tsp=obj.TimeStamp, data=obj.Data) for obj in buffer_list]


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
            frame.data.extend([0] * (8-len(frame.data)))
        elif len(frame.data) > 8:
            frame.data = frame.data[:8]
        else:
            pass
        o.Data = tuple(frame.data)
        status = _zlg_dll.VCI_Transmit(devtype, devidx, channel_number, pointer(o), 1)
        if status == 1:
            count += 1

    return count


def c_close_channel(channel_handle):
    global _usbcan_channel_handle_maps
    del _usbcan_channel_handle_maps[str(channel_handle)]
    return c_clear_cache(channel_handle)


def c_reset_channel(channel_handle):
    global _zlg_dll
    global _usbcan_channel_handle_maps

    devtype, devidx, channel_number, _, _ = _usbcan_channel_handle_maps[str(channel_handle)]
    return True if 1 == _zlg_dll.VCI_ResetCAN(devtype, devidx, channel_number) else False


if __name__ == '__main__':
    from ctypes import *

    class _VCI_INIT_CONFIG(Structure):
        _fields_ = [('AccCode', c_ulong),
                    ('AccMask', c_ulong),
                    ('Reserved', c_ulong),
                    ('Filter', c_ubyte),
                    ('Timing0', c_ubyte),
                    ('Timing1', c_ubyte),
                    ('Mode', c_ubyte)]


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


    vic = _VCI_INIT_CONFIG()
    vic.AccCode = 0x00000000
    vic.AccMask = 0xffffffff
    vic.Filter = 0
    vic.Timing0 = 0x00
    vic.Timing1 = 0x1c
    vic.Mode = 0

    vco = _VCI_CAN_OBJ()
    vco.ID = 0x00000001
    vco.SendType = 0
    vco.RemoteFlag = 0
    vco.ExternFlag = 0
    vco.DataLen = 8
    vco.Data = (1, 2, 3, 4, 5, 6, 7, 8)

    canLib = windll.LoadLibrary('driver/v3.13/ControlCAN.dll')
    print('打开设备: %d' % (canLib.VCI_OpenDevice(21, 0, 0)))
    print('设置波特率: %d' % (canLib.VCI_SetReference(21, 0, 0, 0, pointer(c_int(0x060003)))))
    print('初始化: %d' % (canLib.VCI_InitCAN(21, 0, 0, pointer(vic))))
    print('启动: %d' % (canLib.VCI_StartCAN(21, 0, 0)))
    print('清空缓冲区: %d' % (canLib.VCI_ClearBuffer(21, 0, 0)))
    print('发送: %d' % (canLib.VCI_Transmit(21, 0, 0, pointer(vco), 1)))
