from Acquisition import aq_inner, aq_parent
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ftw.workspace.interfaces import IWorkspace


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
