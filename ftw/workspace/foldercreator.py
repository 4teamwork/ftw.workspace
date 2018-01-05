from ftw.workspace.content.folder import ITabbedViewFolder
from ftw.workspace.content.workspace import IWorkspace
from ftw.zipextract.interfaces import IFolderCreator
from ftw.zipextract.implementations_base import ObjectCreatorBase
from zope.component import adapts
from zope.interface import implements


class FolderCreatorInWorkspace(ObjectCreatorBase):
    implements(IFolderCreator)
    adapts(IWorkspace)
    portal_type = "TabbedViewFolder"


class FolderCreatorInTabbedViewFolder(ObjectCreatorBase):
    implements(IFolderCreator)
    adapts(ITabbedViewFolder)
    portal_type = "TabbedViewFolder"
