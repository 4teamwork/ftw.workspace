from ftw.lawgiver.tests.base import WorkflowTest
from path import Path
import ftw.workspace
import sys


class CompareWorkspaceWorkflowTest(WorkflowTest):
    """Inherit from this test in a policy-packages if you want to use
    the ftw.workspace workflow:

    class TestPolicyWorkflowWorkspaceContent(CompareWorkspaceWorkflowTest):
        layer = EXAMPLE_FUNCTIONAL
        workflow_path = '../profiles/default/workflows/workspace_content_workflow'


    In addition to the default workflow-test it also compares the
    ftw.workspace workflow with the policy-workflow. The tests will pass
    unless the policyworkflow is out of sync with the ftw.workspace workflow.

    By that, you're able to detect if someone changed the ftw.workspace
    workflow and you can easely update your policy workflow.
    """
    specification_name = 'specification.de.txt'

    def test_compare_workspace_workflow(self):
        if self._is_base_test():
            return

        spec_source_path = Path(ftw.workspace.__file__).joinpath(
            '..', 'profiles', 'default',
            'workflows', Path(self.workflow_path).basename(),
            self.specification_name).abspath()

        self.assertTrue(
            spec_source_path.isfile(),
            "The source file at '{}' does no longer exists.".format(
                spec_source_path))

        class_file_path = sys.modules[self.__class__.__module__].__file__
        spec_target_path = Path(class_file_path).joinpath(
            '..', self.workflow_path, self.specification_name).abspath()

        self.maxDiff = None
        self.assertMultiLineEqual(
            spec_source_path.bytes(),
            spec_target_path.bytes() if spec_target_path.isfile() else ''
            """
            Your policy specification.txt is not anymore synced with the
            specifiaction in ftw.workspace.

            ftw.workspace provides a recommended workflow which should be used
            in your package. Perhaps this workflow have been updated and you
            didn't updated your policy with that new workflow.

            If this is the case, just type in the following command to fix the test:

            cp {} {}

            Otherwise if you want to provide an own workflow in your policy which
            is different than the recommended workflow in ftw.workspace,
            you have to adjust the failing testcase. Just inherit from the
            `WorfklowTest` class directly and your wokflow will be tested as usual:

            Rename:

            {}(CompareWorkspaceWorkflowTest)

            to

            {}(WorkflowTest)
            """.format(
                spec_source_path,
                spec_target_path,
                self.__class__.__name__,
                self.__class__.__name__))

    def _is_base_test(self):
        return super(CompareWorkspaceWorkflowTest, self)._is_base_test() \
            or type(self) == CompareWorkspaceWorkflowTest
