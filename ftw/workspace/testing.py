from ftw.tabbedview.interfaces import IGridStateStorageKeyGenerator
from ftw.tabbedview.interfaces import ITabbedView
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.registry import Registry
from plone.registry.interfaces import IRegistry
from plone.testing import Layer
from plone.testing import z2
from plone.testing import zca
from zope.component import provideAdapter
from zope.component import provideUtility
from zope.configuration import xmlconfig
from zope.interface import Interface


USERS = [
    {'user': 'member1', 'roles': ('Member', 'Reader')},
    {'user': 'member2', 'roles': ('Member', 'Reader')},
    {'user': 'member3', 'roles': ('Member', 'Reader')}]


class FtwWorkspaceLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.workspace
        import zope.traversing
        xmlconfig.file(
            'configure.zcml',
            ftw.workspace,
            context=configurationContext)
        xmlconfig.file(
            'configure.zcml',
            zope.traversing,
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


class BasicMockOverviewLayer(Layer):

    defaultBases = (zca.ZCML_DIRECTIVES, )

    def testSetUp(self):
        self['configurationContext'] = context = \
            zca.stackConfigurationContext(self.get('configurationContext'))

        import zope.traversing
        xmlconfig.file('configure.zcml', zope.traversing, context=context)

        import plone.registry
        xmlconfig.file('configure.zcml', plone.registry, context=context)

        registry = Registry()
        provideUtility(component=registry, provides=IRegistry)
        registry.registerInterface(ITabbedView)

        class GridStateKeyGenerator(object):
            """Stub
            ftw.tabbedview.statestorage.DefaultGridStateStorageKeyGenerator
            """

            def __init__(self, *args):
                pass

            def get_key(self):
                return '1'

        provideAdapter(GridStateKeyGenerator,
                       (Interface, Interface, Interface),
                       IGridStateStorageKeyGenerator)

        import ftw.dictstorage
        xmlconfig.file('configure.zcml', ftw.dictstorage, context=context)

    def testTearDown(self):
        del self['configurationContext']

OVERVIEW_LAYER = BasicMockOverviewLayer()


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
