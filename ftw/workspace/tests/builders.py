from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder
from StringIO import StringIO


class WorkspaceBuilder(ArchetypesBuilder):
    portal_type = 'Workspace'


class TabbedViewFolderBuilder(ArchetypesBuilder):
    portal_type = 'TabbedViewFolder'


class ImageBuilder(ArchetypesBuilder):

    portal_type = 'Image'

    def attach_image_containing(self, iocontent, name="test.gif"):
        iocontent.filename = name
        self.attach(iocontent)
        return self

    def attach(self, image):
        self.arguments['image'] = image
        return self

    def with_dummy_content(self):
        data = StringIO(
            'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00'
            '\x00!\xf9\x04\x04\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00'
            '\x01\x00\x00\x02\x02D\x01\x00;')

        self.attach_image_containing(data)
        return self


builder_registry.register('workspace', WorkspaceBuilder)
builder_registry.register('TabbedViewFolder', TabbedViewFolderBuilder)
builder_registry.register('image', ImageBuilder)
