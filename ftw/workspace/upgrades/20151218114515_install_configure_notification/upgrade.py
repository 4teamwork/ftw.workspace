from ftw.upgrade import UpgradeStep


class InstallConfigureNotification(UpgradeStep):
    """Install configure notification.
    """

    def __call__(self):
        base_version = self.portal_setup.getLastVersionForProfile(
            'ftw.notification.base:default')
        if base_version is None or base_version == 'unknown':
            self.setup_install_profile('profile-ftw.notification.base:default')

        email_version = self.portal_setup.getLastVersionForProfile(
            'ftw.notification.base:email')
        if email_version is None or email_version == 'unknown':
            self.setup_install_profile('profile-ftw.notification.email:default')

        self.install_upgrade_profile()
