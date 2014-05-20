from Acquisition import aq_parent, aq_base, aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.factory import IFactoryTool
from ftw.workspace.utils import find_workspace
from zope.component.hooks import getSite
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


class PrincipalVocabulary(SimpleVocabulary):
    """Vocabulary of a list of users. The userids are
    passed to __init__.
    """

    def __init__(self, userids):
        self.userids = userids
        super(PrincipalVocabulary, self).__init__(tuple(self._get_terms()))

    def _get_terms(self):
        portal = getSite()
        acl_users = getToolByName(portal, 'acl_users')

        users_dict = {}
        for id_ in self.userids:
            user = acl_users.getUserById(id_)

            catalog = getToolByName(portal, 'portal_catalog')
            brains = catalog(dict(UID=id_))
            if user is not None:
                users_dict[id_] = user.getProperty('fullname', id_)

            elif len(brains):
                brain = brains[0]
                users_dict[brain.UID] = "%s (Kontakt)" % brain.Title

        for id_, fullname in sorted(
            users_dict.items(), key=lambda item: item[1]):

            yield self.createTerm(id_, str(id_), fullname)


class AssignableUsersVocabulary(object):
    """Vocabulary of all users which participates in this workspace.
    """

    implements(IVocabularyFactory)

    def __call__(self, context, membersonly=False):
        workspace = find_workspace(context)
        catalog = getToolByName(context, 'portal_catalog')
        gtool = getToolByName(context, 'portal_groups')
        # users = getUtility(
        #     IVocabularyFactory,
        #     name='plone.principalsource.Users',
        #     context=context)(context)

        if not workspace:
            workspace = context

        # Create a list of user depending on local roles and inherited
        # roles. Also read out users from groups
        users = set([])
        groups = set([])

        # Walk upwards until reach portal root or role acquire check fails
        portal = workspace.portal_url.getPortalObject()
        cont = True
        while cont:
            if context == portal:
                break

            if IFactoryTool.providedBy(context):
                # this is portal_factory - skip it
                context = aq_parent(aq_inner(context))
                continue

            if IFactoryTool.providedBy(aq_parent(context)):
                # this is the 'Ticket Box' temp folder
                # within portal_factory - skip it
                context = aq_parent(aq_inner(context))
                continue

            userroles = portal.acl_users._getLocalRolesForDisplay(context)
            # Use dict's to auto. prevent duplicated entries
            for user, roles, role_type, name in userroles:
                if role_type == u'user' and name not in users:
                    users.add(name)
                elif role_type == u'group' and user not in groups:
                    groups.add(name)

            if getattr(aq_base(context), '__ac_local_roles_block__', None):
                cont = False
            else:
                context = aq_parent(context)

        # Go throught groups an add their containing users to the user list
        for groupid in groups:
            group = gtool.getGroupById(groupid)
            if group:
                members = set(group.getGroupMemberIds())
            else:
                continue
            # Put together
            users = users.union(members)

        result = users

        if not membersonly:
            query = dict(
                portal_type='Contact',
                path='/'.join(workspace.getPhysicalPath()),
                sort_on='sortable_title')

            for brain in catalog(query):
                result.add(brain.UID)

        return PrincipalVocabulary(result)


AssignableUsersVocabularyFactory = AssignableUsersVocabulary()
