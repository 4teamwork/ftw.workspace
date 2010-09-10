from Products.Five.browser import BrowserView


class OverviewTab(BrowserView):

    def catalog(self, types, depth=2, sort_on='modified'):
        return self.context.portal_catalog(
            portal_type=types,
            path=dict(depth=depth,
                      query='/'.join(self.context.getPhysicalPath())),
            sort_on=sort_on,
            sort_order='reverse')

    def folders(self):
        return self.catalog(
            ['Folder', 'Workspace', 'TabbedViewFolder'],
            sort_on='created')[:-1]

    def blogs(self):
        return self.catalog(['Blog', ])

    def description(self):
        return self.context.Description()

    def documents(self):
        return self.catalog(['File', ], sort_on='created')[:5]

    def recently_modified(self):
        return self.catalog(['File', 'Folder',
                             'Workspace', 'Event', ],
                            sort_on='created')[:5]
