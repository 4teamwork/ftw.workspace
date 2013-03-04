from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.pdfgenerator.view import MakoLaTeXView
from ftw.table import helper
from ftw.workspace import _
from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.interfaces import IWorkspaceDetailsListingProvider
from zope.component import adapts
from zope.component import getAdapters
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implements
from ftw.workspace.utils import has_ftwfile


class WorkspaceDetailsView(MakoLaTeXView):
    adapts(IWorkspace, Interface, ILaTeXLayout)

    template_directories = ['templates']
    template_name = 'details.tex'

    def get_render_arguments(self):
        self.layout.use_package('pdflscape')
        self.layout.use_package('longtable')
        self.layout.use_package('array,supertabular')

        args = {}
        args.update(self.get_labels())
        args.update(self.get_workspace_metadata())
        args['listings'] = self.get_listings()

        return args

    def get_labels(self):
        labels = {
            'labelWorkspace': _(u'latex_label_workspace', u'Workspace'),
            'labelTitle': _(u'latex_label_title', u'Title'),
            'labelOwner': _(u'latex_label_owner', u'Owner'),
            'labelDescription': _(u'latex_label_description', u'Description'),
            }

        for key, value in labels.items():
            labels[key] = translate(value, context=self.request)

        return labels

    def get_workspace_metadata(self):
        return {
            'workspaceTitle': self.convert(self.context.Title()),
            'workspaceOwner': self.convert(self.get_owner()),
            'workspaceDescription': self.convert(self.context.Description()),
            'workspaceText': self.convert(self.context.getText()),
            }

    def get_owner(self):
        userid = self.context.getOwner(0).getId()
        acl_users = getToolByName(self.context, 'acl_users')
        user = acl_users.getUserById(userid)
        return user and user.getProperty('fullname', userid) or userid

    def get_listings(self):
        providers = getAdapters((
                self.context, self.request, self.layout, self),
                                IWorkspaceDetailsListingProvider)
        providers = [provider for name, provider in providers]
        providers.sort(key=lambda p: p.get_sort_key())

        listings = []

        for provider in providers:
            title = provider.get_title()
            latex = provider.get_listing()
            if latex is not None:
                listings.append((title, latex))

        return listings


class FilesListing(object):
    implements(IWorkspaceDetailsListingProvider)
    adapts(IWorkspace, Interface, ILaTeXLayout, Interface)

    template = ViewPageTemplateFile('templates/files_listing.pt')

    def __init__(self, context, request, layout, view):
        self.context = context
        self.request = request
        self.layout = layout
        self.view = view

    def get_sort_key(self):
        return 10

    def get_title(self):
        return translate(_(u'latex_label_files', u'Files'),
                         context=self.request)

    def get_listing(self):
        if len(self._brains()) == 0:
            return None
        else:
            return self.view.convert(self.template())

    def get_items(self):
        """Returns all items to be displayed.
        """
        ftwfile = has_ftwfile(self.context)
        for brain in self._brains():
            yield {'title': brain.Title,
                   'effective': helper.readable_date(
                        brain, getattr(
                        brain, ftwfile and 'documentDate' or 'effective')),
                   'modified': helper.readable_date(
                        brain, getattr(brain, 'modified')),
                   'creator': self.get_creator(brain),
                   }

    def _brains(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {'path': '/'.join(self.context.getPhysicalPath()),
                 'portal_type': ['File'],
                 'sort_on': 'created',
                 'sort_order': 'reverse'}

        return catalog(query)

    def get_creator(self, brain):
        userid = brain.Creator
        acl_users = getToolByName(self.context, 'acl_users')
        user = acl_users.getUserById(userid)
        return user and user.getProperty('fullname', userid) or userid
