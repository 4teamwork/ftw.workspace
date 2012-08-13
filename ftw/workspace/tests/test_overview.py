from ftw.testing import MockTestCase
from ftw.workspace.browser.overview import OverviewTab
from ftw.workspace.testing import OVERVIEW_LAYER
from mocker import ANY
from mocker import Mocker


class TestOverview(MockTestCase):

    layer = OVERVIEW_LAYER

    def setUp(self):
        self.searchable_text = ''
        self.search_text_in_request = False

        self.request = self.stub()
        self.response = self.stub()
        self.expect(self.request.response).result(self.response)
        self.expect(self.request.RESPONSE).result(self.response)

        self.expect(self.response.getHeader("Content-Type")).result('')
        self.expect(self.response.setHeader("Content-Type", ANY)).result(None)

        self.expect('searchable_text' in self.request).call(
            lambda: self.search_text_in_request)
        self.expect(self.request.get('searchable_text')).call(
            lambda k: self.search_text_in_request and self.searchable_text)
        self.expect(self.request.get('searchable_text', None)).call(
            lambda k, d: self.search_text_in_request and self.searchable_text)

        self.expect(self.request.get('pagenumber', 1)).result(1)
        self.expect(self.request.debug).result(True)
        self.expect(self.request.get('sort', ANY)).call(lambda k, d: d)
        self.expect(self.request.get('dir', ANY)).call(lambda k, d: d)
        self.expect(self.request.get('groupBy', ANY)).call(lambda k, d: d)

        self.context = self.stub()
        self.expect(self.context.portal_type).result('Workspace')
        self.expect(self.context.absolute_url()).result('http://nohost/plone')
        self.expect(self.context.getPhysicalPath()).result(['', 'plone'])
        self.expect(self.context.portal_catalog(ANY)).result([])
        self.expect(self.context.aq_explicit).result(self.context)
        self.expect(self.context.__parent__).result(None)
        self.expect(self.context.Description).result(
            lambda: 'MOCK ALL THE THINGS')
        schema = self.stub()
        self.expect(self.context.Schema()).result(schema)
        self.expect(schema.getField('text').get(self.context)).result(
            'THE TEXT')

        self.testcase_mocker = Mocker()

        self.overview = OverviewTab(self.context, self.request)
        self.overview._table_source = self.testcase_mocker.mock()
        self.overview._table_source.search_results(ANY)
        self.testcase_mocker.result([])
        self.testcase_mocker.count(0, None)

        self.overview.table_source.build_query()
        self.testcase_mocker.result('')
        self.testcase_mocker.count(0, None)

        self.overview.table_source.custom_sort()
        self.testcase_mocker.result('')
        self.testcase_mocker.count(0, None)

        self.overview.__name__
        self.testcase_mocker.result('tabbedview_view-overview')
        self.testcase_mocker.count(0, None)

        # self.obj = self.testcase_mocker.proxy(self.overview)

        self.testcase_mocker.replay()

    def tearDown(self):
        self.testcase_mocker.verify()
        self.testcase_mocker.restore()

    def test_overview(self):
        self.replay()
        self.searchable_text = ''
        self.search_text_in_request = False
        self.overview.update()
        self.assertEqual(self.overview.show_search_results(), False)
        testhtml = "MOCK ALL THE THINGS"
        template = self.overview.template()
        self.assertEqual(testhtml in template, True)

    def test_second_overview(self):
        self.replay()
        self.searchable_text = 'Test'
        self.search_text_in_request = True
        self.overview.update()
        self.assertEqual(self.overview.show_search_results(), True)
        testhtml = ''
        template = self.overview.template()
        self.assertEqual(testhtml in template, True)
