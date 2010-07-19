from Products.Five.browser import BrowserView
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


class OverviewTab(BrowserView):

    template = ViewPageTemplateFile('overview.pt')

    def get_css_classes(self):
        return 'mylist'

    def catalog(self, types, depth=2, sort_on = 'modified'):
        return self.context.portal_catalog(
            portal_type=types,
            path=dict(
                depth=depth,
                query='/'.join(self.context.getPhysicalPath())),
                sort_on=sort_on,
                sort_order='reverse')

    def boxes(self):
        items = [[dict(id = 'folders', content=self.folders(), type_='list'),
                  dict(id = 'blogs', content=self.blogs()),
                  dict(id='description', content=self.description()), ],
                  [dict(id ='documents', content=self.documents()),
                  dict(id='recently_modified',
                        content=self.recently_modified()),
                ]]
        return items

    def folders(self):
        return self.catalog(['Folder', 'Workspace', ])

    def blogs(self):
        return self.catalog(['Blog', ])

    def description(self):
        return self.context.Description()

    def documents(self):
        return self.catalog(['File', ], sort_on='created', )[:5]

    def recently_modified(self):
        return self.catalog(['File', 'Folder',
                            'Workspace', 'Event', ],
                            sort_on='created', )[:5]
