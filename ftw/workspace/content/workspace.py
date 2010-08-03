"""Definition of the Workspace content type
"""

from AccessControl import ClassSecurityInfo
from ftw.workspace.config import PROJECTNAME
from ftw.workspace.content.schemata import finalizeWorkspaceSchema
from ftw.workspace.interfaces import IWorkspace
from Products.Archetypes import atapi
from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName
from zope.component import adapter
from zope.interface import implements


WorkspaceSchema = folder.ATFolderSchema.copy()

# FIXME: move to egov.workspace?
WorkspaceSchema = finalizeATCTSchema(WorkspaceSchema,
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
                                                    'Editor', 'Reader']


class Workspace(folder.ATFolder):
    """A type for collaborative spaces."""
    implements(IWorkspace)

    portal_type = "Workspace"
    schema = WorkspaceSchema

    security = ClassSecurityInfo()

atapi.registerType(Workspace, PROJECTNAME)
