"""File generated by TLObjects' generator. All changes will be ERASED"""
from ...tl.tlobject import TLObject
from ...tl import types
from ...utils import get_input_peer, get_input_channel, get_input_user, get_input_media, get_input_photo
import os
import struct


class ClearSavedInfoRequest(TLObject):
    CONSTRUCTOR_ID = 0xd83d70c1
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, credentials=None, info=None):
        """
        :param bool | None credentials:
        :param bool | None info:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.credentials = credentials
        self.info = info

    def to_dict(self, recursive=True):
        return {
            'credentials': self.credentials,
            'info': self.info,
        }

    def __bytes__(self):
        return b''.join((
            b'\xc1p=\xd8',
            struct.pack('<I', (1 if self.credentials else 0) | (2 if self.info else 0)),
        ))

    @staticmethod
    def from_reader(reader):
        flags = reader.read_int()

        _credentials = bool(flags & 1)
        _info = bool(flags & 2)
        return ClearSavedInfoRequest(credentials=_credentials, info=_info)

    def on_response(self, reader):
        self.result = reader.tgread_object()

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)


class GetPaymentFormRequest(TLObject):
    CONSTRUCTOR_ID = 0x99f09745
    SUBCLASS_OF_ID = 0xa0483f19

    def __init__(self, msg_id):
        """
        :param int msg_id:

        :returns payments.PaymentForm: Instance of PaymentForm.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.msg_id = msg_id

    def to_dict(self, recursive=True):
        return {
            'msg_id': self.msg_id,
        }

    def __bytes__(self):
        return b''.join((
            b'E\x97\xf0\x99',
            struct.pack('<i', self.msg_id),
        ))

    @staticmethod
    def from_reader(reader):
        _msg_id = reader.read_int()
        return GetPaymentFormRequest(msg_id=_msg_id)

    def on_response(self, reader):
        self.result = reader.tgread_object()

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)


class GetPaymentReceiptRequest(TLObject):
    CONSTRUCTOR_ID = 0xa092a980
    SUBCLASS_OF_ID = 0x590093c9

    def __init__(self, msg_id):
        """
        :param int msg_id:

        :returns payments.PaymentReceipt: Instance of PaymentReceipt.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.msg_id = msg_id

    def to_dict(self, recursive=True):
        return {
            'msg_id': self.msg_id,
        }

    def __bytes__(self):
        return b''.join((
            b'\x80\xa9\x92\xa0',
            struct.pack('<i', self.msg_id),
        ))

    @staticmethod
    def from_reader(reader):
        _msg_id = reader.read_int()
        return GetPaymentReceiptRequest(msg_id=_msg_id)

    def on_response(self, reader):
        self.result = reader.tgread_object()

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)


class GetSavedInfoRequest(TLObject):
    CONSTRUCTOR_ID = 0x227d824b
    SUBCLASS_OF_ID = 0xad3cf146

    def __init__(self):
        super().__init__()
        self.result = None
        self.content_related = True

    def to_dict(self, recursive=True):
        return {}

    def __bytes__(self):
        return b''.join((
            b'K\x82}"',
        ))

    @staticmethod
    def from_reader(reader):
        return GetSavedInfoRequest()

    def on_response(self, reader):
        self.result = reader.tgread_object()

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)


class SendPaymentFormRequest(TLObject):
    CONSTRUCTOR_ID = 0x2b8879b3
    SUBCLASS_OF_ID = 0x8ae16a9d

    def __init__(self, msg_id, credentials, requested_info_id=None, shipping_option_id=None):
        """
        :param int msg_id:
        :param str | None requested_info_id:
        :param str | None shipping_option_id:
        :param TLObject credentials:

        :returns payments.PaymentResult: Instance of either PaymentResult, PaymentVerficationNeeded.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.msg_id = msg_id
        self.requested_info_id = requested_info_id
        self.shipping_option_id = shipping_option_id
        self.credentials = credentials

    def to_dict(self, recursive=True):
        return {
            'msg_id': self.msg_id,
            'requested_info_id': self.requested_info_id,
            'shipping_option_id': self.shipping_option_id,
            'credentials': (None if self.credentials is None else self.credentials.to_dict()) if recursive else self.credentials,
        }

    def __bytes__(self):
        return b''.join((
            b'\xb3y\x88+',
            struct.pack('<I', (1 if self.requested_info_id else 0) | (2 if self.shipping_option_id else 0)),
            struct.pack('<i', self.msg_id),
            b'' if not self.requested_info_id else (TLObject.serialize_bytes(self.requested_info_id)),
            b'' if not self.shipping_option_id else (TLObject.serialize_bytes(self.shipping_option_id)),
            bytes(self.credentials),
        ))

    @staticmethod
    def from_reader(reader):
        flags = reader.read_int()

        _msg_id = reader.read_int()
        if flags & 1:
            _requested_info_id = reader.tgread_string()
        else:
            _requested_info_id = None
        if flags & 2:
            _shipping_option_id = reader.tgread_string()
        else:
            _shipping_option_id = None
        _credentials = reader.tgread_object()
        return SendPaymentFormRequest(msg_id=_msg_id, credentials=_credentials, requested_info_id=_requested_info_id, shipping_option_id=_shipping_option_id)

    def on_response(self, reader):
        self.result = reader.tgread_object()

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)


class ValidateRequestedInfoRequest(TLObject):
    CONSTRUCTOR_ID = 0x770a8e74
    SUBCLASS_OF_ID = 0x8f8044b7

    def __init__(self, msg_id, info, save=None):
        """
        :param bool | None save:
        :param int msg_id:
        :param TLObject info:

        :returns payments.ValidatedRequestedInfo: Instance of ValidatedRequestedInfo.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.save = save
        self.msg_id = msg_id
        self.info = info

    def to_dict(self, recursive=True):
        return {
            'save': self.save,
            'msg_id': self.msg_id,
            'info': (None if self.info is None else self.info.to_dict()) if recursive else self.info,
        }

    def __bytes__(self):
        return b''.join((
            b't\x8e\nw',
            struct.pack('<I', (1 if self.save else 0)),
            struct.pack('<i', self.msg_id),
            bytes(self.info),
        ))

    @staticmethod
    def from_reader(reader):
        flags = reader.read_int()

        _save = bool(flags & 1)
        _msg_id = reader.read_int()
        _info = reader.tgread_object()
        return ValidateRequestedInfoRequest(msg_id=_msg_id, info=_info, save=_save)

    def on_response(self, reader):
        self.result = reader.tgread_object()

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)
