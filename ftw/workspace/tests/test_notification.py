from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browser
from ftw.testbrowser import browsing
from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase


class TestFtwNotificationIntegration(TestCase):

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace').titled('Workspace'))

    @browsing
    def test_notification_action_on_workspace(self, browser):
        self.assert_notification_action(self.workspace)

    @browsing
    def test_notification_action_on_tabbedviewfolder(self, browser):
        folder = create(Builder('TabbedViewFolder').within(self.workspace))
        self.assert_notification_action(folder)

    @browsing
    def test_notification_action_on_file(self, browser):
        file_ = create(Builder('file').within(self.workspace))
        self.assert_notification_action(file_)

    def assert_notification_action(self, obj):
        browser.login().visit(obj)
        self.assertEquals(
            'Notification',
            browser.css('#plone-contentmenu-actions-notification').first.text)
