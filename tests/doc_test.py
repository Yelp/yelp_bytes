import sys

import pytest


@pytest.mark.skipif(
    sys.version_info >= (3,),
    reason="Python 3 doesn't have the UnicodeEncodeError problem",
)
def test_docs():
    from doctest import testfile, ELLIPSIS
    failures, _ = testfile(
        'README.md',
        module_relative=False,
        encoding='UTF-8',
        optionflags=ELLIPSIS,
    )
    assert failures == 0
