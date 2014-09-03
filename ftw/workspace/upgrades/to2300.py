from ftw.upgrade import UpgradeStep


class InstallActivity(UpgradeStep):

    def __call__(self):
        self.setup_install_profile('profile-ftw.activity:default')
