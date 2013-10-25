from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.interfaces import IWorkspacePreview
from ftw.workspace.testing import FTW_WORKSPACE_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from pyquery import PyQuery
from unittest2 import TestCase
from zope.component import queryMultiAdapter


class TestPreview(TestCase):

    layer = FTW_WORKSPACE_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace'))
        self.tab = self.workspace.restrictedTraverse(
           '@@tabbedview_view-documents')

        portal.portal_types.get(
            'Workspace').allowed_content_types = ('File, Image')

    def test_show_pills_on_document_tab(self):
        create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())

        doc = PyQuery(self.tab())
        self.assertTrue(doc('.ViewChooser'))
