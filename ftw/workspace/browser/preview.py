from ftw.workspace.interfaces import IWorkspacePreview
from itertools import groupby
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MimetypesRegistry.common import MimeTypeException
from zope.component import queryMultiAdapter
from ftw.table.helper import readable_date_text


class PreviewTab(BrowserView):
    """Preview tab for workspace"""

    template = ViewPageTemplateFile('preview.pt')

    def __call__(self):
        return self.template()

    @property
    def _query(self):
        return dict(
            path='/'.join(self.context.getPhysicalPath()))

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

    def get_previews(self):

        def groupbymodifieddate(item):
            return readable_date_text(item, item.modified)

        keys, previews = self.group(keyfunc=groupbymodifieddate)

        return dict(keys=keys,
                    previews=previews)

    def group(self, keyfunc='modified'):
        catalog = getToolByName(self.context, 'portal_catalog')
        result = catalog(self._query)

        if not callable(keyfunc):
            raise TypeError('keyfunc is not a function')

        keys = []
        groups = []
        for key, group in groupby(result, key=keyfunc):

            previews = []
            for obj in group:
                adapter = self.get_preview_adapter(obj)
                if adapter:
                    previews.append(adapter)

            # Only append items with a preview adapter
            if previews:
                groups.append(previews)
                keys.append(key)

        return keys, groups

    def get_preview_adapter(self, brain):
            obj = brain.getObject()

            for extension in self.get_extensions(obj.getContentType()):
                adapter = queryMultiAdapter(
                    (obj, obj.REQUEST),
                    IWorkspacePreview,
                    name=extension)

                if adapter is not None:
                    return adapter

            return None
