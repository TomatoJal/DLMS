from array import array
from collections import namedtuple
import re


def trans_to_array(frame):
    """转换'xx xx xx xx'字符串为array('B')"""
    if ' ' in frame:
        frame = frame.split(' ')
    else:
        frame = re.findall(r'.{2}', frame)
    return array('B', [int(b, 16) for b in frame])


def u8_to_hex(u8, header=None):
    """
    将一字节数转换为十六进制字符串
    :param u8: 一字节数
    :param header: 需要添加的头,默认不需要
    :return: u8在合法范围内返回十六进制字符串
    """
    if u8 > 255 or u8 < 0:
        return None
    if header is not None:
        return header + hex(u8)[2:].rjust(2, '0')
    return hex(u8)[2:].rjust(2, '0')


class DLMSBaseType:
    # 建立value, info机制,检查时若info为None则认为这一帧错误
    element_namedtuple = namedtuple('element', 'value info', defaults=[None])

    def __init__(self, frame):
        if isinstance(frame, str) is True:
            frame = trans_to_array(frame)
        self.frame = array('B', frame)
        self.element = dict()

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
        return new_obj

    def __len__(self):
        return len(self.frame)

    def __repr__(self):
        output = self.__class__.__name__ + '({})'.format(list(self.frame))
        return output

    def get_frame_string(self, space=False):
        """打印frame"""
        output = ''
        for i in self.frame:
            output += hex(int(i))[2:].rjust(2, '0')
            if space is True:
                output += ' '
        return output

    @property
    def get_info(self):
        """获取该DLMS结构信息"""
        for key in self.element.keys():
            if self.element[key].info is None:
                return f'Wrong {key}'
        return self.element

    def _set_info(self, m, info):
        self.element[m] = self.element[m]._replace(info=info)

    def _set_value(self, m, value):
        self.element[m] = self.element[m]._replace(value=value)


if __name__ == '__main__':
    print(u8_to_hex(100, header='0x'))
