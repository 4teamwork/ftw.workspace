from ftw.upgrade import UpgradeStep


class InstallNewFeatures(UpgradeStep):
    """
    Enable filtering on overview.
    Truncate long text in recently modified listing.
    Use 'today + time' and 'yesterday + time' in recently modified listing.
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-collective.js.jqsmartTruncation:default')

        self.setup_install_profile(
            'profile-ftw.workspace.upgrades:1700')
