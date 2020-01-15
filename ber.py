# -*- coding: UTF-8 -*-
import math
from collections import namedtuple
from base_type import DLMSBaseType
from channel.hdlc import IInfo
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
BER = namedtuple('BER', 'rep cls pc tag len value')

BER_TAG_TYPE_UNIVERSAL, BER_TAG_TYPE_APPLICATION, BER_TAG_TYPE_CONTEXT_SPECIFIC, BER_TAG_TYPE_PRIVATE = \
            0b00000000,               0b01000000,                    0b10000000,           0b11000000

PRIMITIVE = 0b00000000       # 原始数据类型
CONSTRUCTED = 0b00100000     # 构造数据类型

"""UNIVERSAL tag"""
"""

#define BER_TYPE_BOOLEAN				0x01
#define BER_TYPE_INTEGER				0x02
#define BER_TYPE_BIT_STRING				0x03
#define BER_TYPE_OCTET_STRING				0x04
#define BER_TYPE_NULL					0x05
#define BER_TYPE_OID					0x06
#define BER_TYPE_SEQUENCE				0x30
#define BER_TYPE_COUNTER				0x41
#define BER_TYPE_GAUGE					0x42
#define BER_TYPE_TIME_TICKS				0x43
#define BER_TYPE_NO_SUCH_OBJECT				0x80
#define BER_TYPE_NO_SUCH_INSTANCE			0x81
#define BER_TYPE_END_OF_MIB_VIEW			0x82
#define BER_TYPE_SNMP_GET				0xA0
#define BER_TYPE_SNMP_GETNEXT				0xA1
#define BER_TYPE_SNMP_RESPONSE				0xA2
#define BER_TYPE_SNMP_SET				0xA3
#define BER_TYPE_SNMP_GETBULK				0xA5
#define BER_TYPE_SNMP_INFORM				0xA6
#define BER_TYPE_SNMP_TRAP				0xA7
#define BER_TYPE_SNMP_REPORT				0xA8
————————————————
版权声明：本文为CSDN博主「聪明的狐狸」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/smartfox80/article/details/18899707
"""
BER_TYPE_REVERSE0, BER_TYPE_BOOLEAN, BER_TYPE_INTEGER, BER_TYPE_BIT_STRING, BER_TYPE_OCTET_STRING, BER_TYPE_NULL = \
                0,                1,                3,                   4,                     5,             6
"""------------------------------------------------------------------------------------------------------------------"""
BER_TYPE_OBJECT_IDENTIFIER, BER_TYPE_OBJECT_DESCRIPTION, BER_TYPE_EXTERNAL, BER_TYPE_INSTANCE_OF, BER_TYPE_REAL = \
                         7,                           8,                 9,                    9,            10
"""------------------------------------------------------------------------------------------------------------------"""
BER_TYPE_ENUMERATED, BER_TYPE_EMBEDDED_PDV, BER_TYPE_UFT8_STRING, BER_TYPE_RELATIVE_OID, BER_TYPE_REVERSE15 = \
                 11,                    12,                   13,                    14,                 15
"""------------------------------------------------------------------------------------------------------------------"""
BER_TYPE_REVERSE16, BER_TYPE_SEQUENCE, SEQUENCE_OF, BER_TYPE_SET, BER_TYPE_SET_OF = \
                16,                17,          17,           18,              18
"""------------------------------------------------------------------------------------------------------------------"""
BER_TYPE_NUMERIC_STRING, BER_TYPE_PRINTABLE_STRING, BER_TYPE_TELETEX_STRING, BER_TYPE_T61_STRING = \
                     19,                        20,                      21,                  21
"""------------------------------------------------------------------------------------------------------------------"""
BER_TYPE_VIDEOTEX_STRING, BER_TYPE_IA5_STRING, BER_TYPE_UTCTIME, BER_TYPE_GENERALIZED_TIME, BER_TYPE_GRAPHIC_STRING = \
                      22,                  23,               24,                        25,                      26
"""------------------------------------------------------------------------------------------------------------------"""
BER_TYPE_VISIBLE_STRING, BER_TYPE_ISO646_STRING, BER_TYPE_GENERAL_STRING, BER_TYPE_UNIVERSAL_STRING = \
                     27,                     27,                      28,                        29
"""------------------------------------------------------------------------------------------------------------------"""
BER_TYPE_CHARACTER_STRING, BER_TYPE_REVERSE31 = \
                       30,                 31
"""------------------------------------------------------------------------------------------------------------------"""


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

    # Assume that the ber_value is offset 2 or is blank
    # first + tag
    offset += 1
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
    result.append(BER(ber_cls+ber_pc+ber_tag, ber_cls, ber_pc, ber_tag, ber_len, DLMSBaseType(ber_value)))
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


if __name__ == '__main__':
    test = IInfo('E6 E6 00 60 29 A1 09 06 07 60 85 74 05 08 01 01 A6 0A 04 08 00 00 00 00 00 00 98 00 BE 10 04 0E 01 00 00 00 06 5F 1F 04 00 00 1F 3F FF FD')
    print(ber_decode(test.element['I_Information'].value))


