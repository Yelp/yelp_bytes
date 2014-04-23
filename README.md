# yelp_bytes

yelp_bytes contains several utility functions to help ensure that the data you're using is always either Unicode or byte strings, taking care of the edge cases for you so that you don't have to worry about them. We do all of this by leveraging our [yelp_encodings](https://github.com/Yelp/yelp_encodings) library to handle the encoding and decoding of data to and from Unicode.

## Installation

Installation is easy with ``pip``! The package lives on PyPI so all you have to do is run

```
$ pip install yelp_bytes
```

And you're off!

## Usage

All you need to do is import yelp_bytes into your code.

```
import yelp_bytes

yelp_bytes.to_utf8('Hello world!')  # => 'Hello World!'
yelp_bytes.to_bytes('Hello world!') # => 'Hello World!'

yelp_bytes.from_utf8('Hello world!')  # => u'Hello World!'
yelp_bytes.from_bytes('Hello world!') # => u'Hello World'
```

You have four functions available to you:

1. ``to_bytes`` encodes to utf-8 bytestrings
2. ``from_bytes`` decodes values to unambiguous unicode characters
3. ``to_utf8`` encodes unicode text to utf-8 bytes
4. ``from_utf8`` decodes utf-8 bytes to unicode text

Check out the source to learn more about the input parameters and return values.
