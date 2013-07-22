from datetime import datetime
from datetime import timedelta
from plone.memoize import ram
from Products.Archetypes.utils import OrderedDict
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
import os.path


def icon(item, value):
    if not item.getIcon:
        return ''
    url_method = lambda: '#'
    site = getSite()
    props = getToolByName(site, 'portal_properties')
    portal_url = getToolByName(site, 'portal_url')
    item_type = item.portal_type
    ftw_worspace = props.get('ftw.workspace_properties', None)
    if not ftw_worspace:
        # fallback
        direct_downloadable_types = ['File', ]
    else:
        direct_downloadable_types = ftw_worspace.getProperty(
            'direct_downloadable_types',
            ['File', ])
    if hasattr(item, 'getURL'):
        url_method = item.getURL
    elif hasattr(item, 'absolute_url'):
        url_method = item.absolute_url
    has_file = item_type in direct_downloadable_types
    # use a icon
    img = u'<img src="%s/%s"/>' % (portal_url(), item.getIcon)

    # link it with either the download (usually "file" field) or with
    # the content default view
    href = url_method()
    if has_file:
        href = os.path.join(href, 'at_download', 'file')
    elif hasattr(item, 'portal_type'):
        # do we need to add /view ?

        types_using_view = props.get('site_properties').getProperty(
            'typesUseViewActionInListings')
        if item_type in types_using_view:
            href = os.path.join(href, 'view')

    return u'<a href="%s">%s</a>' % (href.decode('utf8'), img)


@ram.cache(lambda m, i, author: author)
def readable_author(item, author):
    #TODO: terribly inefficient. Make some HelperCommons or something
    site = getSite()
    portal_url = getToolByName(site, 'portal_url')
    if not author:
        return '-'
    name = author
    user = site.acl_users.getUserById(author)
    url = None
    if user is not None:
        name = user.getProperty('fullname', author)
        if not len(name):
            name = author
    if user is None:
        url, name = find_contact_object(item, author)
    if url is None:
        url = "%s/author/%s" % (portal_url(), author)
    return '<a href="%s">%s</a>' % (url, name)


def find_contact_object(item, id_):
    item = item.getObject()
    current = item.aq_inner.aq_explicit
    while current.aq_parent.Type() in ['Workspace']:
        current = current.aq_parent
    brains = item.portal_catalog(id=id_,
                                 Type='Contact',
                                 path='/'.join(current.getPhysicalPath()))
    if len(brains):
        return brains[0].getURL(), brains[0].Title
    return None, id_


def responsible(item, value):
    return ','.join(
        [readable_author(item, r)
            for r in item.getObject().getResponsibility()])


def group_by_date(results):
    grouped_results = OrderedDict()
    grouped_results['today'] = []
    grouped_results['yesterday'] = []
    grouped_results['this_week'] = []
    grouped_results['this_month'] = []
    grouped_results['older'] = []

    today = datetime.today().day
    yesterday = (datetime.today() - timedelta(1)).day
    this_week = int(datetime.today().strftime("%V"))  # isoweek
    this_month = datetime.today().month
    this_year = datetime.today().year

    for result in results:
        modified = result.modified
        if modified.month() == this_month and modified.year() == this_year:
            if modified.day() == today:
                grouped_results['today'].append(result)
            elif modified.day() == yesterday:
                grouped_results['yesterday'].append(result)
            elif int(modified.strftime("%V")) == this_week:
                grouped_results['this_week'].append(result)
            else:
                grouped_results['this_month'].append(result)
        else:
            grouped_results['older'].append(result)
    return grouped_results.items()

