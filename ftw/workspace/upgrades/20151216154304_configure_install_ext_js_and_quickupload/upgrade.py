from ftw.upgrade import UpgradeStep


class ConfigureInstallExtJsAndQuickupload(UpgradeStep):
    """Configure install extjs and quickupload.
    """

    def __call__(self):
        extjs_version = self.portal_setup.getLastVersionForProfile(
            'ftw.tabbedview:extjs')
        if extjs_version is None or extjs_version == 'unknown':
            self.setup_install_profile('profile-ftw.tabbedview:extjs')

        quickuplad_version = self.portal_setup.getLastVersionForProfile(
            'ftw.tabbedview:quickupload')
        if quickuplad_version is None or quickuplad_version == 'unknown':
            self.setup_install_profile('profile-ftw.tabbedview:quickupload')
