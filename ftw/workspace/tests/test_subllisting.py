from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.testing import FTW_WORKSPACE_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.registry.interfaces import IRegistry
from pyquery import PyQuery
from unittest2 import TestCase
from zope.component import getUtility


class TestOverviewFolderSublisting(TestCase):

    layer = FTW_WORKSPACE_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace'))
        self.view = self.workspace.restrictedTraverse('@@overview_sublisting')

    def test_sublisting_empty(self):

        self.assertListEqual([], self.view.collect())

    def test_sublisting_folders(self):
        create(Builder('TabbedViewFolder')
            .within(self.workspace)
            .titled('Folder'))

        self.assertEquals(1, len(self.view.collect()), 'Expect one Folder')

    def test_sublisting_result(self):
        folder1 = create(Builder('TabbedViewFolder')
            .within(self.workspace)
            .titled('A folder'))
        folder2 = create(Builder('TabbedViewFolder')
            .within(self.workspace)
            .titled('B folder'))

        self.assertEquals(1, len(self.view.collect()), 'Expect one Folder')
        self.assertEquals('Folder', self.view.collect()[0]['title'])

        objects = self.view.collect()[0]['objects']
        self.assertIn(folder1.getId(), [item.getId for item in objects])
        self.assertIn(folder2.getId(), [item.getId for item in objects])

    def test_list_more_types(self):
        registry = getUtility(IRegistry)
        registry['ftw.workspace.sublisting_types'].append('File')

        folder = create(Builder('TabbedViewFolder')
            .within(self.workspace)
            .titled('A folder'))

        file_ = create(Builder('file')
            .titled('File')
            .within(self.workspace))

        self.assertEquals(2, len(self.view.collect()), 'Expect two Folders')

        self.assertEquals('File', self.view.collect()[0]['title'])
        self.assertEquals('Folder', self.view.collect()[1]['title'])

        files = self.view.collect()[0]['objects']
        folders = self.view.collect()[1]['objects']

        self.assertIn(folder.getId(), [item.getId for item in folders])
        self.assertIn(file_.getId(), [item.getId for item in files])

    def test_sublisting_renders(self):
        create(Builder('TabbedViewFolder')
            .within(self.workspace)
            .titled('A folder'))

        doc = PyQuery(self.view())

        self.assertTrue(doc('ul li a'))
        self.assertTrue(doc('h2'))

    def test_sublisting_renders_in_overview_tab(self):
        create(Builder('TabbedViewFolder')
            .within(self.workspace)
            .titled('Folder'))

        tab = self.workspace.restrictedTraverse('@@tabbedview_view-overview')
        doc = PyQuery(tab())

        self.assertTrue(doc('.box.sublisting li'))

    def test_sublisting_listed_objects_are_linked(self):
        folder = create(Builder('TabbedViewFolder')
            .within(self.workspace)
            .titled('A folder'))

        doc = PyQuery(self.view())
        href = doc('.box.sublisting a.rollover').attr('href')

        self.assertEquals(folder.absolute_url(), href)

    def test_translate_title(self):
        self.assertEquals('Folder',
                          self.view.translated_title('TabbedViewFolder'))
        self.assertEquals('Page',
                          self.view.translated_title('Document'))
        self.assertEquals('File',
                          self.view.translated_title('File'))

    def test_translate_title_fallback(self):
        self.assertEquals('Dummy',
                          self.view.translated_title('Dummy'))
