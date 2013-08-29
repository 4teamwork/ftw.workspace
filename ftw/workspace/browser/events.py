from ftw.tabbedview.browser import listing
from ftw.table import helper
from ftw.workspace import _
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18nmessageid import MessageFactory
from Products.Five.browser import BrowserView


plone_locales_mf = MessageFactory('plonelocales')


class EventsTab(listing.CatalogListingView):
    types = ['Meeting', 'Poodle', 'Event']

    sort_on = 'start'
    sort_order = 'reverse'

    show_selects = False
    show_menu = False

    columns = ({'column': 'start',
                'column_index': 'start',
                'column_title': _(u'label_eventstab_start'),
                'transform': helper.readable_date_text,
                'width': 80},

               {'column': 'Title',
                'column_index': 'sortable_title',
                'column_title': _(u'label_eventstab_title'),
                'sort_index': 'sortable_title',
                'transform': helper.linked},


               {'column': 'getMeeting_type',
                'column_title': _(u'label_eventstab_type',
                                  default=u'Type'),
                'transform': helper.translated_string('ftw.meeting'),
                'width': 80},


               {'column': 'Creator',
                'column_index': 'sortable_creator',
                'column_title': _(u'label_eventstab_creator'),
                'transform': helper.readable_author}, )

    template = ViewPageTemplateFile('events.pt')


class EventsCalendarTab(BrowserView):

    template = ViewPageTemplateFile('eventscalendar.pt')
    types = []

    def __init__(self, *args, **kwargs):
        super(EventsCalendarTab, self).__init__(*args, **kwargs)
        self.js_config = None

    def __call__(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        self.js_config = portal.unrestrictedTraverse('ftwcalendar_config.js')()
        return self.template()
