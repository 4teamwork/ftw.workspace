from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.registry.interfaces import IRegistry
from unittest2 import TestCase
from zope.component import getUtility


class TestOverviewFolderSublisting(TestCase):

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

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
        self.assertEquals(0, objects.index(folder1))
        self.assertEquals(1, objects.index(folder2))

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
        self.assertEquals('TabbedViewFolder', self.view.collect()[1]['title'])

        files = self.view.collect()[0]['objects']
        folders = self.view.collect()[1]['objects']

        self.assertIn(file_, files)
        self.assertIn(folder, folders)

