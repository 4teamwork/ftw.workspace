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
        return ('<img height="200px" src="{0}" alt="{1}" title="{1}" '
                'data-preview=\'{2}\' />').format(
                    self.full_url(),
                    _(u'text_no_preview', default=u'No Preview'),
                    self.data_preview_attr())

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

    def data_preview_attr(self):
        return '{{"detail_url":"{0}", "download_url":"{1}"}}'.format(
            self.detail_url(),
            self.download_url())

    def download_url(self):
        return "%s/download" % self.context.absolute_url()

    def preview_type(self):
        return 'image'


class PDFPeekPreview(DefaultPreview):

    preview_image_path = '++resource++ftw.workspace-resources/default.png'

    def __init__(self, context, request):
        super(PDFPeekPreview, self).__init__(context, request)
        self.has_pdfpeek_preview = bool(context.unrestrictedTraverse(
            'view-image-annotation',
            None))

    def full_url(self):
        if self.has_pdfpeek_preview:
            return '{0}/pdf_two_slides_preview'.format(
                self.context.absolute_url())
        else:
            portal_url = getToolByName(self.context, 'portal_url')
            return '{0}/{1}'.format(portal_url(), self.preview_image_path)

    def preview(self):
        if self.has_pdfpeek_preview:
            return ('<img height="200px" src="{0}" alt="{1}" title="{1}" '
                    'data-preview=\'{2}\' />'.format(
                        '{0}/++images++1_thumb'.format(
                            self.context.absolute_url()),
                        self.context.Title(),
                        self.data_preview_attr()))
        else:
            return super(PDFPeekPreview, self).preview()

    def preview_type(self):
        if self.has_pdfpeek_preview:
            return 'html'
        else:
            return 'image'
