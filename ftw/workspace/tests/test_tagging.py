from ftw.builder import Builder
from ftw.builder import create
from ftw.tagging.interfaces.tagging import ITaggable
from ftw.workspace.testing import FTW_WORKSPACE_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase


class TestTagging(TestCase):

    layer = FTW_WORKSPACE_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace'))
        self.file = create(Builder('file')
            .within(self.workspace))

    def test_files_can_be_tagged(self):
        import pdb; pdb.set_trace()
        self.assertTrue(ITaggable.providedBy(self.file))

    def test_tagcloud_portlet_is_displayed_and_shows_tags(self):
        import pdb; pdb.set_trace()
