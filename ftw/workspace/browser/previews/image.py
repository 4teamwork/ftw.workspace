from ftw.workspace.interfaces import IWorkspacePreview
from plone.app.blob.interfaces import IATBlobImage
from plone.namedfile.interfaces import IAvailableSizes
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from zope.interface import Interface


class ImagePreview(object):
    """Image preview"""

    implements(IWorkspacePreview)
    adapts(IATBlobImage, Interface)

    def __init__(self, image, request):
        self.image = image
        self.request = request

    def preview(self):
        scale = self.image.restrictedTraverse('@@images')
        width, height = self.get_scale_properties()
        # scale=workspace_preview would have the same result, but we need the
        # width/height accessable on the adaper
        return scale.scale(
            'image', width=width, height=height, direction='down').tag()

    def full_url(self):
        return '{0}/image_large'.format(self.image.absolute_url())

    def get_scale_properties(self):
        sizes = getUtility(IAvailableSizes)()
        return sizes.get('workspace_preview', (200, 200))
