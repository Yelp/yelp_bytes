# yelp_bytes

[![Build Status](https://travis-ci.org/Yelp/yelp_bytes.svg?branch=master)](https://travis-ci.org/Yelp/yelp\_bytes)
[![Coverage Status](https://img.shields.io/coveralls/Yelp/yelp_bytes.svg?branch=master)](https://coveralls.io/r/Yelp/yelp\_bytes?branch=master)

`yelp_bytes` contains several utility functions to help ensure that the data you're using is always either Unicode or
byte strings, taking care of the edge cases for you so that you don't have to worry about them. We handle ambiguous
bytestrings by leveraging our our ["internet" encoding](https://github.com/Yelp/yelp_encodings). This allows you to
write functions that need unicode but can accept arbitrary values without crashing.


## Installation

For a primer on pip and virtualenv, see the [Python Packaging User Guide](
https://python-packaging-user-guide.readthedocs.org/en/latest/tutorial.html).

TL;DR: `pip install yelp_bytes`

## Usage

The `from_bytes` function is the most interesting one. It takes an object and returns its unicode representation.
This function never fails, except for extremely rare edge cases (that we haven't ourselves encountered).  `from_utf8` is
similar, but uses 'UTF-8' rather than 'internet' encoding, and so will fail if given poorly-encoded bytes. `to_bytes`
and `to_utf8` both take an object and return its UTF-8 bytestring representation.

    python
    >>> import yelp_bytes

    >>> euro = u'€'

    >>> print(yelp_bytes.from_bytes(euro.encode('UTF-8')))
    €
    >>> print(yelp_bytes.from_bytes(euro.encode('cp1252')))
    €
    >>> print(yelp_bytes.from_bytes(euro))
    €


We also handle objects with (certain common classes of) encoding issues, and all the other various edge cases we've
encountered. One of the more common is putting non-ascii unicode into an error message:

    python
    >>> error = Exception(euro)
    >>> print(error)
    Traceback (most recent call last):
        ...
    UnicodeEncodeError: 'ascii' codec can't encode character u'\u20ac' in position 0: ordinal not in range(128)

    >>> print(yelp_bytes.from_utf8(error))
    €
    >>> yelp_bytes.to_utf8(error) == euro.encode('UTF-8')
    True


Check out [the source](https://github.com/Yelp/yelp_bytes/blob/HEAD/yelp_bytes.py) to learn more about the input parameters and return values.
