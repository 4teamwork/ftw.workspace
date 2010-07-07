from Products.CMFCore.permissions import ManagePortal
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

def finalizeWorkspaceSchema(schema, folderish=False, moveDiscussion=True, portletLinkTitle=False):
    """Finalizes an ATCT type schema to alter some fields
    """
    
    finalizeATCTSchema(schema,folderish,moveDiscussion)
    
    schema.moveField('relatedItems', pos='bottom')
    if folderish:
        schema['relatedItems'].widget.visible['edit'] = 'invisible'
    schema.moveField('excludeFromNav', after='allowDiscussion')
    if moveDiscussion:
        schema.moveField('allowDiscussion', after='relatedItems')

    # Categorization
    if schema.has_key('subject'):
        schema.changeSchemataForField('subject', 'settings')
    if schema.has_key('relatedItems'):
        schema.changeSchemataForField('relatedItems', 'settings')
    if schema.has_key('location'):
        schema.changeSchemataForField('location', 'settings')
        schema['location'].widget.visible = -1
    if schema.has_key('language'):
        schema.changeSchemataForField('language', 'settings')
        schema['language'].widget.visible = -1

    # Dates
    if schema.has_key('effectiveDate'):
        schema.changeSchemataForField('effectiveDate', 'default')
    if schema.has_key('expirationDate'):
        schema.changeSchemataForField('expirationDate', 'default')    
    if schema.has_key('creation_date'):
        schema.changeSchemataForField('creation_date', 'settings')    
    if schema.has_key('modification_date'):
        schema.changeSchemataForField('modification_date', 'settings')    

    # Ownership
    if schema.has_key('creators'):
        schema.changeSchemataForField('creators', 'settings')
        schema['creators'].widget.visible = -1
    if schema.has_key('contributors'):
        schema.changeSchemataForField('contributors', 'settings')
        schema['contributors'].widget.visible = -1
    if schema.has_key('rights'):
        schema.changeSchemataForField('rights', 'settings')
        schema['rights'].widget.visible = -1

    # Settings
    if schema.has_key('allowDiscussion'):
        schema.changeSchemataForField('allowDiscussion', 'settings')
    if schema.has_key('excludeFromNav'):
        schema.changeSchemataForField('excludeFromNav', 'settings')
    if schema.has_key('nextPreviousEnabled'):
        schema.changeSchemataForField('nextPreviousEnabled', 'settings')
        schema['nextPreviousEnabled'].widget.visible = -1

    #add Title for Link Portlet
    if portletLinkTitle:
        schema.addField(StringField('linkPortletTitle',
                                             schemata = 'settings',
                                             widget=StringWidget(
                                                i18n_domain='plonegov',
                                                label='Link Portlet-Titel',
                                                label_msgid='ZugNews_label_portlettitle',
                                                visible = {'edit': 1, 'view': 0},
                                                ),
                                             )
                                )
    #set permissions for settings schemata

    settings_fields = [schema[key] for key in schema.keys() if schema[key].schemata == 'settings']
    for field in settings_fields:
        field.write_permission = ManagePortal

    return schema
