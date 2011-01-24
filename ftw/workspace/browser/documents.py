from tab import Tab
from ftw.table import helper
from ftw.workspace.browser import helper as workspace_helper
from ftw.workspace import _


class DocumentsTab(Tab):

    types = ['File', 'Document']

    sort_on = 'modified'

    columns = (#('', helper.path_checkbox),
               {'column':'getContentType',
                'column_title': _(u'column_type', default=u'Type'),
                'transform': workspace_helper.icon},
               {'column':'Title',
                'collumn_title': _(u'column_title', default=u'Title'),
                'sort_index':'sortable_title',
                'transform': helper.linked_without_icon},
               {'column':'date',
                'column_title': _(u'column_date', default=u'date'),
                'transform': helper.readable_date},
               {'column':'modified',
                'column_title': _(u'column_modified', default=u'modified'),
                'transform': helper.readable_date},
               {'column':'Creator',
                'column_title': _(u'column_creator', default=u'Creator'),
                'sort_index':'sortable_creator',
                'transform': helper.readable_author}, )
