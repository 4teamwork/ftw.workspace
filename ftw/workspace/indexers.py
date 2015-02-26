from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.utils import get_creator_fullname
from plone.indexer.decorator import indexer
from Products.ATContentTypes.interfaces.interfaces import IATContentType


@indexer(IWorkspace)
def ownerid(object_, **kw):
    """indexes the userid of the object owner"""
    userid = object_.getOwner(0).getId()
    return userid and userid or ''


@indexer(IATContentType)
def sortable_creator(object_, **kw):
    return get_creator_fullname(object_)
