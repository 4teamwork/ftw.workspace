from ftw.workspace.browser.previews.default import PDFPeekPreview
from ftw.workspace.interfaces import IWorkspacePreview
from Products.ATContentTypes.interfaces.file import IATFile
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class DocPreview(PDFPeekPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    preview_image_path = '++resource++ftw.workspace-resources/doc.png'


class DocXPreview(PDFPeekPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    preview_image_path = '++resource++ftw.workspace-resources/docx.png'


class PptPreview(PDFPeekPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    preview_image_path = '++resource++ftw.workspace-resources/ppt.png'


class PptxPreview(PDFPeekPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    preview_image_path = '++resource++ftw.workspace-resources/pptx.png'


class XlsPreview(PDFPeekPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    preview_image_path = '++resource++ftw.workspace-resources/xls.png'


class XlsxPreview(PDFPeekPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    preview_image_path = '++resource++ftw.workspace-resources/xlsx.png'


class PdfPreview(PDFPeekPreview):

    implements(IWorkspacePreview)
    adapts(IATFile, Interface)

    preview_image_path = '++resource++ftw.workspace-resources/pdf.png'
