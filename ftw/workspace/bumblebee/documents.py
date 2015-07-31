from ftw.bumblebee.mimetypes import get_mimetype_image_url
from ftw.bumblebee.mimetypes import get_mimetype_title
from ftw.bumblebee.utils import get_representation_url_by_brain
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


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

        if 'searchable_text' in self.request.keys() and self.request['searchable_text'] != '':
            query['SearchableText'] = self.request.get('searchable_text')
            if not query['SearchableText'].endswith('*'):
                query['SearchableText'] += '*'
        query.update(kwargs)
        return query

    def previews(self, **kwargs):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(self._query())

        for brain in brains:
            desc = brain.Description
            if desc:
                desc = len(desc) < 50 and desc or desc[:49] + '...'
            yield {
                'title': brain.Title,
                'description': desc,
                'details_url': brain.getURL() + '/view',
                'overlay_url': brain.getURL() + '/file_preview',
                'preview_image_url': get_representation_url_by_brain(
                    'thumbnail', brain),
                'mimetype_image_url': get_mimetype_image_url(
                    brain.getContentType),
                'mimetype_title': get_mimetype_title(brain.getContentType),
                'uid': brain.UID,
            }
