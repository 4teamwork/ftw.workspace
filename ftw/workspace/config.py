"""Common configuration constants
"""

PROJECTNAME = 'ftw.workspace'

ADD_PERMISSIONS = {
    'Workspace': 'ftw.workspace: Add Workspace',
    'TabbedViewFolder': 'ATContentTypes: Add Folder',
}

INDEXES = (("sortable_creator", "FieldIndex"),
           ("getContentType", "FieldIndex"),
           ("ownerid", "FieldIndex"), )

METADATA = ("getMeeting_type", )
DEFAULT_TINYMCE_ALLOWED_BUTTONS = (
    'bg-basicmarkup',
    'bold-button',
    'italic-button',
    'list-ol-addbutton',
    'list-ul-addbutton',
    'definitionlist',
    'linklibdrawer-button',
    'removelink-button', )
