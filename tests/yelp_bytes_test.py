# -*- coding: utf-8 -*-
import sys

import pytest

from yelp_bytes import to_bytes, to_utf8, from_bytes, from_utf8, text_type


# Define some interesting unicode inputs
class UNICODE:
    ascii = u'A'  # The most basic of unicode.
    latin1 = ascii + u'ü'  # U-umlaut. This is defined in latin1 but not ascii.
    win1252 = latin1 + u'€'  # Euro sign. This is defined in windows-1252, but not latin1.
    bmp = win1252 + u'Ł'  # Polish crossed-L. This requires at least a two-byte encoding.
    utf8 = bmp + u'🐵'  # Monkey-face emoji. This requires at least a three-byte encoding.


class DunderCompat(object):
    # pylint: disable=no-member
    def __str__(self):
        # Dispatch to what str() actually means on this Python version
        try:
            if sys.version_info < (3,):
                return self.__bytes__()
            else:
                return self.__unicode__()
        except AttributeError:
            return super(DunderCompat, self).__str__()


skip_on_py3 = pytest.mark.skipif(
    sys.version_info >= (3,),
    reason="Python 3 str() doesn't fall back to decoding bytes()",
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
    class MyString(text_type):
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
    class Unicodable(DunderCompat):
        def __unicode__(self):
            return UNICODE.utf8

    unicodable = Unicodable()
    assert UNICODE.utf8 == testfunc(unicodable)


@skip_on_py3
@both_from_funcs
def test_with_utf8able_object(testfunc):
    class Utf8able(DunderCompat):
        def __bytes__(self):
            return UNICODE.utf8.encode('utf8')

    utf8able = Utf8able()
    assert UNICODE.utf8 == testfunc(utf8able)


class Win1252able(DunderCompat):
    def __bytes__(self):
        return UNICODE.utf8.encode('windows-1252', 'ignore')


@skip_on_py3
def test_with_win1252able_object():
    win1252able = Win1252able()
    assert UNICODE.win1252 == from_bytes(win1252able)


@skip_on_py3
def test_from_utf8_with_win1252():
    win1252 = UNICODE.utf8.encode('windows-1252', 'ignore')
    with pytest.raises(UnicodeDecodeError):
        from_utf8(win1252)


@skip_on_py3
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
