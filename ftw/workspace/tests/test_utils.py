from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
from ftw.workspace.utils import item_for_brain
from unittest2 import TestCase
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME


class TestItemForBrain(TestCase):

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace'))

        self.portal.portal_types.get(
            'Workspace').allowed_content_types = ('File')

        self.bumble1 = create(
            Builder('file').titled("ein blatt Papier").within(self.workspace))

    def test_item_for_brain(self):
        catalog = self.portal.portal_catalog
        catalog.addColumn('bumblebee_checksum')
        catalog.addColumn('getContentType')

        brains = catalog(UID=self.bumble1.UID())
        brain = brains[0]
        brain.__setitem__(
            'bumblebee_checksum', 'def332dde323332decccaa3349505')
        brain.__setitem__('getContentType', 'application/msword')

        results = item_for_brain(brain)

        self.assertEqual(
            results['title'], 'ein blatt Papier')
        self.assertEqual(
            results['details_url'],
            'http://nohost/plone/workspace/ein-blatt-papier/view')
        self.assertEqual(
            results['overlay_url'],
            'http://nohost/plone/workspace/ein-blatt-papier/file_preview')
        self.assertEqual(
            results['mimetype_image_url'], 'http://nohost/plone/doc.png')
        self.assertEqual(
            results['mimetype_title'], 'Microsoft Word Document')
