from ftw.workspace import _
from ftw.workspace.browser.previews.default import DefaultPreview
from ftw.workspace.interfaces import IWorkspacePreview
from Products.ATContentTypes.interfaces.file import IATFile
from Products.CMFCore.utils import getToolByName
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


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


class PptxPreview(DefaultPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    def full_url(self):
        portal_url = getToolByName(self.context, 'portal_url')
        return '{0}/++resource++ftw.workspace-resources/pptx.png'.format(
            portal_url())


class XlsPreview(DefaultPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    def full_url(self):
        portal_url = getToolByName(self.context, 'portal_url')
        return '{0}/++resource++ftw.workspace-resources/xls.png'.format(
            portal_url())


class XlsxPreview(DefaultPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    def full_url(self):
        portal_url = getToolByName(self.context, 'portal_url')
        return '{0}/++resource++ftw.workspace-resources/xlsx.png'.format(
            portal_url())


class PdfPreview(DefaultPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    def __init__(self, context, request):
        super(PdfPreview, self).__init__(context, request)
        self.has_image_preview = bool(self.context.restrictedTraverse(
            'view-image-annotation',
            None))

    def full_url(self):
        if self.has_image_preview:
            return '{0}/pdf_two_slides_preview'.format(
                self.context.absolute_url())
        else:
            portal_url = getToolByName(self.context, 'portal_url')
            return '{0}/++resource++ftw.workspace-resources/pdf.png'.format(
                portal_url())

    def preview(self):
        if self.has_image_preview:
            return '<img height="200px" src="{0}" alt={1} title={1}/>'.format(
                '{0}/++images++1_thumb'.format(
                    self.context.absolute_url()),
                self.context.Title()
            )
        else:
            return '<img height="200px" src="{0}" alt={1} title={1}/>'.format(
                self.full_url(),
                _(u'text_no_preview', default=u'No Preview')
                )

    def preview_type(self):
        if self.has_image_preview:
            return 'html'
        else:
            return 'image'
