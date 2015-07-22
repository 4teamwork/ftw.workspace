from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from ftw.bumblebee.utils import get_representation_url
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PreviewOverlay(BrowserView):
    """Preview tab for workspace"""

    template = ViewPageTemplateFile('overlay.pt')

    def __call__(self):
        return self.template()

