from ftw.builder.session import BuilderSession
from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import set_builder_session_factory
from ftw.workspace.tests import builders
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import Layer
from plone.testing import z2
from plone.testing import zca
from Products.CMFCore.utils import getToolByName
from zope.configuration import xmlconfig


USERS = [
    {'user': 'member1', 'roles': ('Member', 'Reader'),
     'fullname': 'BBB MEMBER1'},
    {'user': 'member2', 'roles': ('Member', 'Reader'),
     'fullname': 'AAA MEMBER2'},
    {'user': 'member3', 'roles': ('Member', 'Reader'),
     'fullname': 'BAA MEMBER3'}]


def functional_session_factory():
    sess = BuilderSession()
    sess.auto_commit = True
    return sess


class FtwWorkspaceLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.workspace
        import zope.traversing
        import ftw.file
        xmlconfig.file(
            'configure.zcml',
            ftw.workspace,
            context=configurationContext)
        xmlconfig.file(
            'configure.zcml',
            zope.traversing,
            context=configurationContext)

        xmlconfig.file(
            'configure.zcml',
            ftw.file,
            context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2 products,
        # using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'ftw.workspace')
        z2.installProduct(app, 'ftw.file')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.workspace:default')
        applyProfile(portal, 'ftw.file:default')
        # Add role for vocab testing
        portal._addRole('Reader')

        mtool = getToolByName(portal, 'portal_membership')

        # Setup some users
        for userinfo in USERS:
            username = userinfo['user']

            portal.acl_users.userFolderAddUser(
                username, 'password', userinfo['roles'], [])

            member = mtool.getMemberById(username)
            member.setMemberProperties(
                mapping={"fullname": userinfo['fullname']})

        # Setup a group and add member3
        portal.portal_groups.addGroup('group1')
        portal.portal_groups.addPrincipalToGroup("member3", "group1")


FTW_WORKSPACE_FIXTURE = FtwWorkspaceLayer()
FTW_WORKSPACE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_WORKSPACE_FIXTURE, ), name="FtwWorkspace:Integration")

FTW_WORKSPACE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_WORKSPACE_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="FtwWorkspace:Functional")


class LatexZCMLLayer(Layer):
    """A layer which only sets up the zcml, but does not start a zope
    instance.
    """

    defaultBases = (zca.ZCML_DIRECTIVES, )

    def testSetUp(self):
        self['configurationContext'] = zca.stackConfigurationContext(
            self.get('configurationContext'))

        import zope.traversing
        xmlconfig.file('configure.zcml', zope.traversing,
                       context=self['configurationContext'])

        import ftw.pdfgenerator.tests
        xmlconfig.file('test.zcml', ftw.pdfgenerator.tests,
                       context=self['configurationContext'])

        import ftw.pdfgenerator
        xmlconfig.file('configure.zcml', ftw.pdfgenerator,
                       context=self['configurationContext'])

        import ftw.workspace.latex
        xmlconfig.file('configure.zcml', ftw.workspace.latex,
                       context=self['configurationContext'])

    def testTearDown(self):
        del self['configurationContext']


LATEX_ZCML_LAYER = LatexZCMLLayer()
