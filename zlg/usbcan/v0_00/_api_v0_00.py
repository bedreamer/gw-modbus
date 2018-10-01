# -*- coding: utf8 -*-
from ctypes import *
import os

# 动态库名称, 需要放在当前脚本目录
_zlg_dll_file_name = ''.join([os.path.dirname(__file__), 'driver/v0.00/zlgcan.dll'])

# dll 句柄，由windll.LoadLibrary返回
# 这里用cdll而不用windll的原因是函数声明方式不同
# 解释参见: https://blog.csdn.net/jiangxuchen/article/details/8741613
_zlg_dll = windll.LoadLibrary(_zlg_dll_file_name)

