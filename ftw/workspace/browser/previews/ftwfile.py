from ftw.file.interfaces import IFile
from ftw.workspace.interfaces import IWorkspacePreview
from plone.namedfile.interfaces import IAvailableSizes
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from zope.interface import Interface


class ImagePreview(object):
    """Image preview"""

    implements(IWorkspacePreview)
    adapts(IFile, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def preview(self):
        scale = self.context.restrictedTraverse('@@images')
        width, height = self.get_scale_properties()
        # scale is not implemented (ex. scale='mini' in ftwfile @@images)
        return scale.scale(
            'file', width=width, height=height, direction='down').tag()

    def full_url(self):
        return '{0}/big_img'.format(self.context.absolute_url())

    def get_scale_properties(self):
        sizes = getUtility(IAvailableSizes)()
        return sizes.get('workspace_preview', (200, 200))
