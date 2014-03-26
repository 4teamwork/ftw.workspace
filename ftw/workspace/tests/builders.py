from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder


class WorkspaceBuilder(ArchetypesBuilder):
    portal_type = 'Workspace'


class TabbedViewFolderBuilder(ArchetypesBuilder):
    portal_type = 'TabbedViewFolder'


builder_registry.register('workspace', WorkspaceBuilder)
builder_registry.register('TabbedViewFolder', TabbedViewFolderBuilder)
