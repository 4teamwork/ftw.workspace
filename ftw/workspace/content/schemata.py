from Products.CMFCore.permissions import ManagePortal
from Products.ATContentTypes.content.schemata import finalizeATCTSchema


def finalizeWorkspaceSchema(schema, folderish=False,
                            moveDiscussion=True, portletLinkTitle=False):
    """Finalizes an ATCT type schema to alter some fields
    """

    finalizeATCTSchema(schema, folderish, moveDiscussion)

    schema.moveField('relatedItems', pos='bottom')
    if folderish:
        schema['relatedItems'].widget.visible['edit'] = 'invisible'
    schema.moveField('excludeFromNav', after='allowDiscussion')
    if moveDiscussion:
        schema.moveField('allowDiscussion', after='relatedItems')

    # Categorization
    if 'subject' in schema:
        schema.changeSchemataForField('subject', 'settings')
    if 'relatedItems' in schema:
        schema.changeSchemataForField('relatedItems', 'settings')
    if 'location' in schema:
        schema.changeSchemataForField('location', 'settings')
        schema['location'].widget.visible = -1
    if 'language' in schema:
        schema.changeSchemataForField('language', 'settings')
        schema['language'].widget.visible = -1

    # Dates
    if 'effectiveDate' in schema:
        schema.changeSchemataForField('effectiveDate', 'default')
        schema['effectiveDate'].widget.visible = -1
    if 'expirationDate' in schema:
        schema.changeSchemataForField('expirationDate', 'default')
        schema['expirationDate'].write_permission = ManagePortal
    if 'creation_date' in schema:
        schema.changeSchemataForField('creation_date', 'settings')
    if 'modification_date' in schema:
        schema.changeSchemataForField('modification_date', 'settings')

    # Ownership
    if 'creators' in schema:
        schema.changeSchemataForField('creators', 'settings')
        schema['creators'].write_permission = ManagePortal
    if 'contributors' in schema:
        schema.changeSchemataForField('contributors', 'settings')
        schema['contributors'].widget.visible = -1
    if 'rights' in schema:
        schema.changeSchemataForField('rights', 'settings')
        schema['rights'].widget.visible = -1

    # Settings
    if 'allowDiscussion' in schema:
        schema.changeSchemataForField('allowDiscussion', 'settings')
    if 'excludeFromNav' in schema:
        schema.changeSchemataForField('excludeFromNav', 'settings')
    if 'nextPreviousEnabled' in schema:
        schema.changeSchemataForField('nextPreviousEnabled', 'settings')
        schema['nextPreviousEnabled'].widget.visible = -1

    settings_fields = [schema[key] for key in schema.keys()
                            if schema[key].schemata == 'settings']
    for field in settings_fields:
        field.write_permission = ManagePortal

    return schema
