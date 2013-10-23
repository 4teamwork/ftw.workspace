from ftw.upgrade import UpgradeStep


class InstallColorbox(UpgradeStep):

    def __call__(self):
        self.setup_install_profile('profile-ftw.colorbox:default')
