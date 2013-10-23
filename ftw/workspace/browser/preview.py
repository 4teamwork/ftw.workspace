from ftw.workspace.interfaces import IWorkspacePreview
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MimetypesRegistry.common import MimeTypeException
from zope.component import queryMultiAdapter


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
        catalog = getToolByName(self.context, 'portal_catalog')

        previews = []

        for brain in catalog(self._query):
            obj = brain.getObject()
            if obj == self.context:
                continue

            adapter = None
            for extension in self.get_extensions(obj.getContentType()):
                adapter = queryMultiAdapter(
                    (obj, obj.REQUEST),
                    IWorkspacePreview,
                    name=extension)
                if adapter is not None:
                    previews.append(adapter)
                    break

        return previews
