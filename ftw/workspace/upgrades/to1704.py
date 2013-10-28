from ftw.upgrade import UpgradeStep


class InstallPreview(UpgradeStep):

    def __call__(self):
        self.setup_install_profile('profile-ftw.colorbox:default')

        self.setup_install_profile(
            'profile-ftw.workspace.upgrades:1704',
            steps=['propertiestool', 'cssregistry', 'jsregistry'])
