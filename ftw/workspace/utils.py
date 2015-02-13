from Acquisition import aq_inner, aq_parent
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.config import DEFAULT_TINYMCE_ALLOWED_BUTTONS
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName


def has_ftwfile(context):
    portal_setup = getToolByName(context, 'portal_setup')
    profile_version = portal_setup.getLastVersionForProfile('ftw.file:default')
    return profile_version != 'unknown'


def find_workspace(context):
    """Walks up and returns the next parent workspace (IWorkspace) or
    returns None if plone site is reached.
    """

    obj = context
    while True:
        if IWorkspace.providedBy(obj):
            return obj

        elif IPloneSiteRoot.providedBy(obj):
            return None

        parent = aq_parent(aq_inner(obj))
        if parent == obj:
            raise ValueError('Somethings wrong: cannot walk up further')
        else:
            obj = parent


class TinyMCEAllowedButtonsConfigurator(object):
    """
    The TinyMCE RichWidget expects the button configuration attributes
    to be a iterable object.

    The configuration is stored in the registry, so we need to do a
    little workaround.
    """

    def __init__(self):
        self._data = None

    def __iter__(self):
        """This is a iterator, so it returns itself.
        """
        return self

    def next(self):
        """Iterate over the result of `load_data`. When the end is reached,
        raise StopIteration as defined for iterable objects. But when
        starting iteration again, retrieve the configuration and start again
        at the beginning.
        """

        if self._data is None:
            self._data = list(self.load_data())

        if len(self._data) > 0:
            return self._data.pop(0)

        else:
            self._data = None
            raise StopIteration()

    def load_data(self):
        registry = getUtility(IRegistry)
        if 'ftw.workspace.allow_buttons' in registry:
            allow_buttons = registry['ftw.workspace.allow_buttons']
            if allow_buttons:
                return allow_buttons

        # Fallback
        return DEFAULT_TINYMCE_ALLOWED_BUTTONS


def get_creator_fullname(obj):
    creator = obj.Creator()
    pas_tool = getToolByName(obj, 'acl_users')
    user = pas_tool.getUserById(creator)
    if not user:
        return creator
    fullname = user.getProperty('fullname', creator)
    if fullname:
        return fullname
    return creator
