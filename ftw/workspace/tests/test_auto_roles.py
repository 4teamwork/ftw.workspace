from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.testing import FTW_WORKSPACE_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry
from unittest2 import TestCase
from zope.component import getUtility


class TestAutoRoles(TestCase):

    layer = FTW_WORKSPACE_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

    def test_roles_are_automaticall_assigned_on_workspace_creation(self):
        workspace = create(Builder('workspace'))
        roles = set(dict(workspace.get_local_roles()).get(TEST_USER_ID))

        self.assertEquals(
            set(['Owner', 'Contributor', 'Editor', 'Reader']),
            roles,
            'The configured roles should be automatically granted to the owner.')

    def test_auto_roles_are_configurable_with_registry_entry(self):
        registry = getUtility(IRegistry)
        roles = registry['ftw.workspace.auto_roles'] = [u'Editor']

        workspace = create(Builder('workspace'))
        roles = set(dict(workspace.get_local_roles()).get(TEST_USER_ID))

        self.assertEquals(
            set(['Owner', 'Editor']),
            roles,
            'Only the configured auto_roles should be granted to the owner.')
