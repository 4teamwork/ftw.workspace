from ftw.builder import Builder
from ftw.builder import create
from ftw.participation.interfaces import IParticipationSupport
from ftw.testbrowser import browsing
from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase


class TestFtwParticipationIntegration(TestCase):

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace').titled('Workspace'))

    @browsing
    def test_tab(self, browser):
        browser.login().visit(self.workspace)
        self.assertEquals('participants',
                          browser.css('#tab-participants').first.text,
                          'Expect the participation tab on workspaces.')

    def test_participation_support_on_workspace(self):
        self.assertTrue(IParticipationSupport.providedBy(self.workspace),
                        'No participation support found :-(')
