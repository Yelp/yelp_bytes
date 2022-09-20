import sys

import doctest
import pytest


@pytest.mark.skipif(
    sys.version_info >= (3,),
    reason="Python 3 doesn't have the UnicodeEncodeError problem",
)
def test_docs():
    failures, _ = doctest.testfile(
        'README.md',
        module_relative=False,
        encoding='UTF-8',
        optionflags=doctest.ELLIPSIS,
    )
    assert failures == 0
