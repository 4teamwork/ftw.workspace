from ftw.upgrade import UpgradeStep
import logging

LOG = logging.getLogger('ftw.workspace.upgrades')


class InstallSmartTruncation(UpgradeStep):

    def __call__(self):
        self.install_package()

    def install_package(self):
        LOG.info('Install collective.js.jqsmarttruncation')
        self.setup_install_profile(
            'profile-collective.js.jqsmartTruncation:default')
