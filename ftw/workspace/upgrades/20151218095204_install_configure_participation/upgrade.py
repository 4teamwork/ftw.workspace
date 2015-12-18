from ftw.upgrade import UpgradeStep
from Products.CMFCore.permissions import View


class InstallConfigureParticipation(UpgradeStep):
    """Install configure participation.
    """

    def __call__(self):
        version = self.portal_setup.getLastVersionForProfile(
            'ftw.participation:default')

        if version is None or version == 'unknown':
            self.setup_install_profile('profile-ftw.participation:default')

        self.install_upgrade_profile(steps=['plone.app.registry'])

        self.add_pariticipants_tab()

    def add_pariticipants_tab(self):
        self.actions_add_type_action(
            portal_type='Workspace',
            after=None,
            action_id='participants',
            **{'category': 'tabbedview-tabs',
               'action': 'string:${object_url}?view=participants',
               'visible': True,
               'permissions': (View, )})
