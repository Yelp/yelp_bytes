def test_docs():
    from doctest import testfile, ELLIPSIS
    failures, _ = testfile(
        'README.md',
        module_relative=False,
        encoding='UTF-8',
        optionflags=ELLIPSIS,
    )
    assert failures == 0
