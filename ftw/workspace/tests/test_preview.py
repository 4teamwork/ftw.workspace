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
import os


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
            'Workspace').allowed_content_types = ('File', 'Image')

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

        self.assertIn('default.png', adapter.preview())

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

        self.assertEquals(image.absolute_url() + '/images/image',
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

    def test_default_preview_query(self):
        query = self.previews._query()

        path = '/'.join(self.workspace.getPhysicalPath())
        self.assertEquals(path, query['path'])

        self.assertEquals('modified', query['sort_on'])
        self.assertEquals('descending', query['sort_order'])

    def test_default_get_group_information(self):
        image = create(Builder('image')
            .within(self.workspace)
            .with_dummy_content())
        adapter = queryMultiAdapter(
            (image, image.REQUEST),
            IWorkspacePreview,
            name='gif')

        self.assertEquals('heute',
                          self.previews.get_group_information(adapter))

    def test_doc_preview_full_url(self):
        file_content = open("{0}/data/test.doc".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
            .within(self.workspace)
            .attach_file_containing(file_content))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='doc')

        self.assertIn('doc.png', adapter.full_url())

    def test_docx_preview_full_url(self):
        file_content = open("{0}/data/test.docx".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
            .within(self.workspace)
            .attach_file_containing(file_content))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='docx')

        self.assertIn('docx.png', adapter.full_url())

    def test_ppt_preview_full_url(self):
        file_content = open("{0}/data/test.ppt".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
            .within(self.workspace)
            .attach_file_containing(file_content))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='ppt')

        self.assertIn('ppt.png', adapter.full_url())

    def test_pptx_preview_full_url(self):
        file_content = open("{0}/data/test.pptx".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
            .within(self.workspace)
            .attach_file_containing(file_content))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='pptx')

        self.assertIn('pptx.png', adapter.full_url())

    def test_xls_preview_full_url(self):
        file_content = open("{0}/data/test.xls".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
            .within(self.workspace)
            .attach_file_containing(file_content))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='xls')

        self.assertIn('xls.png', adapter.full_url())

    def test_xlsx_preview_full_url(self):
        file_content = open("{0}/data/test.xlsx".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
            .within(self.workspace)
            .attach_file_containing(file_content))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='xlsx')

        self.assertIn('xlsx.png', adapter.full_url())

    def test_pdf_preview_full_url(self):
        file_content = open("{0}/data/test.pdf".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
            .within(self.workspace)
            .attach_file_containing(file_content))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='pdf')

        self.assertIn('pdf.png', adapter.full_url())

    def test_zip_preview_full_url(self):
        file_content = open("{0}/data/test.zip".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
            .within(self.workspace)
            .attach_file_containing(file_content))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='zip')

        self.assertIn('zip.png', adapter.full_url())

    def test_txt_preview_full_url(self):
        file_content = open("{0}/data/test.txt".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
            .within(self.workspace)
            .attach_file_containing(file_content))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='txt')

        self.assertIn('txt.png', adapter.full_url())
