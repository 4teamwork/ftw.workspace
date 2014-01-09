from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.quick_upload import generate_id
from ftw.workspace.testing import FTW_WORKSPACE_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase


class TestQuickUploadIdGenerator(TestCase):

    layer = FTW_WORKSPACE_INTEGRATION_TESTING

    def setUp(self):
        super(TestQuickUploadIdGenerator, self).setUp()

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_name_starting_with_underscore(self):
        name = u'_test'
        self.assertEquals(u'test', generate_id(name, self.portal))

    def test_existing_name(self):
        create(Builder('file').titled('test'))
        name = u'test'
        self.assertEquals(u'test-1', generate_id(name, self.portal))

    def test_name_with_umlauts(self):
        create(Builder('file').titled('test'))
        name = u't\xf6st'
        self.assertEquals(u'tost', generate_id(name, self.portal))

    def test_name_with_spaces(self):
        name = u'test test'
        self.assertEquals(u'test-test', generate_id(name, self.portal))
