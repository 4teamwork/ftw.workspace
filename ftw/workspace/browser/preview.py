from DateTime import DateTime
from ftw.table.helper import readable_date_text
from ftw.workspace.interfaces import IWorkspacePreview
from plone.batching.batch import BaseBatch
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MimetypesRegistry.common import MimeTypeException
from zope.component import queryMultiAdapter


class PreviewTab(BrowserView):
    """Preview tab for workspace"""

    template = ViewPageTemplateFile('preview_tab.pt')

    def __call__(self):
        return self.template()

    def previews(self):
        return self.context.restrictedTraverse('@@previews')()


class LoadPreviews(BrowserView):

    template = ViewPageTemplateFile('previews.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.bsize = 12
        self.bstart = 0

    def __call__(self, bstart=0):
        self.bstart = int(bstart)

        return self.template()

    def _query(self, **kwargs):
        query = dict(
            sort_on='modified',
            sort_order="descending",
            portal_type=['File', 'Document', 'Image'],
            path='/'.join(self.context.getPhysicalPath()))

        query.update(kwargs)
        return query

    def get_extensions(self, contenttype):
        mimetool = getToolByName(self.context, 'mimetypes_registry')

        if not contenttype:
            return []

        try:
            mimetype = mimetool.lookup(contenttype)
        except MimeTypeException:
            return []

        if not mimetype:
            return []
        else:
            # only use first result
            mimetype = mimetype[0]

        return mimetype.extensions

    def get_previews(self, **kwargs):
        catalog = getToolByName(self.context, 'portal_catalog')
        result = catalog(self._query(**kwargs))

        batch = BaseBatch(result, self.bsize, start=self.bstart)
        previews = []

        if self.bstart >= batch.end:
            return ''

        for brain in batch:
            obj = brain.getObject()

            adapter = queryMultiAdapter((obj, obj.REQUEST), IWorkspacePreview)

            # Try to get a specific preview adapter
            for extension in self.get_extensions(obj.getContentType()):
                specific = queryMultiAdapter(
                    (obj, obj.REQUEST),
                    IWorkspacePreview,
                    name=extension)

                if specific is not None:
                    adapter = specific
                    break

            previews.append(adapter)
        return previews

    def get_group_information(self, preview_adapter):
        """Rendered as hidden field per entry"""
        attr = self._query()['sort_on']
        context = preview_adapter.context

        value = getattr(context, attr)()
        if isinstance(value, DateTime):
            return readable_date_text(context, value)
        else:
            return value
