from ftw.tabbedview.browser.tabbed import TabbedView
from ftw.table import helper
from tab import Tab


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

    columns = (('', helper.path_checkbox),
               ('Title', 'sortable_title', helper.linked),
               ('modified', helper.readable_date),
               ('Creator', 'sortable_creator', helper.readable_author), )
