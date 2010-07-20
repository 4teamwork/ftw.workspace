from plone.indexer.decorator import indexer
from interfaces import IWorkspace

@indexer(IWorkspace)
def ownerid(object, **kw):
    """indexes the userid of the object owner"""
    userid = object.getOwner(0).getId()
    return userid and userid or ''