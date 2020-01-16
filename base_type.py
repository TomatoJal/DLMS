from collections import namedtuple
from public import *
from ber import *


class DLMSBaseType:
    # 建立value, info机制,检查时若info为None则认为这一帧错误
    element_namedtuple = namedtuple('element', 'value info', defaults=[None])

    def __init__(self, frame):
        if isinstance(frame, str) is True:
            frame = trans_to_array(frame)
        self.frame = array('B', frame)
        self.element = dict()
        # 帧类型
        self.frame_type = None

    def __getitem__(self, index):
        """实现序列协议"""
        return self.frame[index]

    def __add__(self, other):
        """实现帧拼接"""
        if other.frame is None:
            if self.frame is not None:
                return DLMSBaseType(self.frame)
        new_obj = DLMSBaseType(self.frame + other.frame)
        new_obj.element = self.element
        for key in other.element.keys():
            if key not in self.element.keys():
                new_obj.element[key] = other.element[key]
        if self.frame_type is not None:
            new_obj.frame_type = self.frame_type
        elif other.frame_type is not None:
            new_obj.frame_type = other.frame_type
        return new_obj

    def __len__(self):
        return len(self.frame)

    def __repr__(self):
        output = self.__class__.__name__ + '({})'.format(list(self.frame))
        return output

    def get_frame_string(self, space=True):
        """打印frame"""
        output = ''
        for i in self.frame:
            output += hex(int(i))[2:].rjust(2, '0')
            if space is True:
                output += ' '
        return output.upper()

    @property
    def get_info(self):
        """获取该DLMS结构信息"""
        for key in self.element.keys():
            if self.element[key].info is None:
                return f'Wrong {key}'
        return self.element

    def set_info(self, m, info):
        self.element[m] = self.element[m]._replace(info=info)

    def set_value(self, m, value):
        self.element[m] = self.element[m]._replace(value=value)


class BerBoolean(DLMSBaseType):
    def __init__(self, frame, obj='Boolean'):
        super(BerBoolean, self).__init__(frame)
        self.element[obj] = DLMSBaseType.element_namedtuple(self.frame, None)
        if self.frame[0] == BER_TYPE_BOOLEAN and \
           len(self.frame) == 2 and (self.frame[1] == 0 or self.frame[1] == 1):
            self.set_info(obj, obj + ': ' + to_hex(self.frame[1]))


class BerInteger(DLMSBaseType):
    def __init__(self, frame, obj='Boolean'):
        super(BerInteger, self).__init__(frame)
        self.element[obj] = DLMSBaseType.element_namedtuple(self.frame, None)
        if self.frame[0] == BER_TYPE_INTEGER and \
           len(self.frame) == 2:
            self.set_info(obj, obj + ': ' + to_hex(self.frame[1]))


class BerOctetString(DLMSBaseType):
    def __init__(self, frame, obj='OctetString'):
        super(BerOctetString, self).__init__(frame)
        self.element[obj] = DLMSBaseType.element_namedtuple(self.frame, None)
        # 长度处理要改为ASN
        if self.frame[0] == BER_TYPE_OCTET_STRING and \
           self.frame[1] == len(self.frame) - 2:
            self.set_info(obj, obj + ': ' + ''.join([to_hex(i) for i in self.frame]))
