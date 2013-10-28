from ftw.file.interfaces import IFile
from ftw.workspace.browser.previews.default import DefaultPreview
from ftw.workspace.interfaces import IWorkspacePreview
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class ImagePreview(DefaultPreview):
    """Image preview"""

    implements(IWorkspacePreview)
    adapts(IFile, Interface)

    def preview(self):
        scale = self.context.restrictedTraverse('@@images')
        width, height = self.get_scale_properties()
        # scale is not implemented (ex. scale='mini' in ftwfile @@images)
        return scale.scale(
            'file', width=width, height=height, direction='down').tag()

    def full_url(self):
        return '{0}/big_img'.format(self.context.absolute_url())
