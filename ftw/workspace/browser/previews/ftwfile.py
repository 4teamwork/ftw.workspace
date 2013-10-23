from ftw.file.interfaces import IFile
from ftw.workspace.interfaces import IWorkspacePreview
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class ImagePreview(object):
    """Image preview"""

    implements(IWorkspacePreview)
    adapts(IFile, Interface)

    def __init__(self, file_, request):
        self.file_ = file_
        self.request = request

    def preview(self):
        scale = self.file_.restrictedTraverse('@@images')
        # scale is not implemented (ex. scale='mini' in ftwfile @@images)
        return scale.scale('file', width=200, direction='down').tag()

    def full_url(self):
        return '{0}/big_img'.format(self.file_.absolute_url())
