"""Common configuration constants
"""

PROJECTNAME = 'ftw.workspace'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Workspace': 'ftw.workspace: Add Workspace',
}

INDEXES = (("getMeeting_type", "KeywordIndex"),
           ("sortable_creator", "KeywordIndex"),
           ("sortable_responsibility", "KeywordIndex"),
           ("getContentType", "KeywordIndex"),
           # ("get_owner_index", "KeywordIndex"),
          )
          
METADATA = ("getMeeting_type",)