"""Definition of the Workspace content type
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content import folder
from Products.Archetypes import atapi
from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.CMFCore.utils import getToolByName
from ftw.workspace import _
from ftw.workspace.config import PROJECTNAME
from ftw.workspace.content.schemata import finalizeWorkspaceSchema
from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.utils import get_creator_fullname
from ftw.workspace.utils import TinyMCEAllowedButtonsConfigurator
from plone.registry.interfaces import IRegistry
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implements


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
            allow_file_upload=False,
            allow_buttons=TinyMCEAllowedButtonsConfigurator(),
        ),
    ),
))


finalizeWorkspaceSchema(WorkspaceSchema,
                        folderish=True,
                        moveDiscussion=False)


@adapter(IWorkspace, IObjectInitializedEvent)
def workspace_added(workspace, event):
    """When a workspace is created, we add additional local roles
    to enable the creator to delegate them.
    """
    pm_tool = getToolByName(workspace, 'portal_membership')
    current_user = pm_tool.getAuthenticatedMember().getId()
    roles = workspace.get_local_roles_for_userid(current_user)
    if not roles:
        return

    registry = getUtility(IRegistry)
    roles = tuple(set(roles) | set(registry['ftw.workspace.auto_roles']))
    workspace.manage_setLocalRoles(current_user, roles)


class Workspace(folder.ATFolder):
    """A type for collaborative spaces."""
    implements(IWorkspace)

    portal_type = "Workspace"
    schema = WorkspaceSchema

    security = ClassSecurityInfo()

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        return False

    security.declarePublic('SearchableText')
    def SearchableText(self):
        fullname = get_creator_fullname(self)
        return ' '.join((super(Workspace, self).SearchableText(), fullname))

atapi.registerType(Workspace, PROJECTNAME)
