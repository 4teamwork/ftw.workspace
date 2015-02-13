from ftw.upgrade import UpgradeStep
from ftw.workspace.interfaces import IWorkspace
import logging

LOG = logging.getLogger('ftw.workspace.upgrades')


class IndexWorkspaceCreator(UpgradeStep):

    def __call__(self):
        query = {'object_provides': IWorkspace.__identifier__}
        self.catalog_reindex_objects(query, idxs=['SearchableText'])
