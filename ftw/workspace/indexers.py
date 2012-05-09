from plone.indexer.decorator import indexer
from Products.CMFCore.utils import getToolByName
from ftw.workspace.interfaces import IWorkspace
from Products.ATContentTypes.interfaces.interfaces import IATContentType


@indexer(IWorkspace)
def ownerid(object_, **kw):
    """indexes the userid of the object owner"""
    userid = object_.getOwner(0).getId()
    return userid and userid or ''


@indexer(IATContentType)
def sortable_creator(object_, **kw):
    creator = object_.Creator()
    pas_tool = getToolByName(object_, 'acl_users')
    user = pas_tool.getUserById(creator)
    if not user:
        return creator
    fullname = user.getProperty('fullname', creator)
    if fullname:
        return fullname
    return creator
