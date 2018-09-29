# -*- coding: utf8 -*-
import struct


class DataModel(object):
    """MODBUS数据模型"""
    def __init__(self, name, address, formatter, model_name, object_type, access_right, comment=None):
        self.name, self.address, self.formatter = name, address, formatter
        self.model_name = model_name
        self.object_type = object_type
        self.access_right = access_right
        self.comment = comment


class DataModelDescretesInput(DataModel):
    """开入量"""
    def __init__(self, name, address, formatter):
        super(self.__class__, self).__init__(name, address, formatter, 'Descretes Input', 'single bit', ['r'])


class DataModelCoils(DataModel):
    """开出量"""
    def __init__(self, name, address, formatter):
        super(self.__class__, self).__init__(name, address, formatter, 'Coils', 'single bit', ['r', 'w'])


class DataModelInputRegisters(DataModel):
    """输入寄存器"""
    def __init__(self, name, address, formatter):
        super(self.__class__, self).__init__(name, address, formatter, 'InputRegisters', '16-bit word', ['r'])


class DataModelHoldingRegisters(DataModel):
    """输出寄存器"""
    def __init__(self, name, address, formatter):
        super(self.__class__, self).__init__(name, address, formatter, 'HoldingRegisters', '16-bit word', ['r', 'w'])


###############################################################################################


class DataAccessFunction(object):
    def __init__(self, name, access_mode, code, datamode):
        self.name = name
        self.access_mode = access_mode
        self.code = code
        self.supported_datamode_list = datamode

    def __make_pdu(self, data_as_byte_list):
        pdu = [self.code]
        pdu.extend(data_as_byte_list)
        return pdu


class BitDataAccessFunction(DataAccessFunction):
    def __init__(self, name, code, datamode):
        super(self.__class__, self).__init__(name, 'Bit access', code, datamode)


class WordDataAccessFunction(DataAccessFunction):
    def __init__(self, name, code, datamode):
        super(self.__class__, self).__init__(name, '16bits access', code, datamode)


class X01_Function(WordDataAccessFunction):
    def __init__(self):
        super(self.__class__, self).__init__("Read Coils", 0x01, [DataModelCoils])

    def make_pdu(self, starting_address, quantity_of_coils):
        """
        
        :param starting_address: 2 bytes, 0x0000 to 0xffff
        :param quantity_of_coils: 2 bytes, 1 to 2000(0x7d0)
        :return: 
        """
        data_as_byte_list = [(starting_address >> 8) & 0xff, starting_address & 0xff,
                             (quantity_of_coils >> 8) & 0xff, quantity_of_coils & 0xff]
        return self.__make_pdu(data_as_byte_list)


class X02_Function(WordDataAccessFunction):
    def __init__(self):
        super(self.__class__, self).__init__("Read Discrete Inputs", 0x02, [DataModelDescretesInput])

    def make_pdu(self, starting_address, quantity_of_inputs):
        """
        
        :param starting_address: 2 bytes, 0x0000 to 0xffff
        :param quantity_of_inputs: 2bytes, 1 to 2000(0x7d0)
        :return: 
        """
        data_as_byte_list = [(starting_address >> 8) & 0xff, starting_address & 0xff,
                             (quantity_of_inputs >> 8) & 0xff, quantity_of_inputs & 0xff]
        return self.__make_pdu(data_as_byte_list)


class X03_Function(WordDataAccessFunction):
    def __init__(self):
        super(self.__class__, self).__init__("Read Holding Registers", 0x03, [DataModelHoldingRegisters])

    def make_pdu(self, starting_address, quantity_of_registers):
        """
        
        :param starting_address: 2 bytes, 0x0000 to 0xffff
        :param quantity_of_registers: 2bytes, 1 to 125(0x7d)
        :return: 
        """
        data_as_byte_list = [(starting_address >> 8) & 0xff, starting_address & 0xff,
                             0, quantity_of_registers & 0x7f]
        return self.__make_pdu(data_as_byte_list)


class X04_Function(WordDataAccessFunction):
    def __init__(self):
        super(self.__class__, self).__init__("Read Input Registers", 0x04, [DataModelInputRegisters])

    def make_pdu(self, starting_address, quantity_of_input_registers):
        """
        
        :param starting_address: 2 bytes, 0x0000 to 0xffff
        :param quantity_of_input_registers: 2 bytes, 1 to 125(0x7d)
        :return: 
        """
        data_as_byte_list = [(starting_address >> 8) & 0xff, starting_address & 0xff,
                             0, quantity_of_input_registers & 0x7f]
        return self.__make_pdu(data_as_byte_list)


class X05_Function(WordDataAccessFunction):
    def __init__(self):
        super(self.__class__, self).__init__("Write Single Coil", 0x05, [DataModelInputRegisters])

    def make_pdu(self, output_address, output_value):
        """
        
        :param output_address: 2 bytes, 0x0000 to 0xffff
        :param output_value: 2 bytes, 0x0000 or 0xff00
        :return: 
        """
        data_as_byte_list = [(output_address >> 8) & 0xff, output_address & 0xff,
                             (output_value >> 8) & 0xff, 0]
        return self.__make_pdu(data_as_byte_list)


class X06_Function(WordDataAccessFunction):
    def __init__(self):
        super(self.__class__, self).__init__("Write Single Register", 0x06, [DataModelHoldingRegisters, DataModelCoils])

    def make_pdu(self, register_address, register_value):
        """
        
        :param register_address: 2 bytes, 0x0000 to 0xffff
        :param register_value: 2 bytes, 0x0000 to 0xffff
        :return: 
        """
        data_as_byte_list = [(register_address >> 8) & 0xff, register_address & 0xff,
                             (register_value >> 8) & 0xff, register_value & 0xff]
        return self.__make_pdu(data_as_byte_list)


class Server(object):
    def __init__(self, address, mdf):
        """
        MODBUS服务器
        :param address: 服务器地址
        :param mdf: modbus device descrip file
        """
        self.address = address
        self.mdf = mdf


if __name__ == '__main__':
    dev = Server(address=1, mdf="example/NH-100.json")
