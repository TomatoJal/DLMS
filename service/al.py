from base_type import *
from ber import *


def aarq(frame):
    """
    AARQ-apdu ::= [APPLICATION 0] IMPLICIT SEQUENCE
    {
        -- [APPLICATION 0] == [ 60H ] = [ 96 ]
        protocol-version             [0] IMPLICIT BIT STRING {version1 (0)}
        DEFAULT{version1},
        application-context-name     [1] Application-context-name,
        called-AP-title              [2] AP-title OPTIONAL,
        called-AE-qualifier          [3] AE-qualifier OPTIONAL,
        called-AP-invocation-id      [4] AP-invocation-identifier OPTIONAL,
        called-AE-invocation-id      [5] AE-invocation-identifier OPTIONAL,
        calling-AP-title             [6] AP-title OPTIONAL,
        calling-AE-qualifier         [7] AE-qualifier OPTIONAL,
        calling-AP-invocation-id     [8] AP-invocation-identifier OPTIONAL,
        calling-AE-invocation-id     [9] AE-invocation-identifier OPTIONAL,
        -- The following field shall not be present if only the kernel is used.
        sender-acse-requirements     [10] IMPLICIT ACSE-requirements OPTIONAL,
        -- The following field shall only be present if the authentication functional unit is selected.
        mechanism-name               [11] IMPLICIT Mechanism-name OPTIONAL,
        -- The following field shall only be present if the authentication functional unit is selected.
        calling-authentication-value [12] EXPLICIT Authentication-value OPTIONAL,
        implementation-information   [29] IMPLICIT Implementation-data OPTIONAL,
        user-information             [30] EXPLICIT Association-information OPTIONAL
    }
    -- The user-information field shall carry an InitiateRequest APDU encoded in A-XDR, and then
    -- encoding the resulting OCTET STRING in BER.
    """

    frame = trans_to_array(frame)
    b = ber_decode(frame)
    if b[0].cls == BER_TAG_TYPE_APPLICATION and b[0].rep == 0x60:
        frame = b[0].value
    else:
        return None

    ret = DLMSBaseType('')
    members = ber_decode(frame)
    for member in members:
        if member.cls == BER_TAG_TYPE_CONTEXT_SPECIFIC:
            if member.tag == 1:
                application_context_name = ApplicationContextName(member.frame)
                ret += application_context_name
            elif member.tag == 6:
                calling_ap_title = CallingAPTitle(member.frame)
                ret += calling_ap_title
            elif member.tag == 30:
                user_information = UserInformation(member.frame)
                ret += user_information
            else:
                return None
        else:
            return None

    return ret


class ApplicationContextName(DLMSBaseType):
    """
    application-context-name [1] Application-context-name
    Application-context-name ::= OBJECT IDENTIFIER
    short name (SN) referencing:    A1 09 06 07 60 85 74 05 08 01 01
    logical name (LN) referencing:  A1 09 06 07 60 85 74 05 08 01 02
    """
    def __init__(self, frame):
        super(ApplicationContextName, self).__init__(frame)
        self.element['ApplicationContextName'] = DLMSBaseType.element_namedtuple(self.frame, None)
        if len(self.frame) == self.frame[1] + 2 and \
                list(self.frame[2: -1]) == [0x06, 0x07, 0x60, 0x85, 0x74, 0x05, 0x08, 0x01]:
            if self.frame[-1] == 1:
                self.set_info('ApplicationContextName', 'ApplicationContextName：LN')
            elif self.frame[-1] == 2:
                self.set_info('ApplicationContextName', 'ApplicationContextName：SN')


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


class InitiateRequest(DLMSBaseType):
    """
    initiateRequest [1] IMPLICIT InitiateRequest,
    InitiateRequest ::= SEQUENCE
    {
        -- shall not be encoded in DLMS without ciphering
        dedicated-key                   OCTET STRING OPTIONAL,
        response-allowed                BOOLEAN DEFAULT TRUE,
        proposed-quality-of-service     IMPLICIT Integer8 OPTIONAL,
        proposed-dlms-version-number    Unsigned8,
        proposed-conformance            Conformance,
        client-max-receive-pdu-size     Unsigned16
    }
    """
    def __init__(self, frame):
        super(InitiateRequest, self).__init__(frame)
        offset = 1
        # dedicated-key
        self.element['dedicated_key'] = DLMSBaseType.element_namedtuple(self.frame, None)
        if self.frame[offset] != 00:
            pass
        else:
            self.set_info('dedicated_key', 'dedicated_key：FALSE, not present')
        offset += 1

        # response-allowed
        self.element['response_allowed'] = DLMSBaseType.element_namedtuple(self.frame, None)
        if self.frame[offset] != 00:
            pass
        else:
            self.set_info('response_allowed', 'response_allowed：FALSE, default value TRUE conveyed')
        offset += 1

        # proposed-quality-of-service
        self.element['proposed_quality_of_service'] = DLMSBaseType.element_namedtuple(self.frame, None)
        if self.frame[offset] != 00:
            pass
        else:
            self.set_info('proposed_quality_of_service', 'proposed_quality_of_service：'
                                                         'FALSE, not present')
            offset += 1

        # proposed-dlms-version-number
        self.element['proposed_dlms_version_number'] = DLMSBaseType.element_namedtuple(self.frame, None)
        if self.frame[offset] != 00:
            self.set_info('proposed_dlms_version_number', 'proposed_dlms_version_number：' +
                                                          to_hex(self.frame[offset]))
        else:
            pass
        offset += 1

        # proposed-conformance
        self.element['proposed_conformance'] = DLMSBaseType.element_namedtuple(self.frame, None)
        if self.frame[offset] != 00:
            self.set_info('proposed_conformance', 'proposed_conformance：' +
                          ''.join([to_hex(i) for i in self.frame[offset: len(self.frame) - 2]]))
        else:
            pass
        offset += (len(self.frame) - 2 - offset)

        # client-max-receive-pdu-size
        self.element['client_max_receive_pdu_size'] = DLMSBaseType.element_namedtuple(self.frame, None)
        if self.frame[offset] != 00:
            self.set_info('client_max_receive_pdu_size', 'client_max_receive_pdu_size：' + str(array_to_u32(self.frame[-2:])))
        else:
            pass


class Conformance(DLMSBaseType):
    """
    Conformance ::= [APPLICATION 31] IMPLICIT BIT STRING
    {
        -- the bit is set when the corresponding service or functionality is available
        reserved-zero (0),
        -- The actual list of general protection services depends on the security suite
        general-protection (1),
        general-block-transfer (2),
        read (3),
        write (4),
        unconfirmed-write (5),
        reserved-six (6),
        reserved-seven (7),
        attribute0-supported-with-set (8),
        priority-mgmt-supported (9),
        attribute0-supported-with-get (10),
        block-transfer-with-get-or-read (11),
        block-transfer-with-set-or-write (12),
        block-transfer-with-action (13),
        multiple-references (14),
        information-report (15),
        data-notification (16),
        access (17),
        parameterized-access (18),
        get (19),
        set (20),
        selective-access (21),
        event-notification (22),
        action (23)
    }
    """
    bit = ['action', 'event-notification', 'selective-access', 'set', 'get', 'parameterized-access', 'access',
           'data-notification', 'information-report', 'multiple-references', 'block-transfer-with-action',
           'block-transfer-with-set-or-write', 'block-transfer-with-get-or-read', 'attribute0-supported-with-get',
           'priority-mgmt-supported', 'attribute0-supported-with-set', 'reserved-seven', 'reserved-six',
           'unconfirmed-write', 'write', 'read', 'general-block-transfer', 'general-protection', 'reserved-zero']

    def __init__(self, frame):
        super(Conformance, self).__init__(frame)
        self.element['conformance'] = DLMSBaseType.element_namedtuple(self.frame, None)
        b = ber_decode(self.frame)
        info = ''
        if b is not None and b[0].tag == 31 and b[0].value[0] == 0:
            conformance = array_to_u32(b[0].value[1:])
            for i in range(0, 24):
                # info += ('\t\t' + 'bit ' + str(i).rjust(2, '0') + ': ' +
                #          str(((conformance & (1 << i)) >> i)) + ' : ' + self.bit[i] + '\r\n')
                info += ('\t\t' + str(((conformance & (1 << i)) >> i)) + ' : ' + self.bit[i] + '\r\n')
            self.set_info('conformance', 'conformance：\r\n' + info)


if __name__ == '__main__':
    print(aarq('60 29 A1 09 06 07 60 85 74 05 08 01 01 A6 0A 04 08 00 00 00 00 00 00 98 00 BE 10 04 0E 01 00 00 00 06 5F 1F 04 00 00 1F 3F FF FD').get_info)