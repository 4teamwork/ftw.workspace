from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.table.helper import readable_date_text
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
        self.previews = self.workspace.restrictedTraverse(
            '@@previews')

        portal.portal_types.get(
            'Workspace').allowed_content_types = ('File, Image')

    def test_get_extension_no_contenttype(self):
        self.assertListEqual([], self.previews.get_extensions(None))

    def test_get_extension_no_mimetype(self):
        self.assertListEqual([],
                             self.previews.get_extensions('dummy/contenttype'))

    def test_get_extension_malformed_mimetype(self):
        self.assertListEqual([],
                             self.previews.get_extensions('dummycontenttype'))

    def test_get_extension_valid_mimetype(self):
        self.assertListEqual(['gif'],
                             list(self.previews.get_extensions('image/gif')))

    def test_get_previews(self):

        create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())

        self.assertGreaterEqual(len(self.previews.get_previews()),
                                1,
                               'Expect at least one adapter')

    def test_default_preview(self):
        file_ = create(Builder('file')
            .within(self.workspace)
            .with_dummy_content())

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview)

        self.assertIn('default.jpeg', adapter.preview())

    def test_gif_preview(self):
        image = create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())

        adapter = queryMultiAdapter(
            (image, image.REQUEST),
            IWorkspacePreview,
            name='gif')

        self.assertTrue(
            adapter.preview().startswith(
                '<img src="http://nohost/plone/workspace/image'),
            'Expect an image tag. source should be our image')

    def test_gif_full_url(self):
        image = create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())

        adapter = queryMultiAdapter(
            (image, image.REQUEST),
            IWorkspacePreview,
            name='gif')

        self.assertEquals(image.absolute_url() + '/image_large',
                         adapter.full_url())

    def test_gif_scale_properties(self):
        image = create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())

        adapter = queryMultiAdapter(
            (image, image.REQUEST),
            IWorkspacePreview,
            name='gif')

        self.assertEquals((200, 200), adapter.get_scale_properties())

    def test_tab_renders(self):
        create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())

        doc = PyQuery(self.workspace.restrictedTraverse(
            '@@tabbedview_view-preview')())

        self.assertTrue(doc('.previewContainer .colorboxLink img'),
                            'There should be an image')

    def test_ftwfile_gif_preview(self):
        image = ('GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00'
                '\x00!\xf9\x04\x04\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00'
                '\x01\x00\x00\x02\x02D\x01\x00;')

        file_ = create(Builder('file')
            .within(self.workspace)
            .attach_file_containing(image))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='gif')

        self.assertTrue(
            adapter.preview().startswith(
                '<img src="http://nohost/plone/workspace/file'),
            'Expect an image tag. source should be our image')

        self.assertEquals((200, 200), adapter.get_scale_properties())

    def test_default_preview_grouped_result(self):
        image1 = create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())
        image2 = create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())
        image3 = create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())

        for obj in [image2, image3]:
            obj.setModificationDate(DateTime('2013-01-01'))
            obj.reindexObject(idxs='modified')

        def groupbymodifieddate(item):
            return readable_date_text(item, item.modified)

        keys, groups = self.tab.group(keyfunc=groupbymodifieddate)

        self.assertListEqual(['heute', '01.01.2013'], keys)

        self.assertEquals(1, len(groups[0]), "Expect one items in 1. group")
        self.assertEquals(2, len(groups[1]), "Expect two items in 2. group")

        self.assertIn(image1.getId(), [x.context.getId() for x in groups[0]])

        self.assertIn(image2.getId(), [x.context.getId() for x in groups[1]])
        self.assertIn(image2.getId(), [x.context.getId() for x in groups[1]])

    def test_preview_invalid_groupby(self):
        with self.assertRaises(TypeError):
            self.tab.group(keyfunc='id')

        with self.assertRaises(TypeError):
            self.tab.group(keyfunc=None)
