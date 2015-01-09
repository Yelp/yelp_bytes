# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yelp_encodings import internet


internet.register()
unicode = type("")


def to_bytes(obj, encoding='internet', errors='strict'):
    """
    Encode values to utf-8 bytestrings (str).
    str-type values are returned as-is, with the fervent hope that they're already utf8.

    This function always returns utf8-encoded bytes (unless given non-utf8 bytes).
    """
    mro = type(obj).mro()
    if bytes in mro:
        return obj
    elif unicode in mro:
        return obj.encode(encoding, errors)
    elif hasattr(obj, '__bytes__'):
        return obj.__bytes__()

    try:
        return unicode(obj).encode(encoding, errors)
    except UnicodeDecodeError:
        # You get this (for example) when an error object contains utf8 bytes.
        return bytes(obj)


def from_bytes(obj, encoding='internet', errors='strict'):
    """
    Decode values to unambiguous unicode characters.
    The "internet" codec attempts to use utf8, but falls back to latin1 if there are obviously non-utf8 bytes.

    This function always returns unicode.
    """
    mro = type(obj).mro()
    if unicode in mro:
        return obj
    elif bytes in mro:
        return obj.decode(encoding, errors)
    elif hasattr(obj, '__bytes__'):
        return obj.__bytes__().decode(encoding, errors)

    try:
        return unicode(obj)
    except UnicodeDecodeError:
        # You get this (for example) when an error object contains utf8 bytes.
        return bytes(obj).decode(encoding, errors)


def to_utf8(obj, errors='strict'):
    """Encode unicode text to utf8 bytes (str)."""
    return to_bytes(obj, encoding='utf-8', errors=errors)


def from_utf8(obj, errors='strict'):
    """Decode utf8 bytes (str) to unicode text."""
    return from_bytes(obj, encoding='utf-8', errors=errors)
