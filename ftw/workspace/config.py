"""Common configuration constants
"""

PROJECTNAME = 'ftw.workspace'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Workspace': 'ftw.workspace: Add Workspace',
}

INDEXES = (("sortable_creator", "FieldIndex"),
           ("getContentType", "FieldIndex"),
           ("ownerid", "FieldIndex"),
          )
          
METADATA = ("getMeeting_type",)