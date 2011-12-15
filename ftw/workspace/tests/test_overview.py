from plone.mocktestcase import MockTestCase
from mocker import Mocker
from mocker import ANY
from plone.registry.interfaces import IRegistry
from ftw.workspace.browser.overview import OverviewTab
from zope.component import provideUtility
from ftw.workspace.testing import OVERVIEW_LAYER


class TestOverview(MockTestCase):

    layer = OVERVIEW_LAYER

    # def st_in_request(self):
    #     return self.search_text_in_request
    def setUp(self):
        self.search_text_in_request = False
        self.registry_mocker = Mocker()
        registry = self.registry_mocker.mock()
        provideUtility(provides=IRegistry, component=registry)
        registry['ftw.tabbedview.interfaces.ITabbedView.batch_size']
        self.registry_mocker.result(20)
        self.registry_mocker.count(0, None)

        registry['ftw.tabbedview.interfaces.ITabbedView.extjs_enabled']
        self.registry_mocker.result(False)
        self.registry_mocker.count(0, None)

        request = self.registry_mocker.mock()

        request.response.getHeader("Content-Type")
        self.registry_mocker.result('')
        self.registry_mocker.count(0, None)
        request.response.setHeader("Content-Type", ANY)
        self.registry_mocker.result(None)
        self.registry_mocker.count(0, None)

        self.searchable_text = ''
        request.get('pagenumber', 1)
        self.registry_mocker.result(1)
        self.registry_mocker.count(0, None)

        request.get(ANY, ANY)
        self.registry_mocker.result('')
        self.registry_mocker.count(0, None)

        request.get('searchable_text')
        self.registry_mocker.call(lambda key: self.searchable_text)
        self.registry_mocker.count(0, None)

        request.get('sort', 'modified')
        self.registry_mocker.result('modified')
        self.registry_mocker.count(0, None)

        request.debug
        self.registry_mocker.result(True)
        self.registry_mocker.count(0, None)

        request.get('dir', 'reverse')
        self.registry_mocker.result('reverse')
        self.registry_mocker.count(0, None)

        request.get('searchable_text', None)
        self.registry_mocker.call(lambda s, k: self.search_text_in_request)
        self.registry_mocker.count(0, None)

        context = self.registry_mocker.mock()
        context.absolute_url()
        self.registry_mocker.result('http://nohost/plone')
        self.registry_mocker.count(0, None)

        context.absolute_url.__call__
        self.registry_mocker.result('http://nohost/plone')
        self.registry_mocker.count(0, None)

        context.getPhysicalPath()
        self.registry_mocker.result(('', 'plone'))
        self.registry_mocker.count(0, None)

        context.portal_catalog(ANY)
        self.registry_mocker.result([])
        self.registry_mocker.count(0, None)

        context.aq_explicit
        self.registry_mocker.result(context)
        self.registry_mocker.count(0, None)

        context.Description
        self.registry_mocker.result('MOCK ALL THE THINGS')
        self.registry_mocker.count(0, None)

        context.getText
        self.registry_mocker.result('')
        self.registry_mocker.count(0, None)


        self.registry_mocker.replay()

        self.testcase_mocker = Mocker()

        self.overview = OverviewTab(context, request)
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
        self.registry_mocker.verify()
        self.registry_mocker.restore()

    def test_overview(self):

        self.searchable_text = ''
        self.search_text_in_request = False
        self.overview.update()
        self.assertEqual(self.overview.show_search_results, False)
        testhtml = "MOCK ALL THE THINGS"
        template = self.overview.template()
        self.assertEqual(testhtml in template, True)

    def test_second_overview(self):
        self.searchable_text = 'Test'
        self.search_text_in_request = True
        self.overview.update()
        self.assertEqual(self.overview.show_search_results, True)
        testhtml = ''
        template = self.overview.template()
        self.assertEqual(testhtml in template, True)
