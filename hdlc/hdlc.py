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
            self._set_info('flag', f'flag: ' + u8_to_hex(f))

if __name__ == '__main__':
    flag = HDLCFlag('7E')
    print(flag.get_info)
