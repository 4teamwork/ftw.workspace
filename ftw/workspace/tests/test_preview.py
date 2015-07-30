from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.interfaces import IWorkspacePreview
from ftw.workspace.testing import FTW_WORKSPACE_BUMBLEBEE_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from pyquery import PyQuery
from unittest2 import TestCase
from zope.component import queryMultiAdapter
from ftw.testbrowser import browsing
import os


class TestPreview(TestCase):

    layer = FTW_WORKSPACE_BUMBLEBEE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace'))

        self.portal.portal_types.get(
            'Workspace').allowed_content_types = ('File', 'Image')

        self.bumble1 = create(Builder('file').titled("ein blatt Papier").within(self.workspace))
        self.bumble2 = create(Builder('file').within(self.workspace))
        self.bumble3 = create(Builder('file').within(self.workspace))
        self.nobumble = create(Builder('image').within(self.workspace))

    @browsing
    def test_only_bumblebeeable_displayed(self, browser):
        page = browser.login().visit(self.workspace, view='tabbedview_view-documents')
        self.assertEqual(3, len(page.css('.previewitem')))

    @browsing
    def test_filtering_works(self, browser):
        page = browser.login().visit(self.workspace, view='tabbedview_view-documents', data={'searchable_text':"bla"})
        self.assertEqual(1, len(page.css('.previewitem')))
        self.assertEqual("ein blatt Papier", page.css('.previewitem').first.text)
