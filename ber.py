# -*- coding: UTF-8 -*-
import math
from collections import namedtuple
from public import *

"""
cls - tag type
        -- 0b00000000 Universal tag
        -- 0b01000000 Application
        -- 0b10000000 context-specific
        -- 0b11000000 Private
pc  - 0b00000000 PRIMITIVE
    - 0b00100000 CONSTRUCTED
tag
"""
BER = namedtuple('BER', 'rep cls pc tag len value frame')

BER_TAG_TYPE_UNIVERSAL, BER_TAG_TYPE_APPLICATION, BER_TAG_TYPE_CONTEXT_SPECIFIC, BER_TAG_TYPE_PRIVATE = \
            0b00000000,               0b01000000,                    0b10000000,           0b11000000

PRIMITIVE = 0b00000000       # 原始数据类型
CONSTRUCTED = 0b00100000     # 构造数据类型

"""UNIVERSAL tag"""
BER_TYPE_BOOLEAN = 0x01
BER_TYPE_INTEGER = 0x02
BER_TYPE_BIT_STRING = 0x03
BER_TYPE_OCTET_STRING = 0x04
BER_TYPE_NULL = 0x05
BER_TYPE_OID = 0x06
BER_TYPE_SEQUENCE = 0x30
BER_TYPE_COUNTER = 0x41
BER_TYPE_GAUGE = 0x42
BER_TYPE_TIME_TICKS = 0x43
BER_TYPE_NO_SUCH_OBJECT = 0x80
BER_TYPE_NO_SUCH_INSTANCE = 0x81
BER_TYPE_END_OF_MIB_VIEW = 0x82
BER_TYPE_SNMP_GET = 0xA0
BER_TYPE_SNMP_GETNEXT = 0xA1
BER_TYPE_SNMP_RESPONSE = 0xA2
BER_TYPE_SNMP_SET = 0xA3
BER_TYPE_SNMP_GETBULK = 0xA5
BER_TYPE_SNMP_INFORM = 0xA6
BER_TYPE_SNMP_TRAP = 0xA7
BER_TYPE_SNMP_REPORT = 0xA8


def ber_decode(message, result=None):
    """ Decode a message from ASN1-BER (TLV) bytes into a list of byte values.
    Values that contain embedded types will need to call this function to
    break the objects into their individual type/value components. """
    # 用于迭代
    if not result:
        result = []

    # Use masks to isolate the binary parts
    ber_type = message[0]
    ber_cls = ber_type & 0b11000000
    ber_pc = ber_type & 0b00100000
    ber_tag = ber_type & 0b00011111
    # 若tag >= 31, 第一个字节后5bit都为1, 其tag 为后续直到bit 7 为0(最后一个)的0~6 bit相接
    offset = 1
    if ber_tag == 31:
        ber_tag = (message[offset] & 0b01111111)
        while message[offset] & 0b10000000 != 0:
            offset += 1
            ber_tag <<= 8
            ber_tag += (message[offset] & 0b01111111)
        offset += 1
    ber_len = message[offset]
    offset += 1
    # Assume that the ber_value is offset 2 or is blank
    # first + tag
    if ber_len > 0x80:
        offset += (ber_len & 0x7F)
        ber_len = asn_length_decoder(message[1: 1+ber_len-0x80+1])
        # 检查是否是正确的ber_len
        if ber_len is None:
            return None
    # 长度大于实际剩余主数据长度
    if ber_len > len(message)-offset:
        return None

    ber_value = message[offset: offset + ber_len]
    ber_frame = array('B', [ber_cls+ber_pc+ber_tag, ber_len]) + ber_value
    result.append(BER(ber_cls+ber_pc+ber_tag, ber_cls, ber_pc, ber_tag, ber_len, ber_value, ber_frame))
    message = message[ber_len + offset:]
    # If the message had only one type then we are done, if not recurse.
    if len(message) == 0:
        return result
    else:
        return ber_decode(message, result)


def asn_length_encoder(length):
    """
    长度转换为asn码
    :param length: 输入长度，int
    :return:
    """
    length = int(length)
    output = ''

    if length <= 128:
        output += to_hex(length)
    else:
        header = 0x81 + int(math.log(length, 256))
        output += to_hex(header)
        output += to_hex(length)
    return to_hex(output)


def asn_length_decoder(length):
    """
    asn码转换为int
    :param length: 输入长度，str
    :return:   输出长度，int
    """
    header = length[0]

    # if header > 0x8F:
    #     return None
    #     raise ValueError('The length is too bigger than 0x8F')

    """输入length的字节长度错误"""
    if header > 0x80 and len(length) - 1 != header - 0x80:
        return None

    if header <= 128:
        output = header
    else:
        header -= 0x80
        output = int(length.to_hex_str[2:], 16)
    return output

