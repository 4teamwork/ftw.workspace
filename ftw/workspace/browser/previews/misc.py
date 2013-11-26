from ftw.workspace.browser.previews.default import DefaultPreview
from ftw.workspace.interfaces import IWorkspacePreview
from Products.CMFCore.utils import getToolByName
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from Products.ATContentTypes.interfaces.file import IATFile


class ZipPreview(DefaultPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    def full_url(self):
        portal_url = getToolByName(self.context, 'portal_url')
        return '{0}/++resource++ftw.workspace-resources/zip.png'.format(
            portal_url())


class TxtPreview(DefaultPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    def full_url(self):
        portal_url = getToolByName(self.context, 'portal_url')
        return '{0}/++resource++ftw.workspace-resources/txt.png'.format(
            portal_url())
