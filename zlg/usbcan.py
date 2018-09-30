# -*- coding: utf8 -*-
import api


class USBCAN(object):
    # 有错误
    STATUS_ERR = 0
    # 无错误
    STATUS_OK = 1
    # 设备在线
    STATUS_ONLINE = 2
    # 设备离线
    STATUS_OFFLINE = 3
    pass


class USBCAN_I_OR_I_PLUS(USBCAN):
    model = 'USBCAN-I/I+'
    model_type = 3
    nr_channel = 2


class USBCAN_II_OR_II_PLUS(USBCAN):
    model_name = 'USBCAN-II/II+'
    model_type = 4
    nr_channel = 2


class USBCAN_E_U(USBCAN):
    model_name = 'USBCAN-E-U'
    model_type = 20
    nr_channel = 2


class USBCAN_2E_U(USBCAN):
    model_name = 'USBCAN-2E-U/CANalyst-II+'
    model_type = 21
    nr_channel = 2


class USBCAN_4E_U(USBCAN):
    model_name = 'USBCAN-4E-U'
    model_type = 31
    nr_channel = 2


class USBCAN_8E_U(USBCAN):
    model_name = 'USBCAN-8E-U'
    model_type = 34
    nr_channel = 2


def get_supported_device_model_list():
    """
    获取支持的设备名称列表
    :return: class list
    """
    return USBCAN.__subclasses__()


def get_device_driver(model_name):
    """
    根据指定的型号名获取型号定义值
    :param model_name: string
    :return: usbcan class
    """
    for Cls in get_supported_device_model_list():
        if Cls.model_name != model_name:
            continue
        return Cls

    raise NotImplementedError("unsupported device", model_name)


class CANChannel:
    """CAN通道"""
    def __init__(self, device, ch_id):
        self.device = device
        self.driver = device.driver
        self.ch_id = ch_id

    def open(self):
        pass

    def close(self):
        pass

    def run_step_forward(self):
        pass


class CANDevice:
    """CAN设备"""
    def __init__(self, DeviceDriverClass, device_order_numer):
        # 设备驱动类
        self.device_driver = DeviceDriverClass

        # 设备号，编号从0开始，多个设备依次递增
        self.device_order_numer = device_order_numer

        # 设备离线标识
        self.device_offline = True

        # 设备已经打开的通道
        self.channel_list = [None for _ in range(self.device_driver.nr_channel)]

        # 设备句柄
        self.device_handle = -1

    def open(self):
        self.device_handle = api.open_device(self.device_driver.model_type, self.device_order_numer)

        if self.device_handle > 0:
            self.device_offline = False

    def close(self):
        if self.device_handle <= 0:
            return

        for channel in self.channel_list:
            if channel is None:
                continue
            channel.close()

        api.close_device(self.device_handle)

    def is_device_offline(self):
        status = api.is_device_online(self.device_handle)
        return True if status == USBCAN.STATUS_OFFLINE else False

    def run_step_forward(self):
        if self.device_offline is True:
            self.open()
            return

        # 每个循环都测试设备是否还在线，保证后续操作可以正常进行
        self.device_offline = self.is_device_offline()

        for channel in self.channel_list:
            if channel is None:
                continue
            channel.run_step_forward()


if __name__ == '__main__':
    device = CANDevice(USBCAN_II_OR_II_PLUS, 0)
    device.open()
    device.run_step_forward()
    device.run_step_forward()
    device.run_step_forward()
    device.run_step_forward()
    device.run_step_forward()
    device.run_step_forward()
    device.close()
