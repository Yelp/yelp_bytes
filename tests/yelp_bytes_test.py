# -*- coding: utf-8 -*-
import pytest

from yelp_bytes import to_bytes, to_utf8, from_bytes, from_utf8


# Define some interesting unicode inputs
class UNICODE:
    ascii = u'A'  # The most basic of unicode.
    latin1 = ascii + u'ü'  # U-umlaut. This is defined in latin1 but not ascii.
    win1252 = latin1 + u'€'  # Euro sign. This is defined in windows-1252, but not latin1.
    bmp = win1252 + u'Ł'  # Polish crossed-L. This requires at least a two-byte encoding.
    utf8 = bmp + u'🐵'  # Monkey-face emoji. This requires at least a three-byte encoding.


both_from_funcs = pytest.mark.parametrize('testfunc', (from_bytes, from_utf8))
both_to_funcs = pytest.mark.parametrize('testfunc', (to_bytes, to_utf8))


@both_from_funcs
def test_with_unicode(testfunc):
    # Unicode objects aren't touched.
    assert UNICODE.utf8 is testfunc(UNICODE.utf8)


@both_from_funcs
def test_with_unicode_subclass(testfunc):
    # Unicode subclasses (eg markupsafe) also go unmolested.
    class MyString(unicode):
        pass
    mystring = MyString("abcdef")
    assert mystring is testfunc(mystring)


@both_from_funcs
def test_with_utf8(testfunc):
    utf8 = UNICODE.utf8.encode('utf8')
    assert UNICODE.utf8 == testfunc(utf8)


def test_with_win1252():
    win1252 = UNICODE.utf8.encode('windows-1252', 'ignore')
    assert UNICODE.win1252.encode('windows-1252') == win1252
    assert UNICODE.win1252 == from_bytes(win1252)


@both_from_funcs
def test_with_unicodable_object(testfunc):
    class Unicodable:
        def __unicode__(self):
            return UNICODE.utf8

    unicodable = Unicodable()
    assert UNICODE.utf8 == testfunc(unicodable)


@both_from_funcs
def test_with_utf8able_object(testfunc):
    class Utf8able:
        def __str__(self):
            return UNICODE.utf8.encode('utf8')

    utf8able = Utf8able()
    assert UNICODE.utf8 == testfunc(utf8able)


def test_with_win1252able_object():
    class Win1252able:
        def __str__(self):
            return UNICODE.utf8.encode('windows-1252', 'ignore')

    win1252able = Win1252able()
    assert UNICODE.win1252 == from_bytes(win1252able)


def test_from_utf8_with_win1252():
    win1252 = UNICODE.utf8.encode('windows-1252', 'ignore')
    with pytest.raises(UnicodeDecodeError):
        from_utf8(win1252)


def test_from_utf8_with_win1252able_object():
    class Win1252able:
        def __str__(self):
            return UNICODE.utf8.encode('windows-1252', 'ignore')

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
