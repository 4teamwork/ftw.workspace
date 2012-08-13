from ftw.upgrade import ProgressLogger
from ftw.upgrade import UpgradeStep
from ftw.workspace.content.folder import TabbedViewFolder
import logging

LOG = logging.getLogger('ftw.workspace.upgrades')


class UseClasseForFolder(UpgradeStep):

    def __call__(self):
        self.update_fti()
        self.migrate_existing_folders()

    def update_fti(self):
        LOG.info('TabbedViewFolder FTI: update factory')
        self.setup_install_profile(
            'profile-ftw.workspace.upgrades:1501')

    def migrate_existing_folders(self):
        catalog = self.getToolByName('portal_catalog')
        brains = catalog.unrestrictedSearchResults(
            portal_type='TabbedViewFolder')

        with ProgressLogger('Migrate TabbedViewFolder classes',
                            brains) as step:
            for brain in brains:
                obj = self.portal.unrestrictedTraverse(brain.getPath())
                self.migrate_class(obj, TabbedViewFolder)
                step()
