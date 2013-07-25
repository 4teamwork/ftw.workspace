"""Definition of the Workspace content type
"""

from AccessControl import ClassSecurityInfo
from ftw.workspace import _
from ftw.workspace.config import PROJECTNAME
from ftw.workspace.content.schemata import finalizeWorkspaceSchema
from ftw.workspace.interfaces import IWorkspace
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from zope.interface import implements
from ftw.workspace.utils import TinyMCEAllowedButtonsConfigurator


WorkspaceSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.TextField(
        'text',
        searchable=True,
        required=False,
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_output_type='text/x-html-safe',
        default_input_type='text/html',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"label_text", default=u"Text"),
            rows=15,
            allow_buttons=TinyMCEAllowedButtonsConfigurator(),
        ),
    ),
))


finalizeWorkspaceSchema(WorkspaceSchema,
                        folderish=True,
                        moveDiscussion=False)


class Workspace(folder.ATFolder):
    """A type for collaborative spaces."""
    implements(IWorkspace)

    portal_type = "Workspace"
    schema = WorkspaceSchema

    security = ClassSecurityInfo()

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        return False

atapi.registerType(Workspace, PROJECTNAME)
