from Acquisition import aq_inner, aq_parent
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.config import DEFAULT_TINYMCE_ALLOWED_BUTTONS
from plone.registry.interfaces import IRegistry
from zope.component import getUtility



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


def get_tinymce_buttons():
    """Get tinymce buttons from registry"""
    registry = getUtility(IRegistry)
    if 'ftw.workspace.allow_buttons' in registry:
        allow_buttons = registry['ftw.workspace.allow_buttons']
        if allow_buttons:
            return allow_buttons
    # Fallback
    return DEFAULT_TINYMCE_ALLOWED_BUTTONS