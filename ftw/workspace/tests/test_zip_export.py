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
from xlrd import open_workbook
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
        """
        Makes sure the zip file contains a spreadsheet with the correct
        participants.
        """
        create(Builder('user')
               .named('Hugo', 'Boss')
               .with_roles('Editor', on=self.workspace))

        browser.login().visit(self.workspace, view='zip_export')

        self.assertEquals('application/zip', browser.headers['Content-Type'])

        zipfile = ZipFile(StringIO(browser.contents))
        self.assertEquals(['workspace.pdf', 'participants.xlsx'], 
                          zipfile.namelist())

        xlsx = zipfile.read('participants.xlsx')

        workbook = open_workbook(file_contents=xlsx)
        sheet = workbook.sheet_by_index(0)

        data = map(sheet.row_values, range(sheet.nrows))
        headers = data.pop(0)
        data = map(
            lambda row: dict(zip(headers, row)),
            data
        )
        self.maxDiff = None
        self.assertEquals(
            first=[
                {
                    u'E-Mail': u'hugo@boss.com',
                    u'User ID': u'hugo.boss',
                    u'Full name': u'Boss Hugo',
                    u'Roles': u'Editor'
                },
                {
                    u'E-Mail': u'',
                    u'User ID': u'test_user_1_',
                    u'Full name': u'test_user_1_',
                    u'Roles': u'Owner, Contributor, Editor, Reader'
                },
            ],
            second=data
        )
