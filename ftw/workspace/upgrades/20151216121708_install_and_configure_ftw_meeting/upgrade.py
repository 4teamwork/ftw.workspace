from ftw.upgrade import UpgradeStep


class InstallAndConfigureFtwMeeting(UpgradeStep):
    """Install and configure ftw meeting.
    """

    def __call__(self):
        version = self.portal_setup.getLastVersionForProfile(
            'ftw.meeting:default')

        if version is None or version == 'unknown':
            self.setup_install_profile('profile-ftw.meeting:default')

        self.install_upgrade_profile(steps=['typeinfo'])
