from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
from zExceptions import Unauthorized
import transaction


class TestWorkspaceWorkflow(TestCase):

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

    def setUp(self):
        self.browser = Browser(self.layer['app'])
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.portal_types['Folder'].allowed_content_types = (
            'Workspace', )

        self.folder = self._setup_projects_folder_with_placeful_workflow()

    def _setup_projects_folder_with_placeful_workflow(self):
        folder = create(Builder('folder'))

        policy_id = 'workspace_policy'

        folder.manage_addProduct['CMFPlacefulWorkflow']\
            .manage_addWorkflowPolicyConfig()
        config = getToolByName(
            folder,
            'portal_placeful_workflow').getWorkflowPolicyConfig(folder)

        config.setPolicyIn(policy=policy_id)
        config.setPolicyBelow(policy=policy_id, update_security=True)
        transaction.commit()

        return folder

    def test_anonymous_user_cannot_access_folder(self):
        logout()

        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse(self.folder.getId())

    def test_authenticated_user_can_view_folder(self):
        user = create(Builder('user'))

        logout()
        login(self.portal, user.getId())

        self.assertTrue(
            self.portal.restrictedTraverse(self.folder.getId()),
            'A authenticated user should have access to the folder')

    def test_authenticated_user_CANNOT_view_workspace(self):
        workspace = create(Builder('workspace').within(self.folder))
        user = create(Builder('user').with_roles('Authenticated'))

        logout()
        login(self.portal, user.getId())

        with self.assertRaises(Unauthorized):
            self.folder.restrictedTraverse(workspace.getId())

    def test_reader_CAN_view_workspace(self):
        workspace = create(Builder('workspace').within(self.folder))
        user = create(Builder('user').with_roles('Reader', on=workspace))

        logout()
        login(self.portal, user.getId())

        self.assertTrue(
            self.folder.restrictedTraverse(workspace.getId()),
            'A reader should have access to the workspace')

    def test_contributor_CAN_add_content_in_workspace(self):
        workspace = create(Builder('workspace').within(self.folder))
        user = create(Builder('user').with_roles('Contributor', on=workspace))

        logout()
        login(self.portal, user.getId())

        self.assertTrue(
            create(Builder('TabbedViewFolder').within(workspace)),
            'Contributor should be able to add a tabbedviewfolder')

        self.assertTrue(
            create(Builder('file').within(workspace)),
            'Contributor should be able to add a tabbedviewfolder')

    def test_contributor_CAN_delete_his_content_in_workspace(self):
        workspace = create(Builder('workspace').within(self.folder))
        user = create(Builder('user').with_roles('Contributor', on=workspace))

        logout()
        login(self.portal, user.getId())

        item = create(Builder('TabbedViewFolder').within(workspace))
        id_ = item.getId()

        workspace.manage_delObjects([id_])

        self.assertNotIn(id_, workspace.objectIds())

    def test_contributor_CANNOT_delete_workspace(self):
        workspace = create(Builder('workspace').within(self.folder))
        user = create(Builder('user').with_roles('Contributor', on=workspace))

        logout()
        login(self.portal, user.getId())

        with self.assertRaises(Unauthorized):
            self.folder.manage_delObjects([workspace.getId()])

    def test_admin_CAN_manage_permissions(self):
        workspace = create(Builder('workspace').within(self.folder))
        user = create(Builder('user')
                      .with_roles('Editor', on=workspace))

        logout()
        login(self.portal, user.getId())

        self.assertTrue(workspace.restrictedTraverse('@@sharing'),
                        'Admin shold habe access to the sharing view')

    def test_others_CANNOT_manage_permissions(self):
        workspace = create(Builder('workspace').within(self.folder))
        user = create(Builder('user').with_roles('Contributor', on=workspace))

        logout()
        login(self.portal, user.getId())

        with self.assertRaises(Unauthorized):
            workspace.restrictedTraverse('@@sharing')

    def test_admin_CAN_delete_workspace(self):
        workspace = create(Builder('workspace').within(self.folder))
        workspace_id = workspace.getId()
        user = create(Builder('user')
                      .with_roles('Editor', on=workspace))

        logout()
        login(self.portal, user.getId())

        self.folder.manage_delObjects([workspace.getId()])
        self.assertNotIn(workspace_id, self.folder.objectIds())

    def test_site_admin_CAN_delete_his_workspace(self):
        workspace = create(Builder('workspace').within(self.folder))
        workspace_id = workspace.getId()
        user = create(Builder('user')
                      .with_roles('Editor'))

        logout()
        login(self.portal, user.getId())

        self.folder.manage_delObjects([workspace_id])

        self.assertNotIn(workspace_id, self.folder.objectIds())

    def test_reader_CANNOT_edit_content(self):
        workspace = create(Builder('workspace').within(self.folder))
        user = create(Builder('user').with_roles('Reader', on=workspace))
        item = create(Builder('TabbedViewFolder').within(workspace))

        logout()
        login(self.portal, user.getId())

        with self.assertRaises(Unauthorized):
            item.restrictedTraverse('edit')

    def test_contributor_CAN_edit_his_content(self):
        workspace = create(Builder('workspace').within(self.folder))
        user = create(Builder('user').with_roles('Contributor', on=workspace))

        logout()
        login(self.portal, user.getId())

        item = create(Builder('TabbedViewFolder').within(workspace))
        self.assertTrue(item.restrictedTraverse('edit'),
                        'Contributor should be able to edit his content')
