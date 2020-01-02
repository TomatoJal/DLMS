# -*- coding: UTF-8 -*-
"""
HDLC frame format type 3:
Flag|Frame format|Dest.address|Src.address|Control|HCS|Information|FCS|Flag|
"""

from base_type import DLMSBaseType, u8_to_hex


class HDLCFlag(DLMSBaseType):
    """
    HDLC flag 类, flag 恒等于0x7E
    """
    HDLC_FLAG = 0x7E

    def __init__(self, frame):
        super(HDLCFlag, self).__init__(frame)
        self.element['flag'] = DLMSBaseType.element_namedtuple(self.frame[0], None)
        # 长度1字节,值恒为0x7E
        if len(self.frame) == 1 and self.element['flag'].value == self.HDLC_FLAG:
            f = self.element['flag'].value
            self._set_info('flag', 'flag: ' + u8_to_hex(f))


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
            l = ((self.frame[0] & 0b00000111) << 8) + self.frame[1]
            self._set_info('format', 'format type: ' + u8_to_hex(ft) + ',' +
                                     'segmentation: ' + u8_to_hex(s) + ',' +
                                     'frame length sub-field: ' + u8_to_hex(l))


if __name__ == '__main__':
    flag = HDLCFlag('7E')
    print(flag.get_info)

    form = HDLCFormat('A0 21')
    print(form.get_info)

    print((flag + form).get_info)
    print(flag + form)
    print((flag + form).get_frame_string())
