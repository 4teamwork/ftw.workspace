from ftw.dictstorage.interfaces import IDictStorage
from ftw.upgrade import UpgradeStep
from ftw.upgrade.progresslogger import ProgressLogger


PREFIXES = [
    'ftw.tabbedview-Workspace-tabbedview_view-documents-',
    'ftw.tabbedview-TabbedViewFolder-tabbedview_view-documents-',
    'ftw.tabbedview-Folder-tabbedview_view-documents-',
    ]


class ResetExtJSConfig(UpgradeStep):

    def __call__(self):
        workspace = self.get_any_workspace()
        if not workspace:
            return
        view = workspace.unrestrictedTraverse('tabbedview_view-documents')
        storage = IDictStorage(view)
        keys = storage.storage.storage.keys()[:]

        for key in ProgressLogger('Reset documents tab state', keys):
            for PREFIX in PREFIXES:
                if key.startswith(PREFIX):
                    del storage[key]

    def get_any_workspace(self):
        query = {'portal_type': 'Workspace'}
        brains = self.catalog_unrestricted_search(query)
        if not brains:
            return None
        return self.catalog_unrestricted_get_object(brains[0])
