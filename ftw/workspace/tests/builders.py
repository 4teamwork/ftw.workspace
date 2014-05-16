from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder


class WorkspaceBuilder(ArchetypesBuilder):
    portal_type = 'Workspace'


class TabbedViewFolderBuilder(ArchetypesBuilder):
    portal_type = 'TabbedViewFolder'


class MeetingBuilder(ArchetypesBuilder):
    portal_type = 'Meeting'


builder_registry.register('workspace', WorkspaceBuilder)
builder_registry.register('TabbedViewFolder', TabbedViewFolderBuilder)
builder_registry.register('meeting', MeetingBuilder)
