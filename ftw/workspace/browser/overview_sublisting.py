from ftw.workspace import _
from ftw.workspace.browser.overview import ListingHelper
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.component import getUtility


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
                dict(title=type_,
                     objects=objects)
            )

            result.sort(key=lambda x: x['title'])

        return result
