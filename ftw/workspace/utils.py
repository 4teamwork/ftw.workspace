from Products.CMFCore.utils import getToolByName

from interfaces import IWorkspaceUtils
from zope.interface import implements

class WorkspaceUtils(object):
    """ a collection of a few imprtant utils for workspace"""
    implements(IWorkspaceUtils)

    
    def __init__(self):
        """
        """
        
    
    def getAssignableUsers(self,context,role='Contributor'):
        """Collect users with a given role and return them in a list.
        """
        role = role
        results = []
        pas_tool = getToolByName(context, 'acl_users')
        utils_tool = getToolByName(context, 'plone_utils')
        
        inherited_and_local_roles = utils_tool.getInheritedLocalRoles(context) + pas_tool.getLocalRolesForDisplay(context)

        for user_id_and_roles in inherited_and_local_roles:
            if user_id_and_roles[2] == 'user':
                if role in user_id_and_roles[1]:
                    user = pas_tool.getUserById(user_id_and_roles[0])
                    if user:
                        results.append((user.getId(), '%s (%s)' % (user.getProperty('fullname', ''), user.getId())))
            if user_id_and_roles[2] == 'group':
                if role in user_id_and_roles[1]:
                    for user in pas_tool.getGroupById(user_id_and_roles[0]).getGroupMembers():
                        results.append((user.getId(), '%s (%s)' % (user.getProperty('fullname', ''), user.getId())))
                
        return results

