from DateTime import DateTime
from ftw.pdfgenerator.interfaces import IBuilder
from ftw.pdfgenerator.interfaces import ILaTeXView
from ftw.testing import MockTestCase
from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.interfaces import IWorkspaceDetailsListingProvider
from ftw.workspace.latex.layout import WorkspaceLayout
from ftw.workspace.latex.views import FilesListing
from ftw.workspace.latex.views import WorkspaceDetailsView
from ftw.workspace.testing import LATEX_ZCML_LAYER
from mocker import ANY
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass


class ListingTestBase(MockTestCase):

    def setUp(self):
        MockTestCase.setUp(self)

        self.context = self.providing_stub(IWorkspace)
        self.expect(self.context.getPhysicalPath()).result(
            ['', 'path', 'to', 'workspace'])
        self.expect(self.context.getOwner(0).getId()).result('john.doe')

        self.response = self.stub()
        self.expect(self.response.getHeader(ANY))
        self.expect(self.response.setHeader(ANY, ANY))
        self.request = self.create_dummy(debug=True,
                                         response=self.response)

        self.builder = self.stub_interface(IBuilder)
        self.layout = WorkspaceLayout(
            self.context, self.request, self.builder)
        self.view = WorkspaceDetailsView(
            self.context, self.request, self.layout)

        portal_catalog = self.stub()
        self.mock_tool(portal_catalog, 'portal_catalog')
        self.brains = []
        self.expect(portal_catalog({'path': '/path/to/workspace',
                                    'portal_type': ['File'],
                                    'sort_on': 'created',
                                    'sort_order': 'reverse'})).call(
            lambda q: self.brains)

        acl_users = self.stub()
        self.mock_tool(acl_users, 'acl_users')
        self.expect(acl_users.getUserById('john.doe').getProperty(
                'fullname', 'john.doe')).result('John Doe')



class TestWorkspaceDetailsView(ListingTestBase):

    layer = LATEX_ZCML_LAYER

    def test_component_is_registered(self):
        self.replay()
        view = getMultiAdapter((self.context, self.request, self.layout),
                               ILaTeXView)
        self.assertEqual(type(view), WorkspaceDetailsView)

    def test_implements_interface(self):
        self.replay()
        self.assertTrue(ILaTeXView.implementedBy(WorkspaceDetailsView))
        verifyClass(ILaTeXView, WorkspaceDetailsView)

    def test_metadata_in_view(self):
        self.expect(self.context.Title()).result('johns workspace')
        self.expect(self.context.Description()).result('this is my workspace')
        self.expect(self.context.getText()).result('the long description')

        self.replay()

        view = getMultiAdapter((self.context, self.request, self.layout),
                               ILaTeXView)
        latex = view.render()

        self.assertIn('johns workspace', latex)
        self.assertIn('this is my workspace', latex)
        self.assertIn('the long description', latex)
        self.assertIn('John Doe', latex)

    def test_full_rendering(self):
        self.brains = [
            self.create_dummy(Title='my document',
                              effective=DateTime('05/23/2010'),
                              modified=DateTime('06/10/2010'),
                              Creator='john.doe')]

        self.expect(self.context.Title()).result('johns workspace')
        self.expect(self.context.Description()).result('this is my workspace')
        self.expect(self.context.getText()).result('the long description')

        self.replay()

        view = getMultiAdapter((self.context, self.request, self.layout),
                               ILaTeXView)
        latex = view.render()

        self.assertIn('johns workspace', latex)
        self.assertIn('my document', latex)


class TestFilesListing(ListingTestBase):

    layer = LATEX_ZCML_LAYER

    def test_component_is_registered(self):
        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='files-listing')

        self.assertEqual(type(listing), FilesListing)

    def test_implements_interface(self):
        self.replay()
        self.assertTrue(IWorkspaceDetailsListingProvider.implementedBy(
                FilesListing))

        verifyClass(IWorkspaceDetailsListingProvider, FilesListing)

    def test_get_sort_key(self):
        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='files-listing')
        self.assertEqual(listing.get_sort_key(), 10)

    def test_get_title(self):
        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='files-listing')
        self.assertEqual(listing.get_title(), 'Files')

    def test_get_items(self):
        self.brains = [
            self.create_dummy(Title='foo',
                              effective=DateTime('05/23/2010'),
                              modified=DateTime('06/10/2010'),
                              Creator='john.doe')]

        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='files-listing')

        self.assertEqual(list(listing.get_items()), [
                {'title': 'foo',
                 'effective': '23.05.2010',
                 'modified': '10.06.2010',
                 'creator': 'John Doe'}])

    def test_rendering(self):
        self.brains = [
            self.create_dummy(Title='foo',
                              effective=DateTime('05/23/2010'),
                              modified=DateTime('06/10/2010'),
                              Creator='john.doe')]

        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='files-listing')

        latex = listing.get_listing()
        self.assertIn(r'\begin{tabular}', latex)
        self.assertIn(r'foo', latex)
        self.assertIn(r'23.05.2010', latex)
        self.assertIn(r'10.06.2010', latex)
        self.assertIn(r'John Doe', latex)
