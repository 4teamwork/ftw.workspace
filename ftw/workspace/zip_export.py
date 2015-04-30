from ftw.pdfgenerator.interfaces import IPDFAssembler
from ftw.workspace import arbeitsraumMessageFactory as _
from ftw.workspace.export import get_header, get_data, create_xlsx
from ftw.workspace.interfaces import IWorkspace
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.representations.archetypes import FolderZipRepresentation
from Products.CMFPlone.utils import safe_unicode
from StringIO import StringIO
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.i18n import translate
from zope.interface import implements
from zope.interface import Interface


class WorkspaceZipRepresentation(FolderZipRepresentation):
    implements(IZipRepresentation)
    adapts(IWorkspace, Interface)

    def get_files(self, path_prefix=u"", recursive=True, toplevel=True):
        """
        Returns a list of two-value-tuples having the following values:
        - a relative path under which the file should show up in the zip
        - the data as either a file or a stream
        """
        filename = '{0}.pdf'.format(self.context.getId())

        assembler = getMultiAdapter((self.context, self.request),
                                    IPDFAssembler)

        yield (u'{0}/{1}'.format(safe_unicode(path_prefix),
                                 safe_unicode(filename)),
               StringIO(assembler.build_pdf()))

        header = get_header(self.context)
        data = get_data(self.context)
        xlsx = create_xlsx(header, data)

        filename = translate(
            _(u'participants_export_filename', default=u'participants.xlsx'),
            context=self.request
        )

        yield (u'{0}/{1}'.format(safe_unicode(path_prefix),
                                 safe_unicode(filename)), xlsx)
        
        # Recursively export folder contents.
        folder_contents = super(WorkspaceZipRepresentation, self).get_files(
            path_prefix, recursive, toplevel)

        for item in folder_contents:
            yield item
