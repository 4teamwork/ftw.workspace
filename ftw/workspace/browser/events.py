from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.PythonScripts.standard import url_quote_plus
from ftw.tabbedview.browser import listing
from ftw.table import helper
from ftw.workspace import _
from plone.memoize.compress import xhtml_compress
from time import localtime
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.i18nmessageid import MessageFactory


plone_locales_mf = MessageFactory('plonelocales')


class EventsTab(listing.CatalogListingView):
    types = ['Meeting', 'Poodle']

    sort_on = 'start'
    sort_order = 'reverse'

    columns = (#('', helper.path_checkbox),
               {'column': 'start',
                'column_index': 'start',
                'column_title': _(u'label_eventstab_start'),
                'transform': helper.readable_date},

               {'column': 'Title',
                'column_index': 'sortable_title',
                'column_title': _(u'label_eventstab_title'),
                'transform': helper.linked},


               {'column': 'getMeeting_type',
                'column_title': _(u'label_eventstab_type',
                                  default=u'Type'),
                'transform': helper.translated_string('ftw.workspace')},


                {'column': 'Creator',
                 'column_index': 'sortable_creator',
                 'column_title': _(u'label_eventstab_creator'),
                 'transform': helper.readable_author},)

    template = ViewPageTemplateFile('events.pt')


class EventsCalendarTab(listing.CatalogListingView):
    types = ['Meeting']

    template = ViewPageTemplateFile('eventscalendar.pt')

    def __init__(self, context, request):

        super(EventsCalendarTab, self).__init__(context, request)

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

        self.showPrevMonth = yearmonth > (self.now[0] - 1, self.now[1])
        self.showNextMonth = yearmonth < (self.now[0] + 1, self.now[1])

        (self.prevMonthYear,
         self.prevMonthMonth) = self.getPreviousMonth(year, month)

        (self.nextMonthYear,
         self.nextMonthMonth) = self.getNextMonth(year, month)

        self.monthName = plone_locales_mf(
            self._ts.month_msgid(month),
            default=self._ts.month_english(month))

    def render(self):
        return xhtml_compress(self._template())

    def getEventsForCalendar(self):
        context = aq_inner(self.context)
        year = self.year
        month = self.month
        weeks = self.calendar.getEventsForCalendar(
            month,
            year,
            path='/'.join(context.getPhysicalPath()))

        for week in weeks:
            for day in week:
                daynumber = day['day']
                if daynumber == 0:
                    continue
                day['is_today'] = self.isToday(daynumber)
                if day['event']:
                    cur_date = DateTime(year, month, daynumber)
                    localized_date = [self._ts.ulocalized_time(
                            cur_date,
                            context=context,
                            request=self.request)]
                    day['eventstring'] = '\n'.join(
                        localized_date +
                        [self.getEventString(e)
                         for e in day['eventslist']])
                    day['date_string'] = '%s-%s-%s' % (year, month, daynumber)
                    day['date_string_search'] = '%s-%s-%s' % (
                        year,
                        str(month).rjust(2, '0'),
                        str(daynumber).rjust(2, '0'))
        return weeks

    def getEventString(self, event):
        start = event['start'] and \
            ':'.join(event['start'].split(':')[:2]) or ''
        end = event['end'] and ':'.join(event['end'].split(':')[:2]) or ''
        title = safe_unicode(event['title']) or u'event'

        if start and end:
            eventstring = "%s-%s %s" % (start, end, title)
        elif start:  # can assume not event['end']
            eventstring = "%s - %s" % (start, title)
        elif event['end']:  # can assume not event['start']
            eventstring = "%s - %s" % (title, end)
        else:  # can assume not event['start'] and not event['end']
            eventstring = title

        return '<p>' + eventstring + '</p>'

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
        if month == 0 or month == 1:
            month, year = 12, year - 1
        else:
            month -= 1
        return (year, month)

    def getNextMonth(self, year, month):
        if month == 12:
            month, year = 1, year + 1
        else:
            month += 1
        return (year, month)

    def getWeekdays(self):
        """Returns a list of Messages for the weekday names."""
        weekdays = []
        # list of ordered weekdays as numbers
        for day in self.calendar.getDayNumbers():
            weekdays.append(
                plone_locales_mf(
                    self._ts.day_msgid(day).decode('utf-8'),
                    default=self._ts.weekday_english(
                        day).decode('utf-8')))
        return weekdays

    def isToday(self, day):
        """Returns True if the given day and the current
        month and year equals today, otherwise False.

        """
        return self.now[2] == day and self.now[1] == self.month and \
            self.now[0] == self.year

    def getReviewStateString(self):
        states = self.calendar.getCalendarStates()
        return ''.join(map(lambda x: 'review_state=%s&amp;' % \
                               self.url_quote_plus(x), states))

    def getQueryString(self):
        request = self.request
        query_string = request.get('orig_query',
                                   request.get('QUERY_STRING', None))
        if len(query_string) == 0:
            query_string = ''
        else:
            query_string = '%s&amp;' % query_string
        return query_string
