# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yelp_encodings import internet


internet.register()
unicode = type("")

PY2 = str is bytes


def bytes_or_unicode(obj):
    """Determine of an object is more canonically represented as bytes or unicode."""
    mro = type(obj).mro()
    if bytes in mro:
        return bytes, obj
    elif unicode in mro:
        return unicode, obj

    try:
        return unicode, unicode(obj)
    except UnicodeDecodeError:
        return bytes, bytes(obj)


def to_bytes(obj, encoding='internet', errors='strict'):
    """
    Encode values to utf-8 bytestrings (str).
    str-type values are returned as-is, with the fervent hope that they're already utf8.

    This function always returns utf8-encoded bytes (unless given non-utf8 bytes).
    """
    type, obj = bytes_or_unicode(obj)
    if type is bytes:
        return obj
    else:
        # This is definitely unicode.
        return obj.encode(encoding, errors)  # pylint:disable=maybe-no-member


def from_bytes(obj, encoding='internet', errors='strict'):
    """
    Decode values to unambiguous unicode characters.
    The "internet" codec attempts to use utf8, but falls back to latin1 if there are obviously non-utf8 bytes.

    This function always returns unicode.
    """
    type, obj = bytes_or_unicode(obj)
    if type is bytes:
        return obj.decode(encoding, errors)
    else:
        return obj


def to_utf8(obj, errors='strict'):
    """Encode unicode text to utf8 bytes (str)."""
    return to_bytes(obj, encoding='utf-8', errors=errors)


def from_utf8(obj, errors='strict'):
    """Decode utf8 bytes (str) to unicode text."""
    return from_bytes(obj, encoding='utf-8', errors=errors)


def to_native(obj, encoding='internet', errors='strict'):  # pragma: no cover
    """ returns a native string regardless of py env """
    if isinstance(obj, str):
        return obj
    elif PY2:
        return to_bytes(obj, encoding, errors)
    else:  # PY3
        return from_bytes(obj, encoding, errors)
