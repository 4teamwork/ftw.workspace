from Acquisition import aq_inner, aq_parent
from ftw.workspace import _
from OFS.CopySupport import CopyError, ResourceLockedError
from plone.formwidget.contenttree import ContentTreeFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.z3cform import layout
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import form, field
from z3c.form import validator
from z3c.form.interfaces import HIDDEN_MODE
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.component import provideAdapter
from zope.interface import Interface, Invalid
from zope.publisher.browser import BrowserView
import z3c.form


class IMoveItemsSchema(Interface):
    destination_folder = RelationChoice(
        title=_('label_destination', default="Destination"),
        description=_('help_destination',
                      default="Select the destination container."),
        source=ObjPathSourceBinder(
            is_folderish=True,
            navigation_tree_query=None),
        required=True,
        )
    #We Use TextLine here because Tuple and List have no hidden_mode.
    request_paths = schema.TextLine(title=u"request_paths")


class MoveItemsForm(form.Form):

    fields = field.Fields(IMoveItemsSchema)
    fields['destination_folder'].widgetFactory = ContentTreeFieldWidget
    ignoreContext = True
    label = _('heading_move_items', default="Move Items")

    def updateWidgets(self):
        super(MoveItemsForm, self).updateWidgets()
        self.widgets['request_paths'].mode = HIDDEN_MODE
        value = self.request.get('paths')
        if value:
            self.widgets['request_paths'].value = ';;'.join(value)

    @z3c.form.button.buttonAndHandler(_(u'button_move',
                                        default=u'Move'))
    def handle_submit(self, action):
        data, errors = self.extractData()
        if len(errors):
            return

        source = data['request_paths'].split(';;')
        destination = data['destination_folder']
        failed_objects = []
        failed_resource_locked_objects = []
        moved_items = 0

        for path in source:

            portal = getToolByName(
                self.context, 'portal_url').getPortalObject()

            # Get source object
            src_object = portal.unrestrictedTraverse(
                path.encode('utf-8'))

            # Get parent object
            source_container = aq_parent(aq_inner(
                portal.unrestrictedTraverse(path.encode('utf-8'))))

            src_name = src_object.title
            src_id = src_object.id

            try:
                # Try to cut and paste object
                clipboard = source_container.manage_cutObjects(src_id)
                destination.manage_pasteObjects(clipboard)
                moved_items += 1

            except ResourceLockedError:
                # The object is locket over webdav
                failed_resource_locked_objects.append(src_name)
                continue

            except (ValueError, CopyError):
                # Catch exception and add title to a list of failed objects
                failed_objects.append(src_name)
                continue

        self.create_statusmessages(
            moved_items,
            failed_objects,
            failed_resource_locked_objects, )

        self.request.RESPONSE.redirect(destination.absolute_url())

    @z3c.form.button.buttonAndHandler(_(u'button_cancel',
                                        default=u'Cancel'))
    def handle_cancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())

    def create_statusmessages(
        self,
        moved_items,
        failed_objects,
        failed_resource_locked_objects
    ):
        """ Create statusmessages with errors and infos af the move-process
        """
        if moved_items:
            msg = _(u'${moved_items} Elements were moved successfully',
                    mapping=dict(moved_items=moved_items))
            IStatusMessage(self.request).addStatusMessage(
                msg, type='info')

        if failed_objects:
            msg = _(u'Failed to move following objects: ${failed_objects}',
                    mapping=dict(failed_objects=',<br>'.join(failed_objects)))
            IStatusMessage(self.request).addStatusMessage(
                msg, type='error')

        if failed_resource_locked_objects:
            msg = _(
                u'''Failed to move following objects: ''' +
                '''${failed_objects}. Locked via WebDAV''',
                mapping=dict(failed_objects=',<br>'.join(
                    failed_resource_locked_objects)))
            IStatusMessage(self.request).addStatusMessage(
                msg, type='error')


class MoveItemsFormView(layout.FormWrapper, BrowserView):
    """ View to move selected items into another location
    """

    form = MoveItemsForm

    def __init__(self, context, request):
        layout.FormWrapper.__init__(self, context, request)

    def render(self):
        if not self.request.get('paths') and not \
                self.form_instance.widgets['request_paths'].value:
            msg = _(u'You have not selected any items')
            IStatusMessage(self.request).addStatusMessage(
                msg, type='error')

            # redirect to the right tabbedview_tab
            if self.request.form.get('orig_template'):

                return self.request.RESPONSE.redirect(
                    self.request.form.get('orig_template'))
            # fallback documents tab
            else:
                return self.request.RESPONSE.redirect(
                    '%s#documents' % self.context.absolute_url())
        return super(MoveItemsFormView, self).render()


class NotInContentTypes(Invalid):
    __doc__ = _(u"It isn't allowed to add such items there")


class DestinationValidator(validator.SimpleFieldValidator):
    """Validator for destination-path.
    We check the destinations allowed content-type. If one or more source-types
    are not allowed in the destination, we raise an error
    """

    def validate(self, value):
        super(DestinationValidator, self).validate(value)

        # Allowed contenttypes for destination-folder
        allowed_types = [t.getId() for t in value.allowedContentTypes()]

        # Paths to source object
        source = self.view.widgets['request_paths'].value.split(';;')

        # Get source-brains
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        src_brains = portal_catalog(path={'query': source, 'depth': 0})
        failed_objects = []

        # Look for invalid contenttype
        for src_brain in src_brains:
            if not src_brain.portal_type in allowed_types:
                failed_objects.append(src_brain.Title.decode('utf8'))

        # If we found one or more invalid contenttypes, we raise an error
        if failed_objects:
            raise NotInContentTypes(
                _(u"error_NotInContentTypes ${failed_objects}",
                  default=u"It isn't allowed to add such items there: " +
                  "${failed_objects}", mapping=dict(
                      failed_objects=',<br>'.join(failed_objects))))

validator.WidgetValidatorDiscriminators(
    DestinationValidator, field=IMoveItemsSchema['destination_folder'])
provideAdapter(DestinationValidator)
