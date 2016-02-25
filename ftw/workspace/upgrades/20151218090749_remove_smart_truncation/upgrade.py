from ftw.upgrade import UpgradeStep


class RemoveSmartTruncation(UpgradeStep):
    """Remove smart truncation.
    """

    def __call__(self):
        self.install_upgrade_profile()
