# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from yelp_bytes import to_bytes, to_utf8, to_native, from_bytes, from_utf8, unicode, PY2


# Define some interesting unicode inputs
class UNICODE:
    ascii = 'A'  # The most basic of unicode.
    latin1 = ascii + 'ü'  # U-umlaut. This is defined in latin1 but not ascii.
    win1252 = latin1 + '€'  # Euro sign. This is defined in windows-1252, but not latin1.
    bmp = win1252 + 'Ł'  # Polish crossed-L. This requires at least a two-byte encoding.
    utf8 = bmp + '🐵'  # Monkey-face emoji. This requires at least a three-byte encoding.


def dunder_compat(cls):
    if PY2:
        if hasattr(cls, '__bytes__'):
            cls.__str__ = cls.__bytes__
            del cls.__bytes__
    elif hasattr(cls, '__unicode__'):
        cls.__str__ = cls.__unicode__
        del cls.__unicode__
    return cls


@dunder_compat
class Unicodable:
    """unicode() is fine, but bytes() will barf"""
    def __unicode__(self):
        return UNICODE.utf8


unicodable = Unicodable()


@dunder_compat
class Utf8able:
    """bytes() and decode('UTF-8') is fine, but unicode() will barf"""
    def __bytes__(self):
        return UNICODE.utf8.encode('utf8')


utf8able = Utf8able()


@dunder_compat
class Win1252able:
    """bytes() is fine, but unicode() and decode('UTF-8') will barf"""
    def __bytes__(self):
        return UNICODE.utf8.encode('windows-1252', 'ignore')


win1252able = Win1252able()


class BytesLike:
    """looks a bit like python3 bytes, emulating a list of ints"""
    def __iter__(self):
        return iter(range(10))


byteslike = BytesLike()
bytesvalue = b''.join(
    chr(b) if PY2 else bytes([b])
    for b in byteslike
)


both_from_funcs = pytest.mark.parametrize('testfunc', (from_bytes, from_utf8))
both_to_funcs = pytest.mark.parametrize('testfunc', (to_bytes, to_utf8))


@both_from_funcs
def test_with_unicode(testfunc):
    # Unicode objects aren't touched.
    assert UNICODE.utf8 is testfunc(UNICODE.utf8)


@both_from_funcs
def test_with_unicode_subclass(testfunc):
    # Unicode subclasses (eg markupsafe) also go unmolested.
    class MyText(unicode):
        pass
    mytext = MyText("abcdef")
    assert mytext is testfunc(mytext)


@both_to_funcs
def test_with_bytes_subclass(testfunc):
    # it would make sense for the same (above) to hold of a bytes subclass
    class MyBytes(bytes):
        pass
    mybytes = MyBytes(b"abcdef")
    assert mybytes is testfunc(mybytes)


@both_from_funcs
def test_with_utf8(testfunc):
    utf8 = UNICODE.utf8.encode('utf8')
    assert UNICODE.utf8 == testfunc(utf8)


def test_with_win1252():
    win1252 = UNICODE.utf8.encode('windows-1252', 'ignore')
    assert UNICODE.win1252.encode('windows-1252') == win1252
    assert UNICODE.win1252 == from_bytes(win1252)


@both_from_funcs
def test_from_funcs_with_unicodable_object(testfunc):
    assert UNICODE.utf8 == testfunc(unicodable)


@both_from_funcs
def test_from_funcs_with_utf8able_object(testfunc):
    expected = UNICODE.utf8 if PY2 else repr(utf8able)
    assert expected == testfunc(utf8able)


def test_from_bytes_with_win1252able_object():
    expected = UNICODE.win1252 if PY2 else repr(win1252able)
    assert expected == from_bytes(win1252able)


def test_from_utf8_with_win1252():
    win1252 = UNICODE.utf8.encode('windows-1252', 'ignore')
    with pytest.raises(UnicodeDecodeError):
        from_utf8(win1252)


def test_from_utf8_with_win1252able_object():
    if PY2:
        with pytest.raises(UnicodeDecodeError):
            from_utf8(win1252able)
    else:
        assert repr(win1252able) == from_utf8(win1252able)


@both_from_funcs
def test_from_funcs_with_byteslike_object(testfunc):
    expected = repr(byteslike)
    assert expected == testfunc(byteslike)


@both_to_funcs
def test_to_bytes_from_unicode(testfunc):
    assert UNICODE.utf8.encode('utf8') == testfunc(UNICODE.utf8)


@both_to_funcs
def test_to_bytes_from_utf8(testfunc):
    utf8 = UNICODE.utf8.encode('utf8')
    assert utf8 == testfunc(utf8)


@both_to_funcs
def test_to_bytes_from_bad_utf8(testfunc):
    # The to_bytes function doesn't attempt to auto-magically fix non-utf8 encodings.
    win1252 = UNICODE.utf8.encode('windows-1252', 'ignore')
    assert UNICODE.win1252.encode('windows-1252') == win1252
    assert win1252 == testfunc(win1252)


@both_to_funcs
def test_to_funcs_with_unicodable_object(testfunc):
    assert UNICODE.utf8.encode('UTF-8') == testfunc(unicodable)


@both_to_funcs
def test_to_funcs_with_utf8able_object(testfunc):
    expected = UNICODE.utf8 if PY2 else repr(utf8able)
    expected = expected.encode('UTF-8')
    assert expected == testfunc(utf8able)


@both_to_funcs
def test_to_funcs_with_win1252able_object(testfunc):
    expected = UNICODE.win1252 if PY2 else repr(win1252able)
    expected = expected.encode('windows-1252')
    assert expected == testfunc(win1252able)


@both_to_funcs
def test_to_funcs_with_byteslike_object(testfunc):
    expected = repr(byteslike).encode('US-ASCII')
    assert expected == testfunc(byteslike)


@pytest.mark.parametrize('value', (
    UNICODE.utf8,
    unicodable,
    utf8able,
    win1252able,
    byteslike,
))
def test_internet_roundtrip(value):
    assert from_bytes(value) == to_bytes(value).decode('internet')


@pytest.mark.parametrize('value', (
    UNICODE.utf8,
    unicodable,
    utf8able,
))
def test_utf8_roundtrip(value):
    assert from_bytes(value, 'utf8') == to_bytes(value, 'utf8').decode('utf8')


@pytest.mark.parametrize('value', (
    UNICODE.win1252,
    win1252able,
))
def test_windows_roundtrip(value):
    assert from_bytes(value, 'windows-1252') == to_bytes(value, 'windows-1252').decode('windows-1252')


@pytest.mark.parametrize('value', (
    UNICODE.utf8,
    utf8able,
    win1252able,
    byteslike,
))
def test_to_bytes_is_like_str_encode(value):
    # pylint:disable=bare-except,broad-except,redefined-variable-type
    try:
        bytes_result = str(value) if PY2 else str(value).encode('US-ASCII')
    except Exception:
        bytes_result = '(error)'

    try:
        to_bytes_result = to_bytes(value, 'US-ASCII')
    except Exception:
        to_bytes_result = '(error)'

    assert bytes_result == to_bytes_result


@pytest.mark.parametrize('value', (
    UNICODE.latin1,
    UNICODE.win1252,
    UNICODE.bmp,
    UNICODE.utf8,
))
def test_to_native_with_unicode_objects(value):  # pragma: no cover
    if PY2:
        assert to_native(value) == value.encode('UTF-8')
    else:
        assert to_native(value) == value


@pytest.mark.parametrize('value', (
    UNICODE.latin1.encode('latin1'),
    UNICODE.win1252.encode('cp1252'),
    UNICODE.bmp.encode('UTF-8'),
    UNICODE.utf8.encode('UTF-8'),
))
def test_to_native_with_byte_string(value):  # pragma: no cover
    if PY2:
        assert to_native(value) == value
    else:
        assert to_native(value) == from_bytes(value)


def test_to_native_unicodable():
    expected = UNICODE.utf8.encode('UTF-8') if PY2 else UNICODE.utf8
    assert to_native(unicodable) == expected


def test_to_native_utf8able():
    expected = UNICODE.utf8.encode('UTF-8') if PY2 else repr(utf8able)
    assert to_native(utf8able) == expected


def test_to_native_win1252able():
    expected = UNICODE.utf8.encode('cp1252', 'ignore') if PY2 else repr(win1252able)
    assert to_native(win1252able) == expected
