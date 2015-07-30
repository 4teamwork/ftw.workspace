from ftw.upgrade import UpgradeStep


class RemoveUnusedResources(UpgradeStep):
    """Remove unused resources.
    """

    def __call__(self):
        self.install_upgrade_profile()
