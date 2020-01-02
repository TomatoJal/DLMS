# -*- coding: UTF-8 -*-
"""
HDLC frame format type 3:
Flag|Frame format|Dest.address|Src.address|Control|HCS|Information|FCS|Flag|
"""

from base_type import DLMSBaseType, to_hex


class HDLCFlag(DLMSBaseType):
    """
    HDLC flag 类, flag 恒等于0x7E
    """
    HDLC_FLAG = 0x7E

    def __init__(self, frame):
        super(HDLCFlag, self).__init__(frame)
        self.element['flag'] = DLMSBaseType.element_namedtuple(self.frame, None)
        # 长度1字节,值恒为0x7E
        if len(self.frame) == 1 and self.element['flag'].value[0] == self.HDLC_FLAG:
            f = self.frame[0]
            self._set_info('flag', 'flag: ' + to_hex(f))


class HDLCFormat(DLMSBaseType):
    """
    HDLC format类
    MSB                                  LSB
    |1 0 1 0    | S |L L L L L L L L L L L |
    |Format type|   |Frame length sub-field|
    """
    def __init__(self, frame):
        super(HDLCFormat, self).__init__(frame)
        self.element['format'] = DLMSBaseType.element_namedtuple(self.frame, None)
        # 长度2字节
        if len(self.frame) == 2:
            ft = self.frame[0] >> 4
            s = self.frame[0] & 0b00001000
            length = ((self.frame[0] & 0b00000111) << 8) + self.frame[1]
            self._set_info('format', 'format type: ' + to_hex(ft) + ',' +
                                     'segmentation: ' + str(s) + ',' +
                                     'frame length sub-field: ' + str(length))


class HDLCAddress(DLMSBaseType):
    """
    HDLC 地址抽象类
    client addresses:
    No-station----------------------0x00
    Client Management Process-------0x01
    Public Client-------------------0x10
    Open for client SAP assignment--0x02…0x0F
                                  --0x11…0xFF

    server addresses:
    upper HDLC addresses:           One         Two
    No-station                      0x00        0x0000
    Management Logical Device       0x01        0x0001
    Reserved for future use         0x02…0x0F   0x0002…0x000F
    Open for server SAP assignment  0x10…0x7E   0x0010…0x3FFE
    All-station (Broadcast)         0x7F        0x3FFF
    ---------------------------------------------------------
    lower HDLC addresses:
    No-station                      0x00        0x0000
    Reserved for future use         0x01…0x0F   0x0001…0x000F
    Open for server SAP assignment  0x10…0x7D   0x0010…0x3FFD
    CALLING a ) Physical Device     0x7E        0x3FFE
    All-station (Broadcast)         0x7F        0x3FFF
    """
    def __init__(self, frame, owner):
        super(HDLCAddress, self).__init__(frame)
        self.element[owner] = DLMSBaseType.element_namedtuple(self.frame, None)
        """
                                |LSB|                       |LSB|                       |LSB|                       |LSB
        Upper HDLC address      |1  |                       |   |                       |   |                       |
        Upper HDLC address      |0  |Lower HDLC address     |1  |                       |   |                       |
        Upper HDLC addr. high   |0  |Upper HDLC addr. low   |0  |Lower HDLC addr. high  |0  |Lower HDLC addr. low   |1
        First byte                  |Second byte                |Third byte                 |Fourth byte
        """
        if len(self.frame) == 1 and (self.frame[0] & 0x01 == 1) or \
           len(self.frame) == 2 and (self.frame[0] & 0x01 == 0) and (self.frame[1] & 0x01 == 1) or \
           len(self.frame) == 4 and (self.frame[0] & 0x01 == 0) and (self.frame[1] & 0x01 == 1) \
                                and (self.frame[2] & 0x01 == 0) and (self.frame[3] & 0x01 == 1):
            tmp = 0
            for i in self.frame:
                tmp = (tmp << 8) + i
            # 如何区分server/client?
            self._set_info(owner, owner + ' address: ' + to_hex(tmp))


if __name__ == '__main__':
    flag = HDLCFlag('7E')
    print(flag.get_info)

    form = HDLCFormat('A0 21')
    print(form.get_info)

    dest = HDLCAddress('02 23', 'dest')
    print(dest.get_info)

    src = HDLCAddress('21', 'src')
    print(src.get_info)

    print(flag + form + dest + src)
    print((flag + form + dest + src).get_info)
