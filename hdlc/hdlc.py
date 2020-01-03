# -*- coding: UTF-8 -*-


from base_type import DLMSBaseType, to_hex, trans_to_array

fcstab = [
    0x0000, 0x1189, 0x2312, 0x329b, 0x4624, 0x57ad, 0x6536, 0x74bf,
    0x8c48, 0x9dc1, 0xaf5a, 0xbed3, 0xca6c, 0xdbe5, 0xe97e, 0xf8f7,
    0x1081, 0x0108, 0x3393, 0x221a, 0x56a5, 0x472c, 0x75b7, 0x643e,
    0x9cc9, 0x8d40, 0xbfdb, 0xae52, 0xdaed, 0xcb64, 0xf9ff, 0xe876,
    0x2102, 0x308b, 0x0210, 0x1399, 0x6726, 0x76af, 0x4434, 0x55bd,
    0xad4a, 0xbcc3, 0x8e58, 0x9fd1, 0xeb6e, 0xfae7, 0xc87c, 0xd9f5,
    0x3183, 0x200a, 0x1291, 0x0318, 0x77a7, 0x662e, 0x54b5, 0x453c,
    0xbdcb, 0xac42, 0x9ed9, 0x8f50, 0xfbef, 0xea66, 0xd8fd, 0xc974,
    0x4204, 0x538d, 0x6116, 0x709f, 0x0420, 0x15a9, 0x2732, 0x36bb,
    0xce4c, 0xdfc5, 0xed5e, 0xfcd7, 0x8868, 0x99e1, 0xab7a, 0xbaf3,
    0x5285, 0x430c, 0x7197, 0x601e, 0x14a1, 0x0528, 0x37b3, 0x263a,
    0xdecd, 0xcf44, 0xfddf, 0xec56, 0x98e9, 0x8960, 0xbbfb, 0xaa72,
    0x6306, 0x728f, 0x4014, 0x519d, 0x2522, 0x34ab, 0x0630, 0x17b9,
    0xef4e, 0xfec7, 0xcc5c, 0xddd5, 0xa96a, 0xb8e3, 0x8a78, 0x9bf1,
    0x7387, 0x620e, 0x5095, 0x411c, 0x35a3, 0x242a, 0x16b1, 0x0738,
    0xffcf, 0xee46, 0xdcdd, 0xcd54, 0xb9eb, 0xa862, 0x9af9, 0x8b70,
    0x8408, 0x9581, 0xa71a, 0xb693, 0xc22c, 0xd3a5, 0xe13e, 0xf0b7,
    0x0840, 0x19c9, 0x2b52, 0x3adb, 0x4e64, 0x5fed, 0x6d76, 0x7cff,
    0x9489, 0x8500, 0xb79b, 0xa612, 0xd2ad, 0xc324, 0xf1bf, 0xe036,
    0x18c1, 0x0948, 0x3bd3, 0x2a5a, 0x5ee5, 0x4f6c, 0x7df7, 0x6c7e,
    0xa50a, 0xb483, 0x8618, 0x9791, 0xe32e, 0xf2a7, 0xc03c, 0xd1b5,
    0x2942, 0x38cb, 0x0a50, 0x1bd9, 0x6f66, 0x7eef, 0x4c74, 0x5dfd,
    0xb58b, 0xa402, 0x9699, 0x8710, 0xf3af, 0xe226, 0xd0bd, 0xc134,
    0x39c3, 0x284a, 0x1ad1, 0x0b58, 0x7fe7, 0x6e6e, 0x5cf5, 0x4d7c,
    0xc60c, 0xd785, 0xe51e, 0xf497, 0x8028, 0x91a1, 0xa33a, 0xb2b3,
    0x4a44, 0x5bcd, 0x6956, 0x78df, 0x0c60, 0x1de9, 0x2f72, 0x3efb,
    0xd68d, 0xc704, 0xf59f, 0xe416, 0x90a9, 0x8120, 0xb3bb, 0xa232,
    0x5ac5, 0x4b4c, 0x79d7, 0x685e, 0x1ce1, 0x0d68, 0x3ff3, 0x2e7a,
    0xe70e, 0xf687, 0xc41c, 0xd595, 0xa12a, 0xb0a3, 0x8238, 0x93b1,
    0x6b46, 0x7acf, 0x4854, 0x59dd, 0x2d62, 0x3ceb, 0x0e70, 0x1ff9,
    0xf78f, 0xe606, 0xd49d, 0xc514, 0xb1ab, 0xa022, 0x92b9, 0x8330,
    0x7bc7, 0x6a4e, 0x58d5, 0x495c, 0x3de3, 0x2c6a, 0x1ef1, 0x0f78
]


def cs_table_generate(tab=None):
    """
    生成hcs, fcs table 用表
    :param tab: 对比表
    :return: hcs fcs table 用表
    """
    ret = []
    P = 0x8408
    b = 0
    while True:
        v = b
        for i in range(0, 8):
            if (v & 1) == 1:
                v = (v >> 1) ^ P
            else:
                v = (v >> 1)
        ret.append(v & 0xFFFF)
        b += 1
        if b == 256:
            break
    if tab is not None:
        if tab != ret:
            return None
    return ret


def cal_check_field(frame):
    """
    计算校验
    :param frame: 计算帧
    :return: 计算FCS, HCS
    """
    if isinstance(frame, str) is True:
        frame = trans_to_array(frame)

    fcs = 0xffff

    for i in range(0, len(frame)):
        fcs = (fcs >> 8) ^ fcstab[(fcs ^ frame[i]) & 0xff]

    return (~fcs) & 0xFFFF


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
            self.set_info('flag', 'flag: ' + to_hex(f))


class HDLCFormat(DLMSBaseType):
    """
    HDLC format类
    MSB                                  LSB
    |1 0 1 0    | S |L L L L L L L L L L L |
    |Format type|   |Frame length sub-field|
    sub-field is 1010 (binary), which identifies a frame format type 3
    """
    def __init__(self, frame):
        super(HDLCFormat, self).__init__(frame)
        self.element['format'] = DLMSBaseType.element_namedtuple(self.frame, None)
        # 长度2字节
        if len(self.frame) == 2:
            ft = self.frame[0] >> 4
            s = self.frame[0] & 0b00001000
            self.length = ((self.frame[0] & 0b00000111) << 8) + self.frame[1]
            self.set_info('format', 'format type: ' + to_hex(ft) + ',' +
                                     'segmentation: ' + str(s) + ',' +
                                     'frame length sub-field: ' + str(self.length))


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
            self.set_info(owner, owner + ' address: ' + str((tmp & 0xFF) >> 1))


class HDLCControl(DLMSBaseType):
    """
    HDLC control类：
    Command Response    MSB           LSB
    I       I           R R R P/F S S S 0
    RR      RR          R R R P/F 0 0 0 1   (Receive ready)
    RNR     RNR         R R R P/F 0 1 0 1   (Receive not ready)
    SNRM                1 0 0  P  0 0 1 1   (Set normal response mode)
    DISC                0 1 0  P  0 0 1 1   (Disconnect)
            UA          0 1 1  F  0 0 1 1   (Unnumbered acknowledge)
            DM          0 0 0  F  1 1 1 1   (Disconnected mode)
            FRMR        1 0 0  F  0 1 1 1   (Frame reject)
    UI      UI          0 0 0 P/F 0 0 1 1   (Unnumbered information)
    RRR is the receive sequence number N(R)
    SSS is the send sequence number N(S)
    P/F is the poll/final bit.
    """
    def __init__(self, frame):
        super(HDLCControl, self).__init__(frame)
        self.element['control'] = DLMSBaseType.element_namedtuple(self.frame, None)
        if len(self.frame) == 1:
            control = self.element['control'][0][0]
            pf = ((control & 0b00010000) >> 4)
            receive = control >> 5
            send = ((control & 0b00001110) >> 5)
            # I|R R R P/F S S S 0
            if control & 0b00000001 == 0:
                self.frame_type = 'I'
                self.set_info('control', 'I frame, ' + f'receive: {receive}, send: {send}, '
                                        f'P/F: {pf}')
            # RR|R R R P/F 0 0 0 1
            elif control & 0b00001111 == 0b0001:
                self.frame_type = 'RR'
                self.set_info('control', 'RR frame, ' + f'receive: {receive}, P/F: {pf}')
            # RNR|R R R P/F 0 1 0 1
            elif control & 0b00001111 == 0b0101:
                self.frame_type = 'RNR'
                self.set_info('control', 'RNR frame, ' + f'receive: {receive}, P/F: {pf}')
            # SNRM|1 0 0 P 0 0 1 1
            elif control & 0b11101111 == 0b10000011:
                self.frame_type = 'SNRM'
                self.set_info('control', 'SNRM frame, ' + f'Poll: {pf}')
            # DISC|0 1 0 P 0 0 1 1
            elif control & 0b11101111 == 0b01000011:
                self.frame_type = 'DISC'
                self.set_info('control', 'DISC frame, ' + f'Poll: {pf}')
            # UA|0 1 1 F 0 0 1 1
            elif control & 0b11101111 == 0b01100011:
                self.frame_type = 'UA'
                self.set_info('control', 'UA frame, ' + f'Final: {pf}')
            # DM|0 0 0 F 1 1 1 1
            elif control & 0b11101111 == 0b00001111:
                self.frame_type = 'DM'
                self.set_info('control', 'DM frame, ' + f'Final: {pf}')
            # FRMR|1 0 0 F 0 1 1 1
            elif control & 0b11101111 == 0b10000111:
                self.frame_type = 'FRMR'
                self.set_info('control', 'FRMR frame, ' + f'Final: {pf}')
            # UI|0 0 0 P/F 0 0 1 1
            elif control & 0b11100011 == 0b00000011:
                self.frame_type = 'UI'
                self.set_info('control', 'FRMR frame,' + f'P/f: {pf}')


class HDLCCS(DLMSBaseType):
    """
    Header check sequence (HCS) field
    Frame check sequence (FCS) field
    """
    def __init__(self, frame, ht, header=None):
        super(HDLCCS, self).__init__(frame)
        self.element[ht] = DLMSBaseType.element_namedtuple(self.frame, None)
        # 长度1字节,值恒为0x7E
        if len(self.frame) == 2:
            hcs = self.frame[0] + (self.frame[1] << 8)
            if header is not None:
                if hcs != cal_check_field(header):
                    return
            self.set_info(ht, ht + ': 0x' + to_hex(hcs))


class HDLCInformation(DLMSBaseType):
    """
    User information 类
    """
    def __init__(self, frame):
        super(HDLCInformation, self).__init__(frame)
        self.element['information'] = DLMSBaseType.element_namedtuple(self.frame, None)
        info = ''
        for i in self.frame:
            info += to_hex(i) + ' '
        self.set_info('information', 'information：' + info)


def hdlc(frame):
    """
    HDLC frame format type 3:
    Flag|Frame format|Dest.address|Src.address|Control|HCS|Information|FCS|Flag|
    :param frame: 帧
    :return: 正确帧返回HDLC类
    """
    frame = trans_to_array(frame)
    # Flag
    flag1 = HDLCFlag([frame[0]])
    flag2 = HDLCFlag([frame[-1]])
    if flag1.element['flag'].info is None or flag2.element['flag'].info is None:
        return None
    # Frame format
    fo = HDLCFormat(frame[1:3])
    header = fo
    if fo.element['format'].info is None:
        header.set_info('format', 'Wrong format type')
    if fo.length != len(frame) - 3:
        header.set_info('format', 'Wrong length in format type')
    # Dest.address
    dest = None
    for a in range(3, 7):
        if frame[a] & 0x00000001 == 1:
            dest = HDLCAddress(frame[3: a+1], 'dest')
            break
    header += dest
    if dest.element['dest'].info is None:
        header.set_info('dest', 'Wrong dest address')
    # Src.address
    src = None
    for b in range(a+1, a+5):
        if frame[b] & 0x00000001 == 1:
            src = HDLCAddress(frame[a+1: b+1], 'src')
            break
    header += src
    if src.element['src'].info is None:
        header.set_info('src', 'Wrong src address')
    # Control
    control = HDLCControl([frame[b+1]])
    header += control
    if control.element['control'].info is None:
        header.set_info('control', 'Wrong control byte')
    # HCS
    hcs = HDLCCS(frame[b+2: b+4], 'HCS', header.frame)
    header += hcs
    if hcs.element['HCS'].info is None:
        header.set_info('HCS', 'Wrong HCS byte')
    # user information
    information = HDLCInformation(frame[b+4: -3])
    header += information
    if information.element['information'].info is None:
        header.set_info('information', 'Wrong information')
    # FCS
    if len(information.frame) != 0:
        fcs = HDLCCS(frame[-3: -1], 'FCS', header.frame)
        header += fcs
        if fcs.element['FCS'].info is None:
            header.set_info('FCS', 'Wrong FCS byte')
    else:
        fcs = HDLCCS('', 'FCS')
        header += fcs
        header.set_info('FCS', 'No FCS')
    return flag1 + header +flag2


if __name__ == '__main__':
    test = hdlc('7E A0 08 02 23 21 53 B1 A2 7E')
    print(test.get_info)


