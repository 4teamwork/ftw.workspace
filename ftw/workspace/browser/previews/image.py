from ftw.workspace.browser.previews.default import DefaultPreview
from ftw.workspace.interfaces import IWorkspacePreview
from plone.app.blob.interfaces import IATBlobImage
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class ImagePreview(DefaultPreview):
    """Image preview"""

    implements(IWorkspacePreview)
    adapts(IATBlobImage, Interface)

    def preview(self):
        scale = self.context.restrictedTraverse('@@images')
        width, height = self.get_scale_properties()
        # scale=workspace_preview would have the same result, but we need the
        # width/height accessable on the adaper
        return scale.scale(
            'image', width=width, height=height, direction='down').tag()

    def full_url(self):
        return '{0}/image_large'.format(self.context.absolute_url())
