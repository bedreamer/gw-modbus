# -*- coding: utf8 -*-


class CANDriver(object):
    pass


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
        self.device_handle = ucanapi.open_device(self.device_driver.model_type, self.device_order_numer)

        if self.device_handle > 0:
            self.device_offline = False

    def close(self):
        if self.device_handle <= 0:
            return

        for channel in self.channel_list:
            if channel is None:
                continue
            channel.close()

        ucanapi.close_device(self.device_handle)

    def is_device_offline(self):
        status = ucanapi.is_device_online(self.device_handle)
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