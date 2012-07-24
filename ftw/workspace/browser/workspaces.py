from ftw.tabbedview.browser.tabbed import TabbedView
from ftw.table import helper
from ftw.workspace.browser.tab import Tab
from ftw.workspace import _


class WorkspacesView(TabbedView):
    """Tabbed workspaces overview"""

    def get_tabs(self):
        return [{'id':'workspaces', 'class':''},
                {'id':'documents', 'class':''},
                {'id':'events', 'class':''},
               ]


class WorkspacesTab(Tab):

    types = 'Workspace'
    sort_on = 'sortable_title'
    show_selects = False
    show_menu = False

    columns = (
        {'column': 'Title',
         'column_title': _(u'column_title', default=u'Title'),
         'sort_index': 'sortable_title',
         'transform': helper.linked},

        {'column': 'modified',
         'column_title': _(u'column_modified', default=u'modified'),
         'transform': helper.readable_date,
         'width': 80},

         {'column': 'Creator',
          'column_title': _(u'column_creator', default=u'Creator'),
          'sort_index': 'sortable_creator',
          'transform': helper.readable_author}, )
