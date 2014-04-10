# -*- coding: utf-8 -*-
import testify as T

from yelp_bytes.bytes import to_bytes, to_utf8, from_bytes, from_utf8


# Define some interesting unicode inputs
class UNICODE:
    ascii = u'A'  # The most basic of unicode.
    latin1 = ascii + u'ü'  # U-umlaut. This is defined in latin1 but not ascii.
    win1252 = latin1 + u'€'  # Euro sign. This is defined in windows-1252, but not latin1.
    bmp = win1252 + u'Ł'  # Polish crossed-L. This requires at least a two-byte encoding.
    utf8 = bmp + u'🐵'  # Monkey-face emoji. This requires at least a three-byte encoding.


class FromBytesTest(T.TestCase):
    testfunc = staticmethod(from_bytes)

    def test_with_unicode(self):
        # Unicode objects aren't touched.
        T.assert_is(UNICODE.utf8, self.testfunc(UNICODE.utf8))

    def test_with_unicode_subclass(self):
        # Unicode subclasses (eg markupsafe) also go unmolested.
        class MyString(unicode):
            pass
        mystring = MyString("abcdef")
        T.assert_is(mystring, self.testfunc(mystring))

    def test_with_utf8(self):
        utf8 = UNICODE.utf8.encode('utf8')
        T.assert_equal(UNICODE.utf8, self.testfunc(utf8))

    def test_with_win1252(self):
        win1252 = UNICODE.utf8.encode('windows-1252', 'ignore')
        T.assert_equal(UNICODE.win1252.encode('windows-1252'), win1252)
        T.assert_equal(UNICODE.win1252, self.testfunc(win1252))

    def test_with_unicodable_object(self):
        class Unicodable:
            def __unicode__(self):
                return UNICODE.utf8

        unicodable = Unicodable()
        T.assert_equal(UNICODE.utf8, self.testfunc(unicodable))

    def test_with_utf8able_object(self):
        class Utf8able:
            def __str__(self):
                return UNICODE.utf8.encode('utf8')

        utf8able = Utf8able()
        T.assert_equal(UNICODE.utf8, self.testfunc(utf8able))

    def test_with_win1252able_object(self):
        class Win1252able:
            def __str__(self):
                return UNICODE.utf8.encode('windows-1252', 'ignore')

        win1252able = Win1252able()
        T.assert_equal(UNICODE.win1252, self.testfunc(win1252able))


class FromUtf8Test(FromBytesTest):
    testfunc = staticmethod(from_utf8)

    def test_with_win1252(self):
        win1252 = UNICODE.utf8.encode('windows-1252', 'ignore')
        T.assert_raises(UnicodeDecodeError, self.testfunc, win1252)

    def test_with_win1252able_object(self):
        class Win1252able:
            def __str__(self):
                return UNICODE.utf8.encode('windows-1252', 'ignore')

        win1252able = Win1252able()
        T.assert_raises(UnicodeDecodeError, self.testfunc, win1252able)


class ToBytesTest(T.TestCase):
    testfunc = staticmethod(to_bytes)

    def test_to_bytes_from_unicode(self):
        T.assert_equal(UNICODE.utf8.encode('utf8'), self.testfunc(UNICODE.utf8))

    def test_to_bytes_from_utf8(self):
        utf8 = UNICODE.utf8.encode('utf8')
        T.assert_equal(utf8, self.testfunc(utf8))

    def test_to_bytes_from_bad_utf8(self):
        # The to_bytes function doesn't attempt to auto-magically fix non-utf8 encodings.
        win1252 = UNICODE.utf8.encode('windows-1252', 'ignore')
        T.assert_equal(UNICODE.win1252.encode('windows-1252'), win1252)
        T.assert_equal(win1252, self.testfunc(win1252))


class ToUtf8Test(ToBytesTest):
    # to_utf8 will behave essentially the same as to_bytes.
    testfunc = staticmethod(to_utf8)


if __name__ == '__main__':
    T.run()
