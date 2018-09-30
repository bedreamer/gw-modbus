# -*- coding: utf8 -*-
from ctypes import *
import usbcan


# 动态库名称, 需要放在当前脚本目录
_zlg_dll_file_name = 'zlgcan.dll'

# dll 句柄，由windll.LoadLibrary返回
_zlg_dll = windll.LoadLibrary(_zlg_dll_file_name)


# 打开设备
c_open_device = _zlg_dll.ZCAN_OpenDevice
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
# 复位已经初始化的通道，若要再次使用，需要调用_zlg_start_can
c_reset_can = _zlg_dll.ZCAN_ResetCAN

c_get_recv_num = _zlg_dll.ZCAN_GetReceiveNum
c_transmit = _zlg_dll.ZCAN_Transmit
c_receive = _zlg_dll.ZCAN_Receive
c_transmitFD = _zlg_dll.ZCAN_TransmitFD
c_receiveFD = _zlg_dll.ZCAN_ReceiveFD

# 关闭已经打开的设备
c_close_device = _zlg_dll.ZCAN_CloseDevice





