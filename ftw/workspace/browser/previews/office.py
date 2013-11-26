from ftw.workspace.browser.previews.default import DefaultPreview
from ftw.workspace.interfaces import IWorkspacePreview
from Products.CMFCore.utils import getToolByName
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from Products.ATContentTypes.interfaces.file import IATFile


class DocPreview(DefaultPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    def full_url(self):
        portal_url = getToolByName(self.context, 'portal_url')
        return '{0}/++resource++ftw.workspace-resources/doc.png'.format(
            portal_url())


class DocXPreview(DefaultPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    def full_url(self):
        portal_url = getToolByName(self.context, 'portal_url')
        return '{0}/++resource++ftw.workspace-resources/docx.png'.format(
            portal_url())


class PptPreview(DefaultPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    def full_url(self):
        portal_url = getToolByName(self.context, 'portal_url')
        return '{0}/++resource++ftw.workspace-resources/ppt.png'.format(
            portal_url())
