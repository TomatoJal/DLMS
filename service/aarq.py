from base_type import *
from ber import *


class AARQ(DLMSBaseType):
    """
    HDLC flag 类, flag 恒等于0x7E
    """
    HDLC_FLAG = 0x7E

    def __init__(self, frame):
        super(AARQ, self).__init__(frame)
        print(ber_decode(self.frame))
        # self.element['AARQ'] = DLMSBaseType.element_namedtuple(self.frame[0], None)
        # if len(self.frame) == 2:


class ApplicationContextName(DLMSBaseType):
    """
    application-context-name [1] Application-context-name
    Application-context-name ::= OBJECT IDENTIFIER
    """
    def __init__(self, frame):
        super(ApplicationContextName, self).__init__(frame)
        self.element['ApplicationContextName'] = DLMSBaseType.element_namedtuple(self.frame, None)
        if len(self.frame) == self.frame[1] + 2:
            self.set_info('ApplicationContextName', 'ApplicationContextName：' +
                          ''.join([to_hex(i) for i in self.frame]))


class CallingAPTitle(DLMSBaseType):
    """
    calling-AP-title [6] AP-title OPTIONAL
    AP-title ::= OCTET STRING
    """
    def __init__(self, frame):
        super(CallingAPTitle, self).__init__(frame)
        self.element['CallingAPTitle'] = DLMSBaseType.element_namedtuple(self.frame, None)
        if len(self.frame) == self.frame[1] + 2 and \
           self.frame[2] == 0x04 and self.frame[3] == len(self.frame) - 4:
            self.set_info('CallingAPTitle', 'CallingAPTitle：' +
                          ''.join([to_hex(i) for i in self.frame[4:]]))


class UserInformation(DLMSBaseType):
    """
    user-information [30] EXPLICIT Association-information OPTIONAL
    Association-information ::= OCTET STRING
    """
    def __init__(self, frame):
        super(UserInformation, self).__init__(frame)
        self.element['UserInformation'] = DLMSBaseType.element_namedtuple(self.frame, None)
        if len(self.frame) == self.frame[1] + 2 and \
           self.frame[2] == 0x04 and self.frame[3] == len(self.frame) - 4:
            self.set_info('UserInformation', 'UserInformation：' +
                          ''.join([to_hex(i) for i in self.frame[4:]]))


if __name__ == '__main__':
    test = AARQ('60 29 A1 09 06 07 60 85 74 05 08 01 01 A6 0A 04 08 00 00 00 00 00 00 98 00 BE 10 04 0E 01 00 00 00 06 5F 1F 04 00 00 1F 3F FF FD')
    print(test.get_info)
    AARQ('A1 09 06 07 60 85 74 05 08 01 01 A6 0A 04 08 00 00 00 00 00 00 98 00 BE 10 04 0E 01 00 00 00 06 5F 1F 04 00 00 1F 3F FF FD')

    print(ApplicationContextName('A1 09 06 07 60 85 74 05 08 01 01').get_info)
    print(CallingAPTitle('A6 0A 04 08 00 00 00 00 00 00 98 00').get_info)
    print(UserInformation('BE 10 04 0E 01 00 00 00 06 5F 1F 04 00 00 1F 3F FF FD').get_info)

    print(ber_decode(array('B', [0x5F,0x1F,0x04,0x00,0x00,0x1F,0x3F])))
