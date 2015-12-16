from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase


class TestFtwMeetingIntegration(TestCase):

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.workspace = create(Builder('workspace').titled('Workspace'))

    def test_meeding_is_addable(self):
        meeting = create(Builder('meeting')
                         .within(self.workspace)
                         .titled('Test Meeting')
                         .having(start_date=DateTime('08/20/2010 08:00'),
                                 end_date=DateTime('08/20/2010 10:00')))

        self.assertEquals([meeting.getId()], self.workspace.objectIds())

    @browsing
    def test_meeting_is_listed_in_on_tab(self, browser):
        meeting = create(Builder('meeting')
                         .within(self.workspace)
                         .titled('Test Meeting')
                         .having(start_date=DateTime('08/20/2010 08:00'),
                                 end_date=DateTime('08/20/2010 10:00')))

        browser.login().visit(self.workspace, view='tabbedview_view-events')

        self.assertEquals(meeting.start().strftime('%d.%m.%Y'),
                          browser.css('table tbody td')[0].text,
                          'Expect start date in first column.')
        self.assertEquals(meeting.Title(),
                          browser.css('table tbody td')[1].text,
                          'Expect title in second column.')
