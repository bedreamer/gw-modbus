# -*- coding: utf8 -*-


class USBCAN(object):
    pass


class USBCAN_I_OR_I_PLUS(USBCAN):
    model = 'USBCAN-I/I+'
    model_type = 3
    max_channel = 2


class USBCAN_II_OR_II_PLUS(USBCAN):
    model_name = 'USBCAN-II/II+'
    model_type = 4
    max_channel = 2


class USBCAN_E_U(USBCAN):
    model_name = 'USBCAN-E-U'
    model_type = 20
    max_channel = 2


class USBCAN_2E_U(USBCAN):
    model_name = 'USBCAN-2E-U/CANalyst-II+'
    model_type = 21
    max_channel = 2


class USBCAN_4E_U(USBCAN):
    model_name = 'USBCAN-4E-U'
    model_type = 31
    max_channel = 2


class USBCAN_8E_U(USBCAN):
    model_name = 'USBCAN-8E-U'
    model_type = 34
    max_channel = 2


def get_supported_device_model_list():
    """
    获取支持的设备名称列表
    :return: class list
    """
    return USBCAN.__subclasses__()


def get_device_model_type(model_name):
    """
    根据指定的型号名获取型号定义值
    :param model_name: string
    :return: int
    """
    for Cls in USBCAN.__subclasses__():
        if Cls.model_name != model_name:
            continue

        return Cls.model_type

    raise NotImplementedError("unsupported device", model_name)