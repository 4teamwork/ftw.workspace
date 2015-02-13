from Products.CMFCore.utils import getToolByName
from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.testing import FTW_WORKSPACE_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase


class TestWorkspace(TestCase):

    layer = FTW_WORKSPACE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_searchable_text_contains_workspace_creator(self):
        """
        The full name of the creator of a workspace has to be in the
        searchable text index so the workspace overview listing can
        be filtered by creator.
        """
        folder = create(Builder('folder'))
        hugo = create(
            Builder('user')
            .named('Hugo', 'Boss')
            .with_roles('Contributor', on=folder)
        )

        login(self.portal, hugo.getId())
        workspace = create(
            Builder('workspace').within(folder).titled('My Workspace')
        )

        portal_catalog = getToolByName(self.layer['portal'], 'portal_catalog')
        rid = portal_catalog.getrid('/'.join(workspace.getPhysicalPath()))
        index_data = portal_catalog.getIndexDataForRID(rid)

        expected = {'boss', 'hugo', 'my', 'workspace'}
        actual = set(index_data['SearchableText'])
        self.assertTrue(expected.issubset(actual))
