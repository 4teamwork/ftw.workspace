from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from unittest2 import TestCase
from xlrd import open_workbook
from zipfile import ZipFile
import transaction


class TestWorkspaceZipExport(TestCase):

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.user = create(Builder('user')
                           .named('may', 'exists')
                           .with_roles('Manager'))

        login(self.portal, self.user.getId())

        self.workspace = create(Builder('workspace')
                                .titled('Workspace')
                                .having(description='Description'))

        create(Builder('user')
               .named('Hugo', 'Boss')
               .with_roles('Editor', on=self.workspace))

    def get_zip_content(self, browser):
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
        return data

    @browsing
    def test_zip_export_action_is_available(self, browser):
        browser.login().visit(self.workspace)
        self.assertEquals(
            'Export as Zip',
            browser.css('#plone-contentmenu-actions-zipexport').first.text,
            'Expect the zip export action on workspace')

    @browsing
    def test_zip_export_integration(self, browser):
        """
        Makes sure the zip file contains a spreadsheet with the correct
        participants.
        """

        data = self.get_zip_content(browser)
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
                    u'E-Mail': u'may@exists.com',
                    u'User ID': u'may.exists',
                    u'Full name': u'Exists May',
                    u'Roles': u'Owner, Contributor, Editor, Reader'
                },
            ],
            second=data
        )

    @browsing
    def test_zip_export_works_if_owner_no_longer_exists(self, browser):
        """
        Makes sure the zip file contains a spreadsheet with the correct
        participants.
        """

        # Remove owner of Workspace
        mtool = getToolByName(self.portal, 'portal_membership')
        mtool.deleteMembers((self.user.getId(),))
        transaction.commit()

        data = self.get_zip_content(browser)

        self.maxDiff = None
        self.assertEquals(
            first=[
                {
                    u'E-Mail': u'hugo@boss.com',
                    u'User ID': u'hugo.boss',
                    u'Full name': u'Boss Hugo',
                    u'Roles': u'Editor'
                },
            ],
            second=data
        )
