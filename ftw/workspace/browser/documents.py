from tab import Tab
from ftw.table import helper
from ftw.workspace.browser import helper as workspace_helper


class DocumentsTab(Tab):

    types = 'File'

    sort_on = 'modified'

    columns = (('', helper.path_checkbox),
               ('Typ', 'getContentType', workspace_helper.icon),
               ('Title', 'sortable_title', helper.linked),
               ('modified', helper.readable_date),
               ('Creator', 'sortable_creator', helper.readable_author), )
