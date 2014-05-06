from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from ftw.workspace import _
from ftw.workspace.utils import TinyMCEAllowedButtonsConfigurator
from plone.registry.interfaces import IRegistry
from Products.Archetypes.public import TextField, RichWidget
from Products.ATContentTypes.content.folder import ATFolder
from zope.component import adapts
from zope.component import queryUtility
from zope.interface import implements


class folderTextField(ExtensionField, TextField):
    """ Extension TextField
    """


class FolderExtender(object):
    adapts(ATFolder)
    implements(IOrderableSchemaExtender)

    fields = [folderTextField(
        'text',
        searchable=True,
        required=False,
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_output_type='text/x-html-safe',
        default_input_type='text/html',
        widget=RichWidget(
            label=_(u"label_text", default=u"Text"),
            rows=15,
            allow_file_upload=False,
            allow_buttons=TinyMCEAllowedButtonsConfigurator(), )), ]

    def __init__(self, context):
        self.context = context

    def getFields(self):

        # self.context must AQ wrapped
        if not getattr(self.context, 'aq_parent', None):
            return []

        registry = queryUtility(IRegistry)
        if not registry:
            return []
        show = False
        if 'ftw.workspace.showtextfieldonfolder' in registry:
            show = registry['ftw.workspace.showtextfieldonfolder']

        if show and self.context.portal_type == 'TabbedViewFolder':
            return self.fields
        return []

    def getOrder(self, original):
        return original
