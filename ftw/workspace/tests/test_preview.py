from collective.pdfpeek.interfaces import IPDFDataExtractor
from DateTime import DateTime
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
            'Workspace').allowed_content_types = ('File', 'Image', 'Meeting')

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

    def test_pdf_preview_has_no_image_preview(self):
        file_content = open("{0}/data/test.pdf".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
                       .within(self.workspace)
                       .attach_file_containing(file_content))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='pdf')

        self.assertFalse(adapter.has_image_preview, 'No images yet')

    def test_pdf_preview_full_url_without_pdfpeek(self):
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

    def test_pdf_preview_without_pdfpeek(self):
        file_content = open("{0}/data/test.pdf".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
                       .within(self.workspace)
                       .attach_file_containing(file_content))

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='pdf')

        self.assertIn(
            '<img height="200px" src="{0}" alt="{1}" title="{1}" '
            'data-preview="{2}" />'.format(
                adapter.full_url(),
                'text_no_preview',
                adapter.data_preview_attr()),
            adapter.preview())

    def test_pdf_preview_has_image_preview(self):
        file_content = open("{0}/data/test.pdf".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
                       .within(self.workspace))
        file_.setFile(file_content)

        converter = IPDFDataExtractor(file_)
        converter()

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='pdf')

        self.assertTrue(adapter.has_image_preview,
                        'We should have image previews')

    def test_pdf_preview_full_url_with_pdfpeek(self):
        file_content = open("{0}/data/test.pdf".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
                       .within(self.workspace))
        file_.setFile(file_content)

        converter = IPDFDataExtractor(file_)
        converter()

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='pdf')

        self.assertEquals(
            '{0}/pdf_two_slides_preview'.format(file_.absolute_url()),
            adapter.full_url())

    def test_pdf_preview_with_pdfpeek(self):
        file_content = open("{0}/data/test.pdf".format(
            os.path.split(__file__)[0], 'r'))
        file_ = create(Builder('file')
                       .within(self.workspace))
        file_.setFile(file_content)

        converter = IPDFDataExtractor(file_)
        converter()

        adapter = queryMultiAdapter(
            (file_, file_.REQUEST),
            IWorkspacePreview,
            name='pdf')

        self.assertEquals(
            '<img height="200px" src="{0}/++images++1_thumb" alt="" '
            'title="" data-preview="{1}" />'.format(
                file_.absolute_url(),
                adapter.data_preview_attr()),
            adapter.preview())

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

    def test_ftw_meeting_preview(self):
        meeting = create(Builder('meeting').titled('A meeting')
                         .having(start_date=DateTime('2014/01/01 10:00'))
                         .having(end_date=DateTime('2014/01/01 12:00')))

        adapter = queryMultiAdapter(
            (meeting, meeting.REQUEST),
            IWorkspacePreview,
            name='meeting')

        self.assertEquals('{0}/export_ics'.format(meeting.absolute_url()),
                          adapter.download_url())

        self.assertEquals('html',
                          adapter.preview_type())

        self.assertEquals(meeting.absolute_url(),
                          adapter.full_url())

        self.assertIn('MeetingPreviewWrapper', adapter.preview())
