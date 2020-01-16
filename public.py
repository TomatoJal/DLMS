import re
from array import array


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


def array_to_u32(a, big_endian=True):
    ret = 0
    if big_endian is True:
        for i in a:
            ret <<= 8
            ret += i
    else:
        for i in range(0, len(a)).__reversed__():
            ret <<= 8
            ret += a[i]
    return ret
