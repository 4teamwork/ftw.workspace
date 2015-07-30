from ftw.bumblebee.utils import item_for_brain
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

    def get_previews(self, **kwargs):
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(self._query())
        return map(item_for_brain, results)
