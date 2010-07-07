from Products.Five.browser import BrowserView
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility

from ftw.tabbedview.browser.views import views
from ftw.table import helper
from ftw.table.interfaces import ITableGenerator
from ftw.workspace.browser import helper as workspace_helper
from ftw.workspace import _

class GetOwnershipView(BrowserView):

    def __call__(self):
        userid = self.context.getOwner(0).getId()
        return userid and userid or ''


class ArbeitsraeumeView(views.TabbedView):
    show_searchform = True

    def get_tabs(self):
        return [{'id':'Arbeitsraeume', 'class':''},
                {'id':'Tasks','class':''},
                {'id':'Documents','class':''},
                {'id':'Meetings','class':''},
               ]


class MyListing(views.BaseListingView):
    show_searchform = True
    columns = (
               ('Title', 'sortable_title', workspace_helper.workspace_linked),
              ('modified', helper.readable_date),
               ('Creator', helper.readable_author),
              ('', workspace_helper.delete_action),
               )
    sort_on = 'sortable_title'
    sort_order = 'reverse'
    
    custom_sort_indexes = {'Products.PluginIndexes.DateIndex.DateIndex': workspace_helper.custom_sort}
    
    table = ViewPageTemplateFile('table.pt')
    
    def update(self):
        super(MyListing, self).update()
        self.pagesize = 50
        #old izug batching still uses b_start instead of self.pagenumber
        self.pagenumber = int(self.request.get('b_start', 0))/self.pagesize+1

    def render_listing(self):
        generator = queryUtility(ITableGenerator, 'ftw.tablegenerator')
        return generator.generate(self.batch,
                                  self.columns,
                                  sortable=True,
                                  selected=(self.sort_on, self.sort_order),
                                  template = self.table,
                                  auto_count = self.auto_count,
                                  css_mapping = dict(table='sortable-table')
                                  )


# different views for the tabbed_view

# overview-tab
class OverviewTab(BrowserView):
    #TODO: refactor view using viewlets
    def catalog(self, types, depth=2, sort_on = 'modified'):
        return self.context.portal_catalog(portal_type=types,
                                           path=dict(depth=depth,
                                                     query='/'.join(self.context.getPhysicalPath())
                                                     ),
                                           sort_on=sort_on,
                                           sort_order='reverse')

    def boxes(self):
        items = [[dict(id = 'folders', content=self.folders()),
                  dict(id = 'blogs', content=self.blogs()),
                  dict(id='description', content=self.description()),],
                  [dict(id ='documents', content=self.documents()),
                  dict(id='recently_modified', content=self.recently_modified()),
                ]]

        return items


    def folders(self):
        return self.catalog(['Folder', 'Workspace',])

    def boxes(self):
        return self.catalog(['Blog',])

    def description(self):
        return self.context.getDescription()

    def documents(self):
        return self.catalog(['File',], sort_on='created',)[:5]

    def recently_modified(self):
        return self.catalog(['File', 'Folder', 'Workspace', 'Event', ], sort_on='created',)[:5]


#Document-tab
class Documents(MyListing):
   types = 'File'
   
   sort_on = 'modified'
   
   columns = (
              ('Typ', 'getContentType', workspace_helper.icon),
              ('Title', 'sortable_title', workspace_helper.workspace_files_linked),
              ('modified', helper.readable_date),
              ('Creator', helper.readable_author),
              ('', workspace_helper.delete_action),
              )

def translate(item, value):
    return _(value.encode())


class Meetings(MyListing):
    types = 'Meeting'

    sort_on = 'start'

    columns = (
               ('start', helper.readable_date),
               ('Title', 'sortable_title', izug_linked),
               ('getMeeting_type', translate),
               ('Responsible', 'sortable_responsibility', meeting_responsible),
               ('', delete_action),
              )

class Tasks(MyListing):
   types = 'Task'
   
   sort_on = 'end'
   
   columns = (
              ('Title', 'sortable_title', workspace_helper.workspace_linked),
              ('end', helper.readable_date),
              ('Responsible', 'sortable_responsibility', workspace_helper.responsible),
              ('State','review_state', workspace_helper.review_state),
              ('Creator', helper.readable_author),
              ('', workspace_helper.delete_action),
              )

class EventsViewCalendar(BaseListingView):
    types = ['Meeting', ]

    #_template = ViewPageTemplateFile('arbeitsraum_view-events-calendar')
    def __init__(self, context, request):
        context = aq_inner(context)
        self.context = context
        self.request = request
        self.calendar = getToolByName(context, 'portal_calendar')
        self._ts = getToolByName(context, 'translation_service')
        self.url_quote_plus = url_quote_plus

        self.now = localtime()
        self.yearmonth = yearmonth = self.getYearAndMonthToDisplay()
        self.year = year = yearmonth[0]
        self.month = month = yearmonth[1]

        self.showPrevMonth = yearmonth > (self.now[0]-1, self.now[1])
        self.showNextMonth = yearmonth < (self.now[0]+1, self.now[1])

        self.prevMonthYear, self.prevMonthMonth = self.getPreviousMonth(year, month)
        self.nextMonthYear, self.nextMonthMonth = self.getNextMonth(year, month)

        self.monthName = PLMF(self._ts.month_msgid(month),
                            default=self._ts.month_english(month))

    def render(self):
        return xhtml_compress(self._template())

    def getEventsForCalendar(self):
        context = aq_inner(self.context)
        year = self.year
        month = self.month
        weeks = self.calendar.getEventsForCalendar(month, year, path='/'.join(context.getPhysicalPath()))
        for week in weeks:
            for day in week:
                daynumber = day['day']
                if daynumber == 0:
                    continue
                day['is_today'] = self.isToday(daynumber)
                if day['event']:
                    cur_date = DateTime(year, month, daynumber)
                    localized_date = [self._ts.ulocalized_time(cur_date, context=context, request=self.request)]
                    day['eventstring'] = '\n'.join(localized_date+[self.getEventString(e) for e in day['eventslist']])
                    day['date_string'] = '%s-%s-%s' % (year, month, daynumber)
                    day['date_string_search'] = '%s-%s-%s' % (year, (len(str(month)) ==1 and '0%s'%month or month), daynumber)

        return weeks

    def getEventString(self, event):
        start = event['start'] and ':'.join(event['start'].split(':')[:2]) or ''
        end = event['end'] and ':'.join(event['end'].split(':')[:2]) or ''
        title = safe_unicode(event['title']) or u'event'

        if start and end:
            eventstring = "%s-%s %s" % (start, end, title)
        elif start: # can assume not event['end']
            eventstring = "%s - %s" % (start, title)
        elif event['end']: # can assume not event['start']
            eventstring = "%s - %s" % (title, end)
        else: # can assume not event['start'] and not event['end']
            eventstring = title

        return '<p>'+eventstring+'</p>'

    def getYearAndMonthToDisplay(self):
        session = None
        request = self.request

        # First priority goes to the data in the REQUEST
        year = request.get('year', None)
        month = request.get('month', None)

        # Next get the data from the SESSION
        if self.calendar.getUseSession():
            session = request.get('SESSION', None)
            if session:
                if not year:
                    year = session.get('calendar_year', None)
                if not month:
                    month = session.get('calendar_month', None)

        # Last resort to today
        if not year:
            year = self.now[0]
        if not month:
            month = self.now[1]

        year, month = int(year), int(month)

        # Store the results in the session for next time
        if session:
            session.set('calendar_year', year)
            session.set('calendar_month', month)

        # Finally return the results
            return year, month

    def getPreviousMonth(self, year, month):
        if month==0 or month==1:
            month, year = 12, year - 1
        else:
            month-=1
        return (year, month)

    def getNextMonth(self, year, month):
        if month==12:
            month, year = 1, year + 1
        else:
            month+=1
        return (year, month)

    def getWeekdays(self):
        """Returns a list of Messages for the weekday names."""
        weekdays = []
        # list of ordered weekdays as numbers
        for day in self.calendar.getDayNumbers():
            weekdays.append(PLMF(self._ts.day_msgid(day, format='s'),
                                 default=self._ts.weekday_english(day, format='a')))

        return weekdays

    def isToday(self, day):
        """Returns True if the given day and the current month and year equals
         today, otherwise False.
        """
        return self.now[2]==day and self.now[1]==self.month and \
             self.now[0]==self.year

    def getReviewStateString(self):
        states = self.calendar.getCalendarStates()
        return ''.join(map(lambda x: 'review_state=%s&amp;' % self.url_quote_plus(x), states))

    def getQueryString(self):
        request = self.request
        query_string = request.get('orig_query',
                                 request.get('QUERY_STRING', None))
        if len(query_string) == 0:
            query_string = ''
        else:
            query_string = '%s&amp;' % query_string
        return query_string
