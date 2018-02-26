from ftw.workspace.content.folder import ITabbedViewFolder
from ftw.workspace.content.workspace import IWorkspace
from ftw.zipextract.factory_type_decider import DefaultFactoryTypeDecider
from zope.component import adapter
from zope.interface import Interface


@adapter(IWorkspace, Interface)
class WorkspaceFactoryTypeDecider(DefaultFactoryTypeDecider):

    folder_type = "TabbedViewFolder"


@adapter(ITabbedViewFolder, Interface)
class TabbedViewFolderFactoryTypeDecider(DefaultFactoryTypeDecider):

    folder_type = "TabbedViewFolder"
