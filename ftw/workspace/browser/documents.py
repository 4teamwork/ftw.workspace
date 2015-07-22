from DateTime import DateTime
from ftw.table.helper import readable_date_text
from ftw.workspace.interfaces import IWorkspacePreview
from plone.batching.batch import BaseBatch
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MimetypesRegistry.common import MimeTypeException
from zope.component import queryMultiAdapter
from ftw.bumblebee.utils import get_representation_url
from ftw.bumblebee.mimetypes import get_mimetype_image_url
from ftw.bumblebee.mimetypes import get_mimetype_title


class DocumentsTab(BrowserView):
    """Preview tab for workspace"""

    template = ViewPageTemplateFile('documents.pt')

    def __call__(self):
        return self.template()

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _query(self, **kwargs):
        query = dict(
            object_provides='ftw.bumblebee.interfaces.IBumblebeeable',
            sort_on='modified',
            sort_order="descending",
            path='/'.join(self.context.getPhysicalPath()))

        query.update(kwargs)
        return query

    def get_previews(self, **kwargs):
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(self._query())
        return map(self.item_for_brain, results)

    def item_for_brain(self, brain):
        portal_url = getToolByName(self.context, 'portal_url')()
        not_found_image_url = (portal_url +
                               '/++resource++ftw.workspace-resources/image_not_found.png')

        if brain.bumblebee_checksum:
            preview_image_url = get_representation_url('thumbnail',
                                                       checksum=brain.bumblebee_checksum,
                                                       fallback_url=not_found_image_url)

        else:
            preview_image_url = not_found_image_url

        mimetype_image_url = get_mimetype_image_url(brain.getContentType)
        return {'title': brain.Title,
                'description': brain.Description,
                'details_url': brain.getURL() + '/view',
                'overlay_url': brain.getURL() + '/file_preview?nav=true',
                'preview_image_url': preview_image_url,
                'mimetype_image_url': mimetype_image_url,
                'mimetype_title': get_mimetype_title(brain.getContentType),
                }
