from Products.Five.browser import BrowserView
from ftw.workspace.browser import helper as workspace_helper

class OverviewTab(BrowserView):

    def catalog(self, types, depth=2, sort_on='modified'):
        return self.context.portal_catalog(
            portal_type=types,
            path=dict(depth=depth,
                      query='/'.join(self.context.getPhysicalPath())),
            sort_on=sort_on,
            sort_order='reverse')

    def folders(self):
        # import pdb; pdb.set_trace( )
        subfolders = []
        all_folders = self.catalog(
            ['Folder', 'Workspace', 'TabbedViewFolder'],
            sort_on='created')[:-1]
        for item in all_folders:
            folderObject = item.getObject()
            if folderObject.getParentNode() == self.context:
                subfolders.append(item)
        return subfolders
    def blogs(self):
        return self.catalog(['Blog', ])

    def description(self):
        return self.context.Description()

    def documents(self):
        # import pdb; pdb.set_trace( )
        return self.catalog(['Document', ], sort_on='created')[:5]

    def recently_modified(self):
        return self.catalog(['Document', 'Folder',
                             'Workspace', 'Event', ],
                            sort_on='created')[:5]
    def get_icon(self, document):
        return workspace_helper.icon(document, "")
