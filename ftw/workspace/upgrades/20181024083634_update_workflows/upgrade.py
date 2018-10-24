from ftw.upgrade import UpgradeStep


class UpdateWorkflows(UpgradeStep):
    """Update workflows.
    """

    def __call__(self):
        self.install_upgrade_profile()
        self.update_workflow_security(
            ['workspace_workflow',
             'workspace_content_workflow',
             'workspaces_workflow'],
            reindex_security=False)
