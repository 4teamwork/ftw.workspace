from Products.CMFCore.utils import getToolByName
from ftw.workspace.utils import find_workspace
from zope.app.component.hooks import getSite
from zope.component import getUtility
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

        for id in self.userids:
            user = acl_users.getUserById(id)
            catalog = getToolByName(portal, 'portal_catalog')
            brains = catalog(dict(UID=id))
            if user is not None:
                fullname = user.getProperty('fullname', id)
                yield self.createTerm(id, str(id), fullname)
            elif len(brains):
                brain = brains[0]
                yield self.createTerm(
                    brain.UID,
                    brain.UID,
                    "%s (Kontakt)" % brain.Title)


class AssignableUsersVocabulary(object):
    """Vocabulary of all users which participates in this workspace.
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        workspace = find_workspace(context)
        catalog = getToolByName(context, 'portal_catalog')
        if not workspace:
            return getUtility(IVocabularyFactory,
                              name='plone.principalsource.Users',
                              context=context)(context)
        query = dict(
            portal_type='Contact',
            path='/'.join(workspace.getPhysicalPath()),
            sort_on = 'sortable_title')
        result = dict(workspace.get_local_roles()).keys()
        for brain in catalog(query):
            result.append(brain.UID)
        return PrincipalVocabulary(result)


AssignableUsersVocabularyFactory = AssignableUsersVocabulary()
