# -*- coding: utf-8 -*-
from yelp_encodings import internet


internet.register()


def to_bytes(obj, encoding='internet'):
    """
    Encode values to utf-8 bytestrings (str).
    str-type values are returned as-is, with the fervent hope that they're already utf8.

    This function always returns utf8-encoded bytes.
    """
    if isinstance(obj, str):
        # In this case we have to assume it's already utf8.
        return obj
    else:
        return unicode(obj).encode(encoding)


def from_bytes(obj, encoding='internet', errors='strict'):
    """
    Decode values to unambiguous unicode characters.
    The "internet" codec attempts to use utf8, but falls back to latin1 if there are obviously non-utf8 bytes.

    This function always returns unicode.
    """
    if isinstance(obj, unicode):
        return obj
    try:
        return unicode(obj, encoding, errors)
    except TypeError:
        # We're only allowed to specify an encoding for str values, for whatever reason.
        try:
            return unicode(obj)
        except UnicodeDecodeError:
            # You get this (for example) when an error object contains utf8 bytes.
            return unicode(str(obj), encoding, errors)


def to_utf8(obj):
    """Encode unicode text to utf8 bytes (str)."""
    return to_bytes(obj, encoding='utf-8')


def from_utf8(obj, errors='strict'):
    """Decode utf8 bytes (str) to unicode text."""
    return from_bytes(obj, encoding='utf-8', errors=errors)
