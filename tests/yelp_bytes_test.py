# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from yelp_bytes import to_bytes, to_utf8, from_bytes, from_utf8, unicode


# Define some interesting unicode inputs
class UNICODE:
    ascii = 'A'  # The most basic of unicode.
    latin1 = ascii + 'ü'  # U-umlaut. This is defined in latin1 but not ascii.
    win1252 = latin1 + '€'  # Euro sign. This is defined in windows-1252, but not latin1.
    bmp = win1252 + 'Ł'  # Polish crossed-L. This requires at least a two-byte encoding.
    utf8 = bmp + '🐵'  # Monkey-face emoji. This requires at least a three-byte encoding.


def dunder_compat(cls):
    if str is bytes:
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


@dunder_compat
class Utf8able:
    """bytes() and decode('UTF-8') is fine, but unicode() will barf"""
    def __bytes__(self):
        return UNICODE.utf8.encode('utf8')


@dunder_compat
class Win1252able:
    """bytes() is fine, but unicode() and decode('UTF-8') will barf"""
    def __bytes__(self):
        return UNICODE.utf8.encode('windows-1252', 'ignore')


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
    unicodable = Unicodable()
    assert UNICODE.utf8 == testfunc(unicodable)


@both_from_funcs
def test_from_funcs_with_utf8able_object(testfunc):

    utf8able = Utf8able()
    assert UNICODE.utf8 == testfunc(utf8able)


def test_from_bytes_with_win1252able_object():
    win1252able = Win1252able()
    assert UNICODE.win1252 == from_bytes(win1252able)


def test_from_utf8_with_win1252():
    win1252 = UNICODE.utf8.encode('windows-1252', 'ignore')
    with pytest.raises(UnicodeDecodeError):
        from_utf8(win1252)


def test_from_utf8_with_win1252able_object():
    win1252able = Win1252able()
    with pytest.raises(UnicodeDecodeError):
        from_utf8(win1252able)


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
    unicodable = Unicodable()
    assert UNICODE.utf8.encode('UTF-8') == testfunc(unicodable)


@both_to_funcs
def test_to_funcs_with_utf8able_object(testfunc):
    utf8able = Utf8able()
    assert UNICODE.utf8.encode('UTF-8') == testfunc(utf8able)


@both_to_funcs
def test_to_funcs_with_win1252able_object(testfunc):
    win1252able = Win1252able()
    assert UNICODE.win1252.encode('windows-1252') == testfunc(win1252able)
