from ftw.workspace.testing import FTW_WORKSPACE_INTEGRATION_TESTING
import doctest
import unittest2 as unittest
from plone.testing import layered

TESTFILES = (
    #'workspace.txt',
    'assignable_users_vocab.txt',
    )


OPTIONFLAGS = (doctest.NORMALIZE_WHITESPACE |
               doctest.ELLIPSIS |
               doctest.REPORT_NDIFF)


def test_suite():

    suite = unittest.TestSuite()

    for testfile in TESTFILES:
        suite.addTests([
              layered(doctest.DocFileSuite(testfile,
                                           optionflags=OPTIONFLAGS),
                      layer=FTW_WORKSPACE_INTEGRATION_TESTING),
          ])

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
