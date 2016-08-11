from ftw.builder.session import BuilderSession
from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import set_builder_session_factory
from ftw.tabbedview.interfaces import ITabbedView
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.registry.interfaces import IRegistry
from plone.testing import Layer
from plone.testing import z2
from plone.testing import zca
from zope.component import getUtility
from zope.configuration import xmlconfig
import egov.contactdirectory.tests.builders
import ftw.meeting.tests.builders
import ftw.workspace.tests.builders


def functional_session_factory():
    sess = BuilderSession()
    sess.auto_commit = True
    return sess


class FtwWorkspaceLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '  <include package="Products.CMFPlacefulWorkflow" />'
            '</configure>',
            context=configurationContext)

        # DatagridField doesn't define the auto-include entry point
        import Products.DataGridField
        xmlconfig.file('configure.zcml',
                       Products.DataGridField,
                       context=configurationContext)

        z2.installProduct(app, 'ftw.workspace')
        z2.installProduct(app, 'ftw.file')
        z2.installProduct(app, 'ftw.meeting')
        z2.installProduct(app, 'Products.DataGridField')
        z2.installProduct(app, 'egov.contactdirectory')
        z2.installProduct(app, 'Products.CMFPlacefulWorkflow')
        # Dep. of egov.contactdirectory
        z2.installProduct(app, 'ftw.contentpage')
        z2.installProduct(app, 'simplelayout.types.common')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.workspace:default')
        applyProfile(portal, 'ftw.workspace:contact')

        # Disable extjs integration for tests.
        registry = getUtility(IRegistry)
        reg_proxy = registry.forInterface(ITabbedView)
        reg_proxy.extjs_enabled = False


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
