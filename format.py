# -*- coding: utf8 -*-


class DataModelFormat(object):
    def encode(self, python_value):
        """
            将python值编码成MODBUS格式, 返回 modbus bytes list
        """
        raise NotImplementedError

    def decode(self, modbus_bytes_list):
        """        
            将MODBUS格式解码为python值， 返回int, float
        """
        raise NotImplementedError


class DataModel_U16(DataModelFormat):
    name = 'U16'
    def encode(self, python_value):
        """
            将python值编码成MODBUS格式, 返回 modbus bytes list
        """
        word = abs(python_value)
        return [(word >> 8) & 0xff, word & 0xff]


    def decode(self, modbus_bytes_list):
        """        
            将MODBUS格式解码为python值， 返回int, float
        """
        hi, lo = modbus_bytes_list
        word = hi * 256 + lo
        return int(word)


class DataModel_U16x10(DataModelFormat):
    name = 'U16x10'
    def encode(self, python_value):
        """
            将python值编码成MODBUS格式, 返回 modbus bytes list
        """
        word = abs(python_value) * 10
        return [(word >> 8) & 0xff, word & 0xff]

    def decode(self, modbus_bytes_list):
        """        
            将MODBUS格式解码为python值， 返回int, float
        """
        hi, lo = modbus_bytes_list
        word = hi * 256 + lo
        return float(word) / 10.0


class DataModel_U16x100(DataModelFormat):
    name = 'U16x100'
    def encode(self, python_value):
        """
            将python值编码成MODBUS格式, 返回 modbus bytes list
        """
        word = abs(python_value) * 100
        return [(word >> 8) & 0xff, word & 0xff]

    def decode(self, modbus_bytes_list):
        """        
            将MODBUS格式解码为python值， 返回int, float
        """
        hi, lo = modbus_bytes_list
        word = hi * 256 + lo
        return float(word) / 100.0


class DataModel_U16x1K(DataModelFormat):
    name = 'U16x1000'
    def encode(self, python_value):
        """
            将python值编码成MODBUS格式, 返回 modbus bytes list
        """
        word = abs(python_value) * 1000
        return [(word >> 8) & 0xff, word & 0xff]

    def decode(self, modbus_bytes_list):
        """        
            将MODBUS格式解码为python值， 返回int, float
        """
        hi, lo = modbus_bytes_list
        word = hi * 256 + lo
        return float(word) / 1000.0


class DataModel_U16x10K(DataModelFormat):
    name = 'U16x10000'
    def encode(self, python_value):
        """
            将python值编码成MODBUS格式, 返回 modbus bytes list
        """
        word = abs(python_value) * 10000
        return [(word >> 8) & 0xff, word & 0xff]

    def decode(self, modbus_bytes_list):
        """        
            将MODBUS格式解码为python值， 返回int, float
        """
        hi, lo = modbus_bytes_list
        word = hi * 256 + lo
        return float(word) / 10000.0


class DataModel_S16(DataModelFormat):
    def encode(self, python_value):
        """
            将python值编码成MODBUS格式, 返回 modbus bytes list
        """
        raise NotImplementedError

    def decode(self, modbus_bytes_list):
        """        
            将MODBUS格式解码为python值， 返回int, float
        """
        raise NotImplementedError


class DataModel_S16x10(DataModelFormat):
    def encode(self, python_value):
        """
            将python值编码成MODBUS格式, 返回 modbus bytes list
        """
        word = abs(python_value) * 10
        return [(word >> 8) & 0xff, word & 0xff]

    def decode(self, modbus_bytes_list):
        """        
            将MODBUS格式解码为python值， 返回int, float
        """
        hi, lo = modbus_bytes_list
        word = hi * 256 + lo
        return float(word) / 10.0


class DataModel_S16x100(DataModelFormat):
    def encode(self, python_value):
        """
            将python值编码成MODBUS格式, 返回 modbus bytes list
        """
        word = abs(python_value) * 100
        return [(word >> 8) & 0xff, word & 0xff]

    def decode(self, modbus_bytes_list):
        """        
            将MODBUS格式解码为python值， 返回int, float
        """
        hi, lo = modbus_bytes_list
        word = hi * 256 + lo
        return float(word) / 100.0


class DataModel_S16x1K(DataModelFormat):
    def encode(self, python_value):
        """
            将python值编码成MODBUS格式, 返回 modbus bytes list
        """
        word = abs(python_value) * 1000
        return [(word >> 8) & 0xff, word & 0xff]

    def decode(self, modbus_bytes_list):
        """        
            将MODBUS格式解码为python值， 返回int, float
        """
        hi, lo = modbus_bytes_list
        word = hi * 256 + lo
        return float(word) / 1000.0


class DataModel_S16x10K(DataModelFormat):
    def encode(self, python_value):
        """
            将python值编码成MODBUS格式, 返回 modbus bytes list
        """
        word = abs(python_value) * 10000
        return [(word >> 8) & 0xff, word & 0xff]

    def decode(self, modbus_bytes_list):
        """        
            将MODBUS格式解码为python值， 返回int, float
        """
        hi, lo = modbus_bytes_list
        word = hi * 256 + lo
        return float(word) / 10000.0
