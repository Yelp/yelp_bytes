# -*- coding: utf-8 -*-
from yelp_encodings import internet


internet.register()


def to_bytes(x, encoding='internet'):
    """
    Encode values to utf-8 bytestrings (str).
    str-type values are returned as-is, with the fervent hope that they're already utf8.

    This function always returns utf8-encoded bytes.
    """
    if isinstance(x, str):
        # In this case we have to assume it's already utf8.
        return x
    else:
        return unicode(x).encode(encoding)


def from_bytes(x, encoding='internet', errors='strict'):
    """
    Decode values to unambiguous unicode characters.
    The "internet" codec attempts to use utf8, but falls back to latin1 if there are obviously non-utf8 bytes.

    This function always returns unicode.
    """
    if isinstance(x, unicode):
        return x
    try:
        return unicode(x, encoding, errors)
    except TypeError:
        # We're only allowed to specify an encoding for str values, for whatever reason.
        try:
            return unicode(x)
        except UnicodeDecodeError:
            # You get this (for example) when an error object contains utf8 bytes.
            return unicode(str(x), encoding, errors)


def to_utf8(x):
    """Encode unicode text to utf8 bytes (str)."""
    return to_bytes(x, encoding='utf-8')


def from_utf8(x, errors='strict'):
    """Decode utf8 bytes (str) to unicode text."""
    return from_bytes(x, encoding='utf-8', errors=errors)
