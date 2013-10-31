from ftw.file.interfaces import IFile
from ftw.workspace.browser.previews.image import ImagePreview
from zope.component import adapts
from zope.interface import Interface


class ImagePreview(ImagePreview):
    """Image preview"""

    adapts(IFile, Interface)
