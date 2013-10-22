from DateTime import DateTime
from ftw.tabbedview.browser import listing
from ftw.table import helper as table_helper
from ftw.workspace import _
from ftw.workspace.browser import helper
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import datetime


class ListingHelper(object):

    def get_description(self, file_):
        description = file_.getObject().Description()
        # make sure there is no html in description
        transforms = getToolByName(self.context, 'portal_transforms')
        result = transforms.convertTo('text/plain', description)
        if result is None:
            return ''
        else:
            return result.getData()

    def type_class(self, brain):
        """ Returns the contenttype or mimetype class for sprites.
        """
        plone_utils = getToolByName(self.context, 'plone_utils')
        if not brain.getIcon:
            return 'contenttype-' + plone_utils.normalizeString(
                brain.portal_type)
        return ''

    def get_icon(self, document):
        return helper.icon(document, "")


class OverviewTab(listing.CatalogListingView, ListingHelper):
    """Overview tab for workspace"""

    overview_template = ViewPageTemplateFile("overview.pt")
    sort_on = 'modified'
    sort_reverse = True
    show_menu = False
    show_selects = False

    columns = ({'column': 'Title',
                'sort_index': 'sortable_title',
                'column_title': _(u'label_eventstab_title'),
                'transform': table_helper.linked},

               {'column': 'modified',
                'column_title': _(u'column_modified',
                                  default=u'modified'),
                'transform': table_helper.readable_date},

               {'column': 'Creator',
                'sort_index': 'sortable_creator',
                'column_title': _(u'label_eventstab_creator'),
                'transform': helper.readable_author}, )

    def __init__(self, context, request):
        super(OverviewTab, self).__init__(context, request)
        catalog = getToolByName(self.context, 'portal_catalog')

        if 'searchable_text' in self.request:
            searchable_text = self.request.get('searchable_text')
            if len(searchable_text):
                kwargs = {}

                if not searchable_text.endswith('*'):
                    searchable_text += '*'

                kwargs['SearchableText'] = searchable_text
                kwargs['sort_on'] = 'modified'
                kwargs['sort_order'] = 'reverse'
                results = catalog(
                    path='/'.join(self.context.getPhysicalPath()), **kwargs)
                self.contents = helper.group_by_date(results)

    def template(self):
        if self.filter_text != '':
            return super(OverviewTab, self).template()
        else:
            return self.overview_template()

    def catalog(self, types=None, depth=-1, sort_on='modified',
                sort_order='reverse'):

        query = dict(
            path=dict(
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
            sort_on='getObjPositionInParent', sort_order='')
        return all_folders

    def description(self):
        return self.context.Description()

    def recently_modified(self):
        return self.catalog()[:10]

    def show_search_results(self):
        if 'searchable_text' in self.request:
            searchable_text = self.request.get('searchable_text')
            return bool(len(searchable_text))
        return False

    def generate_date(self, datetimestring, now=None):
        if now is None:
            now = datetime.datetime.now()

        today = now.day
        yesterday = (now - datetime.timedelta(1)).day
        this_month = now.month
        this_year = now.year

        modified = DateTime(datetimestring)
        if modified.month() == this_month and modified.year() == this_year:
            if modified.day() == today:
                return _(u'label_today', default=u'Today, ${time}',
                         mapping={'time': modified.strftime('%H:%M')})

            elif modified.day() == yesterday:
                return _(u'label_yesterday', u'Yesterday, ${time}',
                         mapping={'time': modified.strftime('%H:%M')})
            else:
                return modified.strftime('%d.%m.%Y')
        else:
            return modified.strftime('%d.%m.%Y')

    def translate_readable_date(self, value):
        return helper.translate_state(self.context, value)

    def readable_author(self, item, author):
        return helper.readable_author(item, author)

    def render_sublisting(self):
        return self.context.restrictedTraverse('@@overview_sublisting')()
