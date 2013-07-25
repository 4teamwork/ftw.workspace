from ftw.upgrade import UpgradeStep


class ImportRegistry(UpgradeStep):

    def __call__(self):
        self.setup_install_profile('profile-ftw.workspace.upgrades:1701')
