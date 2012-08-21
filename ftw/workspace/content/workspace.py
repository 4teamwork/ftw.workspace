"""Definition of the Workspace content type
"""

from AccessControl import ClassSecurityInfo
from ftw.workspace import _
from ftw.workspace.config import PROJECTNAME
from ftw.workspace.content.schemata import finalizeWorkspaceSchema
from ftw.workspace.interfaces import IWorkspace
from Products.Archetypes import atapi
from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.ATContentTypes.content import folder
from Products.CMFCore.utils import getToolByName
from zope.component import adapter
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

# FIXME: move to egov.workspace?
finalizeWorkspaceSchema(WorkspaceSchema,
                        folderish=True,
                        moveDiscussion=False)


@adapter(IWorkspace, IObjectInitializedEvent)
def workspace_added(object_, event):
    """When a workspace is created, we add additional local roles
    to enable the creator to delegate them.

    TODO: Check if this is still necessary.
    """
    pm_tool = getToolByName(object_, 'portal_membership')
    current_user = pm_tool.getAuthenticatedMember().getId()
    # Fix (PHa): Only set local roles for logged-in user,
    # if his/her id already has local roles
    if current_user in object_.__ac_local_roles__:
        object_.__ac_local_roles__[current_user] += ['Contributor',
                                                    'Editor',
                                                    'Reader',
                                                    'Administrator']


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
