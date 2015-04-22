from ftw.pdfgenerator.interfaces import IPDFAssembler
from ftw.workspace.interfaces import IWorkspace
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.representations.archetypes import FolderZipRepresentation
from StringIO import StringIO
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import Interface


class WorkspaceZipRepresentation(FolderZipRepresentation):
    implements(IZipRepresentation)
    adapts(IWorkspace, Interface)

    def get_files(self, path_prefix=u"", recursive=True, toplevel=True):
        filename = u'{0}.pdf'.format(self.context.getId())

        assembler = getMultiAdapter((self.context, self.request),
                                    IPDFAssembler)

        yield (u'{0}/{1}'.format(path_prefix, filename),
               StringIO(assembler.build_pdf()))

        # Recursively export folder contents.
        folder_contents = super(WorkspaceZipRepresentation, self).get_files(
            path_prefix, recursive, toplevel)

        for item in folder_contents:
            yield item
