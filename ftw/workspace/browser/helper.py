from Products.CMFCore.utils import getToolByName
from plone.memoize import ram
from zope.app.component.hooks import getSite
import os.path


TASK_REVIEW_STATE_ICON = {
    'inactive': 'icon_status_offen.gif',
    'resolved': 'icon_status_freigegeben.gif',
    'active': 'icon_status_in_bearbeitung.gif'}

TASK_REVIEW_STATE_DEFAULT_ICON = 'icon_remove_box.gif'


def workspace_linked(item, value):
    url_method = lambda: '#'
    #item = hasattr(item, 'aq_explicit') and item.aq_explicit or item
    if hasattr(item, 'getURL'):
        url_method = item.getURL
    elif hasattr(item, 'absolute_url'):
        url_method = item.absolute_url
    if isinstance(value, str):
        value = unicode(value, 'utf-8')
    value = len(value) >= 47 and value[:47] + '...' or value
    link = u'<a href="%s">%s</a>' % (url_method(), value)
    return link


def workspace_files_linked(item, value):
    url_method = lambda: '#'
    #item = hasattr(item, 'aq_explicit') and item.aq_explicit or item
    if hasattr(item, 'getURL'):
        url_method = item.getURL
    elif hasattr(item, 'absolute_url'):
        url_method = item.absolute_url
    if isinstance(value, str):
        value = unicode(value, 'utf-8')
    value = len(value) >= 47 and value[:47] + '...' or value
    link = u'<a href="%s/view">%s</a>' % (url_method(), value)
    return link


def delete_action(item, value):
    url_method = lambda: '#'
    portal_url = getToolByName(getSite(), 'portal_url')
    if hasattr(item, 'getURL'):
        url_method = item.getURL
    elif hasattr(item, 'absolute_url'):
        url_method = item.absolute_url
    return """
<a href="%s/delete_confirmation?came_from=%s" class="arbeitsraum_delete_item">
<img src="%s/++resource++ftw.workspace-resources/icon_funktion_entfernen.gif"/>
</a>
""" % (url_method(),
       "%s#%s-tab" % (item.REQUEST.get('HTTP_REFERER'),
                      item.REQUEST.get('view_name')), portal_url())


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
    #item = hasattr(item, 'aq_explicit') and item.aq_explicit or item
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


def review_state(item, value):
    portal_url = getToolByName(getSite(), 'portal_url')
    state_icon = TASK_REVIEW_STATE_ICON.get(item.review_state,
                                      TASK_REVIEW_STATE_DEFAULT_ICON)
    return """
    <img src="%s/++resource++izug.theme.images/%s" width="16" height="16"/>
    """ % (portal_url(), state_icon)
