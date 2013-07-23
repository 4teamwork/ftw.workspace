from DateTime import DateTime
from datetime import datetime
from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from pyquery import PyQuery as pq
from unittest2 import TestCase


class TestOverviewTab(TestCase):

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace')
            .titled('Workspace')
            .having(description='Description'))

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def test_overview_tab_available(self):
        view = self.workspace.restrictedTraverse('tabbedview_view-overview')

        self.assertIsNotNone(view, 'Overview tab is no available.')

    def test_recently_modified_listing_order(self):
        file1 = create(Builder('file')
            .within(self.workspace)
            .titled('Dummy File')
            .having(modificationDate=DateTime() - 1)
            .attach_file_containing('DATA', name='dummy.pdf'))

        self.browser.open(
            '%s/tabbedview_view-overview' % self.workspace.absolute_url())
        doc = pq(self.browser.contents)
        listing = doc('.overview-right-column tr')

        self.assertEquals(2, len(listing),
            'Expect two entries in recently modified listing')

        self.assertEquals(self.workspace.Title(),
            doc('a.rollover', listing[0]).text())

        self.assertEquals(file1.Title(),
            doc('a.rollover', listing[1]).text())

    def test_overview_description(self):
        self.browser.open(
            '%s/tabbedview_view-overview' % self.workspace.absolute_url())
        doc = pq(self.browser.contents)

        self.assertIn(self.workspace.Description(),
            doc('.textbox')[0].text_content(),
            'Description not found')

    def test_overview_base_catalog_result(self):
        file1 = create(Builder('file')
            .within(self.workspace)
            .having(modificationDate=DateTime() - 1)
            .attach_file_containing('DATA', name='dummy.pdf'))

        file2 = create(Builder('file')
            .within(self.workspace)
            .having(modificationDate=DateTime() - 2)
            .attach_file_containing('DATA', name='dummy.pdf'))

        view = self.workspace.restrictedTraverse('tabbedview_view-overview')

        self.assertEquals([self.workspace.id, file1.id, file2.id],
            [brain.getId for brain in view.catalog()],
            'Wrong default order')

    def test_display_subfolders(self):
        folder = create(Builder('TabbedViewFolder')
            .within(self.workspace)
            .titled('SubFolder'))

        self.browser.open(
            '%s/tabbedview_view-overview' % self.workspace.absolute_url())
        doc = pq(self.browser.contents)
        self.assertEquals(folder.Title(),
            doc('.overview-left-column .box ul li a.rollover').text())

    def test_show_ten_recently_modified_items(self):
        for i in range(1, 15):
            create(Builder('file')
                .within(self.workspace))

        view = self.workspace.restrictedTraverse('tabbedview_view-overview')

        self.assertEquals(10, len(view.recently_modified()),
            'Display only the ten most recent changes')

    def test_save_description(self):
        create(Builder('file')
            .within(self.workspace)
            .having(description='<b>Bold description</b>')
            .attach_file_containing('DATA', name='dummy.pdf'))
        brain = self.workspace.getFolderContents()[0]

        view = self.workspace.restrictedTraverse('tabbedview_view-overview')

        self.assertEquals('Bold description', view.get_description(brain))

    def test_overview_show_search_description(self):
        view = self.workspace.restrictedTraverse('tabbedview_view-overview')

        self.assertFalse(view.show_search_results())

        view.request['searchable_text'] = 'something'
        self.assertTrue(view.show_search_results())

    def test_overview_type_class_file(self):
        view = self.workspace.restrictedTraverse('tabbedview_view-overview')
        create(Builder('file')
            .within(self.workspace)
            .attach_file_containing('DATA', name='dummy.pdf'))
        brain = self.workspace.getFolderContents()[0]

        self.assertEquals('', view.type_class(brain))

    def test_overview_type_class_other(self):
        view = self.workspace.restrictedTraverse('tabbedview_view-overview')
        create(Builder('document')
            .within(self.workspace))
        brain = self.workspace.getFolderContents()[0]

        self.assertEquals('contenttype-document',
            view.type_class(brain))

    def test_overview_generate_date_today(self):
        view = self.workspace.restrictedTraverse('tabbedview_view-overview')
        now = datetime(2013, 6, 3, 11, 0)

        datestring = '2013-06-03 09:00:00'
        self.assertEquals('label_today', view.generate_date(datestring, now))

    def test_overview_generate_date_yesterday(self):
        view = self.workspace.restrictedTraverse('tabbedview_view-overview')
        now = datetime(2013, 6, 3, 11, 0)

        datestring = '2013-06-02 09:00:00'
        self.assertEquals('label_yesterday',
            view.generate_date(datestring, now))

    def test_overview_generate_date_older(self):
        view = self.workspace.restrictedTraverse('tabbedview_view-overview')
        now = datetime(2013, 6, 3, 11, 0)

        datestring = '2013-03-01 11:00:00'
        self.assertEquals('01.03.2013', view.generate_date(datestring, now))
