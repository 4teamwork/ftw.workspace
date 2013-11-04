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

    @property
    def _primary_field(self):
        return self.context.getPrimaryField().getName()

    def preview(self):
        scale = self.context.restrictedTraverse('@@images')
        width, height = self.get_scale_properties()

        return scale.scale(
            self._primary_field,
            width=width,
            height=height,
            direction='down').tag()

    def full_url(self):
        return '{0}/images/{1}'.format(self.context.absolute_url(),
                                self._primary_field)
