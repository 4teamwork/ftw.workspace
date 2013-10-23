from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.testing import FTW_WORKSPACE_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase
from zope.component import queryMultiAdapter
from ftw.workspace.interfaces import IWorkspacePreview


class TestPreview(TestCase):

    layer = FTW_WORKSPACE_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace'))
        self.tab = self.workspace.restrictedTraverse(
            '@@tabbedview_view-preview')

        portal.portal_types.get(
            'Workspace').allowed_content_types = ('File, Image')

    def test_get_extension_no_contenttype(self):
        self.assertListEqual([], self.tab.get_extensions(None))

    def test_get_extension_no_mimetype(self):
        self.assertListEqual([], self.tab.get_extensions('dummy/contenttype'))

    def test_get_extension_malformed_mimetype(self):
        self.assertListEqual([], self.tab.get_extensions('dummycontenttype'))

    def test_get_extension_valid_mimetype(self):
        self.assertListEqual(['gif'],
                             list(self.tab.get_extensions('image/gif')))

    def test_get_previews(self):

        create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())

        self.assertGreaterEqual(len(self.tab.get_previews()),
                          1,
                          'Expect at least one adapter')

    def test_gif_preview(self):
        image = create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())

        adapter = queryMultiAdapter(
            (image, image.REQUEST),
            IWorkspacePreview,
            name='gif')

        self.assertTrue(
            adapter.render().startswith(
                '<img src="http://nohost/plone/workspace/image'),
            'Expect an image tag. source should be our image')
