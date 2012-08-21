from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content import folder
from Products.Archetypes import atapi
from ftw.workspace.config import PROJECTNAME
from ftw.workspace.interfaces import ITabbedViewFolder
from zope.interface import implements


class TabbedViewFolder(folder.ATFolder):
    implements(ITabbedViewFolder)

    security = ClassSecurityInfo()

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        return False


atapi.registerType(TabbedViewFolder, PROJECTNAME)
