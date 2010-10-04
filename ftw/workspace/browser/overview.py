from Products.Five.browser import BrowserView
from ftw.workspace.browser import helper as workspace_helper

class OverviewTab(BrowserView):

    def catalog(self, types, depth=2, sort_on='modified', sort_order='reverse'):
        return self.context.portal_catalog(
            portal_type=types,
            path=dict(depth=depth,
                      query='/'.join(self.context.getPhysicalPath())),
            sort_on=sort_on,
            sort_order=sort_order)

    def folders(self):
        # import pdb; pdb.set_trace( )
        subfolders = []
        folderobjects = []
        all_folders = self.catalog(
            ['Folder', 'Workspace', 'TabbedViewFolder'], depth=1,
            sort_on = 'sortable_title', sort_order = '')
        return all_folders

    def blogs(self):
        return self.catalog(['Blog', ])

    def description(self):
        return self.context.Description()

    def files(self):
        # import pdb; pdb.set_trace( )
        return self.catalog(['File', ], sort_on='created')[:5]

    def recently_modified(self):
        return self.catalog(['Document', 'Folder',
                             'Workspace', 'Event', ],
                            sort_on='created')[:5]
    def get_icon(self, document):
        return workspace_helper.icon(document, "")
    def get_description(self, file):
        return file.getObject().Description()