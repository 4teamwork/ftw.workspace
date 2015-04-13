from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from StringIO import StringIO
from unittest2 import TestCase
from zipfile import ZipFile


class TestWorkspaceZipExport(TestCase):

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace')
                                .titled('Workspace')
                                .having(description='Description'))

    @browsing
    def test_zip_export_integration(self, browser):
        browser.login().visit(self.workspace, view='zip_export')

        self.assertEquals('application/zip', browser.headers['Content-Type'])

        zipfile = ZipFile(StringIO(browser.contents))
        self.assertEquals(['workspace.pdf'], zipfile.namelist())
