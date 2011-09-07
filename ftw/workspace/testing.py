from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.testing import z2
from zope.configuration import xmlconfig


USERS = [
    {'user': 'member1', 'roles': ('Member', 'Reader')},
    {'user': 'member2', 'roles': ('Member', 'Reader')},
    {'user': 'member3', 'roles': ('Member', 'Reader')}]


class FtwWorkspaceLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.workspace
        xmlconfig.file(
            'configure.zcml',
            ftw.workspace,
            context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2 products,
        # using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'ftw.workspace')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.workspace:default')

        # Add role for vocab testing
        portal._addRole('Reader')

        # Setup some users
        for userinfo in USERS:
            username = userinfo['user']
            portal.acl_users.userFolderAddUser(
                username, 'password', userinfo['roles'], [])

        # Setup a group and add member3
        portal.portal_groups.addGroup('group1')
        portal.portal_groups.addPrincipalToGroup("member3", "group1")


FTW_WORKSPACE_FIXTURE = FtwWorkspaceLayer()
FTW_WORKSPACE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_WORKSPACE_FIXTURE, ), name="FtwWorkspace:Integration")
