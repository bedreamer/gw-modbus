# -*- coding: utf8 -*-

from ctypes import *


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


# CAN配置结构体
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
                ('TimeFlag', c_uint8),
                ('SendType', c_uint8),
                ('RemoteFlag', c_uint8),
                ('ExternFlag', c_uint8),
                ('DataLen', c_uint8),
                ('Data', c_uint8 * 8),
                ('Reserved', c_uint8 * 3)]
