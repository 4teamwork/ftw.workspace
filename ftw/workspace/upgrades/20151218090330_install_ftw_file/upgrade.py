from ftw.upgrade import UpgradeStep


class InstallFtwFile(UpgradeStep):
    """Install ftw file.
    """

    def __call__(self):
        version = self.portal_setup.getLastVersionForProfile(
            'ftw.file:default')
        if version is None or version == 'unknown':
            self.setup_install_profile('profile-ftw.file:default')
