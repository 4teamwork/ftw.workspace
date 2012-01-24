from ftw.workspace import _
from ftw.workspace.browser import helper
from ftw.table import helper as table_helper
from ftw.tabbedview.browser import listing
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class OverviewTab(listing.CatalogListingView):

    overview_template = ViewPageTemplateFile("overview.pt")
    sort_on = 'modified'
    sort_reverse = True
    columns = (#('', helper.path_checkbox),
               {'column': 'Title',
                'column_index': 'sortable_title',
                'column_title': _(u'label_eventstab_title'),
                'transform': table_helper.linked},

               {'column': 'modified',
                'column_title': _(u'column_modified',
                                  default=u'modified'),
                'transform': table_helper.readable_date},

                {'column': 'Creator',
                 'column_index': 'sortable_creator',
                 'column_title': _(u'label_eventstab_creator'),
                 'transform': helper.readable_author}, )

    def update(self):
        self.load_request_parameters()
        if self.filter_text != '':
            self.show_search_results = True
            super(OverviewTab, self).update()

        else:
            self.show_search_results = False

    def template(self):
        if self.show_search_results:
            return super(OverviewTab, self).template()
        else:
            return self.overview_template()

    def catalog(self, types=[], depth=-1, sort_on='modified',
                sort_order='reverse'):

        query = dict(
            path = dict(
                depth=depth,
                query='/'.join(self.context.getPhysicalPath())),
            sort_on=sort_on,
            sort_order=sort_order)
        if types:
            query['portal_type'] = types

        return self.context.portal_catalog(query)

    def folders(self):
        all_folders = self.catalog(
            ['Folder', 'Workspace', 'TabbedViewFolder'], depth=1,
            sort_on = 'getObjPositionInParent', sort_order = '')
        return all_folders

    def description(self):
        return self.context.Description()

    def files(self):
        return self.catalog(['File', ], sort_on='created')[:5]

    def recently_modified(self):
        return self.catalog()[:5]

    def get_icon(self, document):
        return helper.icon(document, "")

    def get_description(self, file):
        return file.getObject().Description()
