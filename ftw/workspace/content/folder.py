from AccessControl import ClassSecurityInfo
from ftw.workspace.config import PROJECTNAME
from ftw.workspace.content.schemata import finalizeWorkspaceSchema
from ftw.workspace.interfaces import ITabbedViewFolder
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from zope.interface import implements

schema = folder.ATFolder.schema.copy()

finalizeWorkspaceSchema(schema)


class TabbedViewFolder(folder.ATFolder):
    implements(ITabbedViewFolder)

    schema = schema

    security = ClassSecurityInfo()

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        return False


atapi.registerType(TabbedViewFolder, PROJECTNAME)
