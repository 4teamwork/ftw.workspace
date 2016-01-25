from ftw.lawgiver.tests.base import WorkflowTest
from ftw.workspace.testing import FTW_WORKSPACE_INTEGRATION_TESTING


class TestWorkflowSpecificationWorkspaceContent(WorkflowTest):

    workflow_path = '../profiles/default/workflows/workspace_content_workflow'
    layer = FTW_WORKSPACE_INTEGRATION_TESTING


class TestWorkflowSpecificationWorkspace(WorkflowTest):

    workflow_path = '../profiles/default/workflows/workspace_workflow'
    layer = FTW_WORKSPACE_INTEGRATION_TESTING


class TestWorkflowSpecificationWorkspaces(WorkflowTest):

    workflow_path = '../profiles/default/workflows/workspaces_workflow'
    layer = FTW_WORKSPACE_INTEGRATION_TESTING
