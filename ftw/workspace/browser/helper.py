from plone.memoize import ram


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
    if hasattr(item, 'getURL'):
        url_method = item.getURL
    elif hasattr(item, 'absolute_url'):
        url_method = item.absolute_url
    return """
    <a href="%s/delete_confirmation?came_from=%s" class="arbeitsraum_delete_item">
    <img src="%s/++resource++izug.theme.images/icon_funktion_entfernen.gif" />
    </a>
    """ % (url_method(), "%s#%s-tab"%(item.REQUEST.get('HTTP_REFERER'),
                                      item.REQUEST.get('view_name')),
                                      item.portal_url())


def custom_sort(list_, index, dir_):
    reverse = 0
    if dir_ == 'reverse':
        reverse = 1
    return sorted(list_, cmp=lambda x, y: cmp(getattr(x, index), getattr(y, index)), reverse=reverse)


def icon(item, value):
    url_method = lambda: '#'
    #item = hasattr(item, 'aq_explicit') and item.aq_explicit or item
    if hasattr(item, 'getURL'):
        url_method = item.getURL
    elif hasattr(item, 'absolute_url'):
        url_method = item.absolute_url
    img = u'<img src="%s/%s"/>' % (item.portal_url(), item.getIcon)
    link = u'<a href="%s/at_download">%s</a>' % (url_method(), img)
    return link


@ram.cache(lambda m, i, author: author)
def readable_author(item, author):
    #TODO: terribly inefficient. Make some HelperCommons or something
    if not author:
        return '-'
    name = author
    user = item.acl_users.getUserById(author)
    url = None
    if user is not None:
        name = user.getProperty('fullname', author)
        if not len(name):
            name = author
    if user is None:
        url, name = find_contact_object(item, author)
    if url is None:
        url = "%s/author/%s" % (item.portal_url(), author)
    return '<a href="%s">%s</a>' % (url, name)


def find_contact_object(item, id):
    item = item.getObject()
    current = item.aq_inner.aq_explicit
    while current.aq_parent.Type() in ['Workspace']:
        current = current.aq_parent
    brains = item.portal_catalog(id=id,
                                 Type='Contact',
                                 path='/'.join(current.getPhysicalPath()))
    if len(brains):
        return brains[0].getURL(), brains[0].Title
    return None, id


def responsible(item, value):
    return ','.join([readable_author(item, r) for r in item.getObject().getResponsibility()])


def review_state(item, value):
    icon = TASK_REVIEW_STATE_ICON.get(item.review_state,
                                      TASK_REVIEW_STATE_DEFAULT_ICON)
    return """
    <img src="%s/++resource++izug.theme.images/%s" width="16" height="16"/>
    """ % (item.portal_url(), icon)
