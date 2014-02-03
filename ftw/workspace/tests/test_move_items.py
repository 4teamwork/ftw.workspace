from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase


class TestMoveItems(TestCase):

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Reviewer', 'Manager'])

    @browsing
    def test_move_items_moves_items(self, browser):

        # setup folder / items
        source = create(Builder('folder')
                         .titled('Source Folder'))

        target = create(Builder('folder')
                         .titled('Target Folder'))

        create(Builder('file')
               .titled('The File')
               .within(source)
               .attach_file_containing('content', name='file.txt'))

        # open source containing file
        browser.login(SITE_OWNER_NAME).open()
        browser.visit(source, view='folder_contents')

        # select file and hit move button
        browser.css('#cb_the-file').first.node.checked = True
        browser.find('Move Items').click()

        browser.fill({'Destination': target})
        browser.find('Move').click()

        self.assertTrue(
            target.get('the-file'),
            '"The File" should be located in the target folder.')
