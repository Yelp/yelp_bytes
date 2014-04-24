import testify as T


class DocTest(T.TestCase):
    def test_docs(self):
        from doctest import testfile, ELLIPSIS
        failures, _ = testfile('README.md', module_relative=False, encoding='UTF-8', optionflags=ELLIPSIS)
        T.assert_equal(failures, 0)
