from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.interfaces import IWorkspacePreview
from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
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

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

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

    def test_item_for_brain(self):
        catalog = self.portal.portal_catalog
        catalog.addColumn('bumblebee_checksum')
        catalog.addColumn('getContentType')

        brains = catalog(UID=self.bumble1.UID())
        brain = brains[0]
        brain.__setitem__('bumblebee_checksum', 'def332dde323332decccaa3349505')
        brain.__setitem__('getContentType', 'application/msword')

        view = self.portal.restrictedTraverse('/'.join(self.workspace.getPhysicalPath()) + '/tabbedview_view-documents')
        results = view.item_for_brain(brain)
        self.assertEqual(results['title'], 'ein blatt Papier')
        self.assertEqual(results['details_url'], 'http://nohost/plone/workspace/ein-blatt-papier/view')
        self.assertEqual(results['overlay_url'], 'http://nohost/plone/workspace/ein-blatt-papier/file_preview')
        self.assertEqual(results['mimetype_image_url'], 'http://nohost/plone/doc.png')
        self.assertEqual(results['mimetype_title'], 'Microsoft Word Document')
