from ftw.workspace.browser.overview import ListingHelper
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.i18n import translate


class Sublisting(BrowserView, ListingHelper):
    """Workspace sublisting"""

    def collect(self):
        registry = getUtility(IRegistry)
        types = registry.get('ftw.workspace.sublisting_types',
                             ['TabbedViewFolder'])

        result = []

        for type_ in types:
            query = {'portal_type': type_,
                     'sort_on': 'sortable_title'}

            objects = self.context.getFolderContents(contentFilter=query)

            if not objects:
                continue

            result.append(
                dict(title=self.translated_title(type_),
                     objects=objects)
            )

            result.sort(key=lambda x: x['title'])

        return result

    def translated_title(self, type_):
        portal_types = getToolByName(self.context, 'portal_types')
        fti = portal_types.get(type_, None)
        if fti is None or not fti.i18n_domain:
            domain = 'plone'
        else:
            domain = fti.i18n_domain

        if fti:
            title = fti.title
        else:
            title = type_

        return translate(msgid=title, domain=domain,
                         context=self.request)
