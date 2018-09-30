# -*- coding: utf8 -*-
from ctypes import *

# 动态库名称, 需要放在当前脚本目录
_zlg_dll_file_name = 'v0.00/zlgcan.dll'

# dll 句柄，由windll.LoadLibrary返回
# 这里用cdll而不用windll的原因是函数声明方式不同
# 解释参见: https://blog.csdn.net/jiangxuchen/article/details/8741613
_zlg_dll = windll.LoadLibrary(_zlg_dll_file_name)


# for zlgcan.dll
# 打开设备
c_open_device = _zlg_dll.ZCAN_OpenDevice
# 测试设备是否在线
c_is_device_online = _zlg_dll.ZCAN_IsDeviceOnLine

# 初始化某个通道
c_init_can = _zlg_dll.ZCAN_InitCAN
c_get_I_property = _zlg_dll.GetIProperty
c_release_I_property = _zlg_dll.ReleaseIProperty

c_get_device_info = _zlg_dll.ZCAN_GetDeviceInf
c_clear_buffer = _zlg_dll.ZCAN_ClearBuffer
c_read_channel_error_info = _zlg_dll.ZCAN_ReadChannelErrInfo
c_read_channel_status = _zlg_dll.ZCAN_ReadChannelStatus

# 启动已经初始化后的通道
c_start_can = _zlg_dll.ZCAN_StartCAN
c_get_recv_num = _zlg_dll.ZCAN_GetReceiveNum
c_transmit = _zlg_dll.ZCAN_Transmit
c_receive = _zlg_dll.ZCAN_Receive
c_transmitFD = _zlg_dll.ZCAN_TransmitFD
c_receiveFD = _zlg_dll.ZCAN_ReceiveFD
# 复位已经初始化的通道，若要再次使用，需要调用_zlg_start_can
c_reset_can = _zlg_dll.ZCAN_ResetCAN


# 关闭已经打开的设备
c_close_device = _zlg_dll.ZCAN_CloseDevice


# 设备配置结构体
class ZCAN_CHANNEL_INIT_CONFIG(Structure):
    _fields_ = [
        ('can_type', c_uint32),
        ('acc_code', c_uint32),
        ('acc_mask', c_uint32),
        ('reserved', c_uint32),
        ('filter', c_ubyte),
        ('timing0', c_ubyte),
        ('timing1', c_ubyte),
        ('mode', c_ubyte)
    ]
