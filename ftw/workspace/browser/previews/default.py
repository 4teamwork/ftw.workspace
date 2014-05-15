from ftw.workspace import _
from ftw.workspace.interfaces import IWorkspacePreview
from plone.namedfile.interfaces import IAvailableSizes
from Products.CMFCore.utils import getToolByName
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
        return '<img height="200px" src="{0}" alt="{1}" title="{1}" detail_url="{2}" download_url="{3}" />'.format(
            self.full_url(),
            _(u'text_no_preview', default=u'No Preview'),
            self.detail_url(),
            self.download_url()
            )

    def full_url(self):
        portal_url = getToolByName(self.context, 'portal_url')
        return '{0}/++resource++ftw.workspace-resources/default.png'.format(
            portal_url())

    def get_scale_properties(self):
        sizes = getUtility(IAvailableSizes)()
        return sizes.get('workspace_preview', (200, 200))

    def detail_url(self):
        properties = getToolByName(self.context, 'portal_properties')
        view_action_types = properties.site_properties.getProperty(
            'typesUseViewActionInListings', ())
        url = self.context.absolute_url()
        if self.context.portal_type in view_action_types:
            url = '%s/view' % url

        return url

    def download_url(self):
        return "%s/download" % self.context.absolute_url()

    def preview_type(self):
        return 'image'
