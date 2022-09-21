from typing import Any
from typing import Tuple
from typing import Union

from yelp_encodings import internet


internet.register()


def bytes_or_unicode(obj: Any) -> Tuple[type, Union[str, bytes]]:
    """Determine of an object is more canonically represented as bytes or unicode."""
    if isinstance(obj, bytes):
        return bytes, obj

    if isinstance(obj, str):
        return str, obj

    try:
        return str, str(obj)
    except UnicodeDecodeError:
        return bytes, bytes(obj)


def to_bytes(obj: Any, encoding: str = "internet", errors: str = "strict") -> bytes:
    """
    Encode values to utf-8 bytestrings (str).
    str-type values are returned as-is, with the fervent hope that they're already utf8.

    This function always returns utf8-encoded bytes (unless given non-utf8 bytes).
    """
    type, obj = bytes_or_unicode(obj)
    if type is bytes:
        return obj

    # This is definitely unicode.
    return obj.encode(encoding, errors)  # pylint:disable=maybe-no-member


def from_bytes(obj: Any, encoding: str = "internet", errors: str = "strict") -> str:
    """
    Decode values to unambiguous unicode characters.
    The "internet" codec attempts to use utf8, but falls back to latin1 if there are obviously non-utf8 bytes.

    This function always returns unicode.
    """
    type, obj = bytes_or_unicode(obj)
    if type is bytes:
        return obj.decode(encoding, errors)
    return obj


def to_utf8(obj: Any, errors: str = "strict") -> bytes:
    """Encode unicode text to utf8 bytes (str)."""
    return to_bytes(obj, encoding="utf-8", errors=errors)


def from_utf8(obj: Any, errors: str = "strict") -> str:
    """Decode utf8 bytes (str) to unicode text."""
    return from_bytes(obj, encoding="utf-8", errors=errors)


def to_native(
    obj: Any, encoding: str = "internet", errors: str = "strict"
) -> str:  # pragma: no cover
    """returns a native string regardless of py env"""
    if isinstance(obj, str):
        return obj

    return from_bytes(obj, encoding, errors)
