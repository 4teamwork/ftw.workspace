from ftw.workspace import _
from ftw.workspace.interfaces import IWorkspacePreview
from plone.namedfile.interfaces import IAvailableSizes
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from zope.interface import Interface


class DefaultPreview(object):
    """Default preview"""

    implements(IWorkspacePreview)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def preview(self):
        return '<img height="200px" src="{0}" alt={1} />'.format(
            self.full_url(),
            _(u'text_no_preview', default=u'No Preview')
            )

    def full_url(self):
        return '{0}/++resource++ftw.workspace-resources/default.jpeg'.format(
            self.context.absolute_url())

    def get_scale_properties(self):
        sizes = getUtility(IAvailableSizes)()
        return sizes.get('workspace_preview', (200, 200))
