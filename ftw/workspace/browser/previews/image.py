from ftw.workspace.interfaces import IWorkspacePreview
from plone.app.blob.interfaces import IATBlobImage
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class ImagePreview(object):
    """Image preview"""

    implements(IWorkspacePreview)
    adapts(IATBlobImage, Interface)

    def __init__(self, image, request):
        self.image = image
        self.request = request

    def render(self):
        scale = self.image.restrictedTraverse('@@images')
        return scale.scale('image', scale='mini').tag()
