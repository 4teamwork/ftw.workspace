from ftw.pdfgenerator.interfaces import IBuilder
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.pdfgenerator.tests import test_customizable_layout
from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.latex.layout import WorkspaceLayout
from ftw.workspace.testing import LATEX_ZCML_LAYER
from zope.component import getMultiAdapter


class TestWorkspaceLayout(test_customizable_layout.TestCustomizableLayout):

    layout_class = WorkspaceLayout
    layer = LATEX_ZCML_LAYER

    def setUp(self):
        super(test_customizable_layout.TestCustomizableLayout, self).setUp()
        self.context = self.providing_stub(IWorkspace)
        self.builder = self.stub_interface(IBuilder)
        super(TestWorkspaceLayout, self).setUp(context=self.context,
                                               builder=self.builder)

        self.portal_languages = self.stub()
        self.mock_tool(self.portal_languages, 'portal_languages')
        self.expect(self.portal_languages.getPreferredLanguage()).result(
            'en')

    def test_get_render_arguments(self):
        self.replay()

        layout = getMultiAdapter((self.context, self.request, self.builder),
                            ILaTeXLayout)
        args = layout.get_render_arguments()

        self.assertIn('pageLabel', args)
        self.assertIn('printedLabel', args)
        self.assertIn('printedLabel', args)

    def test_layout_renders(self):
        self.replay()
        layout = getMultiAdapter((self.context, self.request, self.builder),
                                 ILaTeXLayout)
        latex = layout.render_latex('CONTENT LATEX')

        self.assertIn('\documentclass[a4paper,10pt]{article}', latex)
        self.assertIn('[english]{babel}', latex)
        self.assertIn('{fancyhdr}', latex)
        self.assertIn('{lastpage}', latex)
        self.assertIn('{hyperref}', latex)
        self.assertIn('CONTENT LATEX', latex)
