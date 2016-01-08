from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.testing import FTW_WORKSPACE_INTEGRATION_TESTING
from operator import methodcaller
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.interfaces.factory import IFactoryTool
from unittest2 import TestCase
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.schema.interfaces import IVocabularyFactory


class TestFtwNotificationIntegration(TestCase):

    layer = FTW_WORKSPACE_INTEGRATION_TESTING

    def setUp(self):

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace').titled('Workspace'))
        self.subfolder = create(Builder('TabbedViewFolder')
                                .within(self.workspace)
                                .titled('Folder1'))
        self.subsubfolder = create(Builder('TabbedViewFolder')
                                   .within(self.subfolder)
                                   .titled('Folder1'))

        self.file_ = create(Builder('file')
                            .titled('A File')
                            .within(self.subsubfolder)
                            .with_dummy_content())

        self.vocab_factory = getUtility(IVocabularyFactory,
                                        name='assignable_users')

        self.owner = [TEST_USER_ID, ]

    def test_list_users_with_local_roles_on_obj(self):
        user1 = create(Builder('user')
                       .named('Test', 'User1')
                       .with_roles('Reader', on=self.workspace))

        self.assertItemsEqual(
            [user1.getId()] + self.owner,
            self.vocab_factory(self.workspace).userids)

    def test_list_users_with_local_roles_on_parents(self):
        user1 = create(Builder('user')
                       .named('Test', 'User1')
                       .with_roles('Reader', on=self.workspace))
        user2 = create(Builder('user')
                       .named('Test', 'User2')
                       .with_roles('Reader', on=self.subfolder))
        user3 = create(Builder('user')
                       .named('Test', 'User3')
                       .with_roles('Reader', on=self.subsubfolder))

        users = map(methodcaller('getId'), [user1, user2, user3])

        self.assertItemsEqual(
            users + self.owner,
            self.vocab_factory(self.file_).userids)

    def test_dont_list_users_with_local_roles_of_childrens(self):
        create(Builder('user')
               .named('Test', 'User1')
               .with_roles('Reader', on=self.workspace))
        user2 = create(Builder('user')
                       .named('Test', 'User2')
                       .with_roles('Reader', on=self.subsubfolder))

        self.assertNotIn(
            user2.getId(),
            self.vocab_factory(self.subfolder).userids)

    def test_do_no_list_users_with_global_roles(self):
        user = create(Builder('user')
                      .named('Test', 'User1')
                      .with_roles('Reader'))

        self.assertNotIn(
            user.getId(),
            self.vocab_factory(self.workspace).userids)

    def test_list_member_of_group_with_local_roles(self):
        user = create(Builder('user')
                      .named('Test', 'User1'))

        create(Builder('group')
               .titled('Group')
               .with_roles('Reader', on=self.workspace)
               .with_members(user))

        self.assertItemsEqual(
            [user.getId()] + self.owner,
            self.vocab_factory(self.subfolder).userids)

    def test_dont_list_users_with_local_roles_if_acquistion_stopped(self):
        create(Builder('user')
               .named('Test', 'User1')
               .with_roles('Reader', on=self.workspace))

        self.subfolder.__ac_local_roles_block__ = True

        self.assertItemsEqual(
            self.owner,
            self.vocab_factory(self.subfolder).userids)

    def test_dont_list_member_of_group_if_acquistion_stopped(self):
        user = create(Builder('user')
                      .named('Test', 'User1'))

        create(Builder('group')
               .titled('Group')
               .with_roles('Reader', on=self.workspace)
               .with_members(user))

        self.subfolder.__ac_local_roles_block__ = True

        self.assertItemsEqual(
            self.owner,
            self.vocab_factory(self.subfolder).userids)

    def test_vocab_is_sorted_by_fullname(self):
        user1 = create(Builder('user')
                       .named('ZZZ', 'User')
                       .with_roles('Reader', on=self.workspace))
        user2 = create(Builder('user')
                       .named('aaa', 'User')
                       .with_roles('Reader', on=self.subfolder))
        user3 = create(Builder('user')
                       .named('ABC', 'User')
                       .with_roles('Reader', on=self.subsubfolder))

        users = map(lambda user: user.getProperty('fullname'),
                    [user2, user3, user1])
        users.insert(0, '')  # The test user has no fullname

        users_from_vocabulary = [user.title for user in self.vocab_factory(
            self.subsubfolder)]

        self.assertItemsEqual(users, users_from_vocabulary)

    def test_vocabulary_can_lists_contacts_too(self):
        user1 = create(Builder('user')
                       .named('ZZZ', 'User')
                       .with_roles('Reader', on=self.workspace))

        contact = create(Builder('contact')
                         .within(self.workspace)
                         .having(firstname='Contact', lastname='User'))

        self.assertItemsEqual(
            [user1.getId()] + self.owner + [IUUID(contact)],
            self.vocab_factory(self.subfolder, membersonly=False).userids)

        self.assertItemsEqual(
            [user1.getId()] + self.owner,
            self.vocab_factory(self.subfolder, membersonly=True).userids)

    def test_vocabulary_ignore_local_roles_of_factory_tool(self):
        user1 = create(Builder('user')
                       .named('Test', 'User1')
                       .with_roles('Reader', on=self.workspace))
        create(Builder('user')
               .named('Test', 'User2')
               .with_roles('Reader', on=self.subfolder))
        create(Builder('user')
               .named('Test', 'User3')
               .with_roles('Reader', on=self.subsubfolder))

        alsoProvides(self.subfolder, IFactoryTool)

        self.assertItemsEqual(
            [user1.getId()] + self.owner,
            self.vocab_factory(self.file_).userids)
