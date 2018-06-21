from ftw.builder import Builder
from ftw.builder import create
from ftw.workspace.testing import FTW_WORKSPACE_FUNCTIONAL_TESTING
from ftw.zipextract.tests import FunctionalTestCase
import os
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from ftw.zipextract import zipextracter
from operator import itemgetter

class ZipExtracterTest(FunctionalTestCase):

    layer = FTW_WORKSPACE_FUNCTIONAL_TESTING

    def zip_extract_base_test(self, folder):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        self.workspace = create(Builder('workspace'))
        if folder:
            self.folder = create(Builder('TabbedViewFolder').within(self.workspace))
        else:
            self.folder = self.workspace
        file_content = open("{0}/data/test.zip".format(
            os.path.split(__file__)[0], 'r')).read()
        file_ = create(Builder('file')
                       .titled("zipfile")
                       .within(self.folder)
                       .attach_file_containing(file_content, u'file.zip'))
        extracter = zipextracter.ZipExtracter(file_)

        nfiles = len(self.portal.portal_catalog(portal_type="File"))
        nfolders = len(self.portal.portal_catalog(portal_type="TabbedViewFolder"))
        nworkspaces = len(self.portal.portal_catalog(portal_type="Workspace"))
        extracter.extract()
        files = self.portal.portal_catalog(portal_type="File")
        folders = self.portal.portal_catalog(portal_type="TabbedViewFolder")
        workspaces = self.portal.portal_catalog(portal_type="Workspace")
        self.assertEqual(len(files), nfiles + 1)
        self.assertEqual(len(folders), nfolders + 1)
        self.assertEqual(len(workspaces), nworkspaces)


    def test_zip_extract_in_workspace(self):
        self.zip_extract_base_test(False)

    def test_zip_extract_in_tabbedviewfolder(self):
        self.zip_extract_base_test(True)


