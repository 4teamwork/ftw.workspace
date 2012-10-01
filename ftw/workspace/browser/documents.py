from ftw.workspace.browser.tab import Tab
from ftw.table import helper
from ftw.workspace.browser import helper as workspace_helper
from ftw.workspace import _

import pkg_resources
try:
    pkg_resources.get_distribution('ftw.file')
except pkg_resources.DistributionNotFound:
    HAS_FTWFILE = False
    pass
else:
    HAS_FTWFILE = True


class DocumentsTab(Tab):

    types = ['File', 'Document']

    show_selects = False
    show_menu = False

    sort_reverse = True

    def __init__(self, context, request):
        super(DocumentsTab, self).__init__(context, request)
        # default implementation
        if HAS_FTWFILE:
            # ftw.file implementation
            self.sort_on = 'documentDate'
        else:
            self.sort_on = 'effective'

    @property
    def columns(self):
        # default implementation
        date_column = {'column': 'effective',
                       'column_title': _(u'column_date', default=u'date'),
                       'transform': helper.readable_date,
                       'width': 100}
        # ftw.file implementation
        if HAS_FTWFILE:
            date_column['column'] = 'documentDate'
            date_column['column_title'] = _(u'column_document_date',
                                            default=u'Document date')

        columns = (
            {'column': 'getIcon',
             'sort_index': 'getContentType',
             'column_title': _(u'column_type', default=u'Type'),
             'transform': workspace_helper.icon,
             'width': 35},

            {'column': 'Title',
             'column_title': _(u'column_title', default=u'Title'),
             'sort_index': 'sortable_title',
             'transform': helper.link(icon=False, tooltip=True)},
        ) + (date_column,) + (  # Add variable date column
            {'column': 'Creator',
             'column_title': _(u'column_creator', default=u'Creator'),
             'sort_index': 'sortable_creator',
             'transform': helper.readable_author},

            {'column': 'modified',
             'column_title': _(u'column_modified', default=u'modified'),
             'transform': helper.readable_date,
             'width': 80},
        )
        return columns
