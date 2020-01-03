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


def to_hex(u, header=''):
    """

    :param u:
    :param header:
    :return:
    """
    u = int(u)
    body = hex(u)[2:]
    output = body.rjust(len(body) + len(body) % 2, '0')
    output = re.findall(r'.{2}', output)

    output = [header + i.upper() for i in output]
    return ''.join(output)


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

    def _set_info(self, m, info):
        self.element[m] = self.element[m]._replace(info=info)

    def _set_value(self, m, value):
        self.element[m] = self.element[m]._replace(value=value)


if __name__ == '__main__':
    print(to_hex(10, header='0x'))
