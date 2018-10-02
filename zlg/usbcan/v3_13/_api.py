# -*- coding: utf8 -*-
import os
from gateway import can
import handle
# 导入当前接口中的全部结构体
from ._types import _VCI_BOARD_INFO
from ._types import _VCI_INIT_CONFIG
from ._types import _VCI_CAN_OBJ
from ._products import *


# 动态库名称, 需要放在当前脚本目录
_zlg_dll_file_name = ''.join([os.path.dirname(__file__), '/driver/ControlCAN.dll'])

# dll 句柄，由windll.LoadLibrary返回
# 这里用cdll而不用windll的原因是函数声明方式不同
# 解释参见: https://blog.csdn.net/jiangxuchen/article/details/8741613
_zlg_dll = windll.LoadLibrary(_zlg_dll_file_name)


_token_name_can_device = "can device"
_token_name_can_channel = "can device channel"


class DeviceToken(handle.Token):
    def __init__(self, *args):
        super(self.__class__, self).__init__(_token_name_can_device, args)


class ChannelToken(handle.Token):
    def __init__(self, *args):
        super(self.__class__, self).__init__(_token_name_can_channel, args)


def c_open_device(devtype, devidx):
    global _zlg_dll

    # 避免重复打开设备
    token = DeviceToken(devtype, devidx)
    exsits_handle = handle.find(token)
    if exsits_handle is not None:
        return exsits_handle

    status = _zlg_dll.VCI_OpenDevice(devtype, devidx, 0)
    if status == 1:
        return handle.new(token)
    else:
        return 0


def is_device_online(device_handle):
    global _zlg_dll

    devtype, devidx = handle.get(device_handle)
    info = _VCI_BOARD_INFO()
    status = _zlg_dll.VCI_ReadBoardInfo(devtype, devidx, pointer(info))

    return True if status == 1 else False


def c_close_device(device_handle):
    global _zlg_dll

    # 关闭设备之前必须将关联的通道一并关闭, 做到资源主动回收
    channel_close_list = list()
    for ch, token in handle.all():
        if token.name != _token_name_can_channel:
            continue

        _, _, _, _, _, h, _, _ = token.payload()[0]
        if device_handle != h:
            continue

        channel_close_list.append(int(ch))

    for channel_handle in channel_close_list:
        handle.delete(channel_handle)

    devtype, devidx = handle.get(device_handle)
    handle.delete(device_handle)

    return True if 0 == _zlg_dll.VCI_CloseDevice(devtype, devidx) else False


def c_open_channel(device_handle, channel_number, bps, work_mode, acc_code, acc_mask):
    global _zlg_dll
    global _bps_table

    devtype, devidx = handle.get(device_handle)
    # 避免重复打开设备
    token = ChannelToken(devtype, devidx, channel_number, bps, work_mode, device_handle, acc_code, acc_mask)
    exsits_handle = handle.find(token)
    if exsits_handle is not None:
        return exsits_handle

    ic = _VCI_INIT_CONFIG()

    ic.Mode = work_mode
    #ic.AccCode, ic.AccMask = acc_code, acc_mask
    #ic.Filter = 0
    #ic.Timing0, ic.Timing1 = _bps_table[bps]

    bps_config_data = get_bps_config_data_by_handle(device_handle, bps)
    # VCI_SetReference 必须在VCI_InitCAN之前调用
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

    # 打开通道后先清空缓冲区
    _zlg_dll.VCI_ClearBuffer(devtype, devidx, channel_number)

    return handle.new(token)


def c_clear_cache(channel_handle):
    global _zlg_dll

    devtype, devidx, channel_number, _, _, _, _, _ = handle.get(channel_handle)
    return True if 0 == _zlg_dll.VCI_ClearBuffer(devtype, devidx, channel_number) else False


def c_get_cache_counter(channel_handle):
    global _zlg_dll

    devtype, devidx, channel_number, _, _, _, _, _ = handle.get(channel_handle)

    return _zlg_dll.VCI_GetReceiveNum(devtype, devidx, channel_number)


def c_get_frame(channel_handle, count, wait_ms):
    global _zlg_dll

    devtype, devidx, channel_number, _, _, _, _, _ = handle.get(channel_handle)

    CAN_OBJ_ARRY_TYPE = _VCI_CAN_OBJ * count
    buffer_list = CAN_OBJ_ARRY_TYPE()

    read_count = _zlg_dll.VCI_Receive(devtype, devidx, channel_number, pointer(buffer_list), count, wait_ms)
    if read_count in (0xffffffff, -1, 0):
        return list()

    return [can.CANFrame(id=obj.ID, tsp=obj.TimeStamp, data=obj.Data, size=obj.DataLen) for obj in buffer_list]


def c_send_frame(channel_handle, frames_list):
    global _zlg_dll

    devtype, devidx, channel_number, _, _, _, _, _ = handle.get(channel_handle)
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
    handle.delete(channel_handle)
    return True


def c_reset_channel(channel_handle):
    global _zlg_dll

    # 关闭原有句柄，重新打开新的句柄
    devtype, devidx, channel_number, bps, work_mode, device_handle, acc_code, acc_mask = handle.get(channel_handle)
    handle.delete(channel_handle)

    return c_open_channel(device_handle, channel_number, bps, work_mode, acc_code, acc_mask)
