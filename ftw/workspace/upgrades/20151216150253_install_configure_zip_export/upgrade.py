from ftw.upgrade import UpgradeStep


class InstallConfigureZipExport(UpgradeStep):
    """Install configure zip export.
    """

    def __call__(self):
        version = self.portal_setup.getLastVersionForProfile(
            'ftw.zipexport:default')

        if version is None or version == 'unknown':
            self.setup_install_profile('profile-ftw.zipexport:default')

        self.install_upgrade_profile(steps=['plone.app.registry'])
