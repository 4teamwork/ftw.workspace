"""Definition of the Workspace content type
"""

from AccessControl import ClassSecurityInfo

from zope.interface import implements
from zope.component import adapter

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.configuration import zconf
from Products.Archetypes.interfaces import IObjectInitializedEvent

from Products.CMFCore.permissions import View

from Products.validation.config import validation
from Products.validation.validators.SupplValidators import MaxSizeValidator

from ftw.calendarwidget.browser.widgets import FtwCalendarWidget
from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.config import PROJECTNAME
from ftw.workspace.content.utilities import finalizeWorkspaceSchema

validation.register(MaxSizeValidator('checkImageMaxSize',
                                     maxsize=zconf.ATImage.max_file_size))

WorkspaceSchema = folder.ATFolderSchema.copy()

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.
WorkspaceSchema['title'].storage = atapi.AnnotationStorage()
WorkspaceSchema['description'].storage = atapi.AnnotationStorage()
WorkspaceSchema['description'].required = True
schemata.finalizeATCTSchema(WorkspaceSchema, folderish=True, moveDiscussion=False)
finalizeWorkspaceSchema(WorkspaceSchema, folderish=True, moveDiscussion=False)

WorkspaceSchema.changeSchemataForField('effectiveDate','settings')
WorkspaceSchema.changeSchemataForField('expirationDate','settings')
WorkspaceSchema.get('effectiveDate').widget = FtwCalendarWidget(
    label="Start of Meeting",
    description="task_help_start_date",
    )
WorkspaceSchema['effectiveDate'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}
WorkspaceSchema['expirationDate'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}

@adapter(IWorkspace, IObjectInitializedEvent)
def workspace_added(object_, event):
    current_user = object_.portal_membership.getAuthenticatedMember().getId()
    # Fix (PHa): Only set local roles for logged-in user, if his/her id already has local roles 
    if object_.__ac_local_roles__.has_key(current_user):
        object_.__ac_local_roles__[current_user] += ['Contributor', 'Administrator', 'Editor', 'Reader']

class Workspace(folder.ATFolder):
    """A type for collaborative spaces."""
    implements(IWorkspace)

    portal_type = "Workspace"
    schema = WorkspaceSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    image = atapi.ATFieldProperty('image')
    start_date = atapi.ATFieldProperty('start_date')
    end_date = atapi.ATFieldProperty('end_date')

    security = ClassSecurityInfo()

    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return folder.ATFolder.__bobo_traverse__(self, REQUEST, name)

    @property
    def sortAttribute(self):
        return 'getObjPositionInParent'
        
    @property
    def sortOrder(self):
        return 'ascending'

atapi.registerType(Workspace, PROJECTNAME)
