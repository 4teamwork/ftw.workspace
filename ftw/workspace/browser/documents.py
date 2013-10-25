from ftw.table import helper
from ftw.workspace import _
from ftw.workspace.browser import helper as workspace_helper
from ftw.workspace.browser.tab import Tab
from ftw.workspace.utils import has_ftwfile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18nmessageid import MessageFactory


fileMF = MessageFactory('ftw.file')


class DocumentsTab(Tab):

    types = ['File', 'Document', 'Image']

    show_selects = False
    show_menu = False

    sort_reverse = True

    template = ViewPageTemplateFile('documents.pt')

    def __init__(self, context, request):
        super(DocumentsTab, self).__init__(context, request)
        # default implementation
        if has_ftwfile(self.context):
            # ftw.file implementation
            self.sort_on = 'documentDate'
        else:
            self.sort_on = 'effective'

    @property
    def columns(self):
        # default implementation
        date_column = {'column': 'effective',
                       'column_title': _(u'column_date', default=u'date'),
                       'transform': helper.readable_date_text,
                       'width': 100}
        # ftw.file implementation
        if has_ftwfile(self.context):
            date_column['column'] = 'documentDate'
            date_column['column_title'] = fileMF(u'label_document_date',
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
             'transform': helper.readable_date_text,
             'width': 80},
        )
        return columns
