from ftw.meeting.interfaces import IMeeting
from ftw.workspace import _
from ftw.workspace.browser.previews.default import DefaultPreview
from ftw.workspace.interfaces import IWorkspacePreview
from plone.namedfile.interfaces import IAvailableSizes
from Products.CMFCore.utils import getToolByName
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from zope.interface import Interface

HTML = """
<div class="MeetingPreviewWrapper">
    <h2>{title}</h2>
    <p>Datum: {date}</p>
    <p>Time: {time}</p>
</div>
"""


class MeetingPreview(DefaultPreview):
    """Default preview"""

    implements(IWorkspacePreview)
    adapts(IMeeting, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def preview(self):
        return HTML.format(
            **{'title': self.context.Title(),
               'date': self.context.start().strftime('%d.%m.%Y'),
               'time': self.context.start().strftime('%H:%M')+" - " +
               self.context.end().strftime('%H:%M')})

    def full_url(self):
        return self.context.absolute_url()

    def get_scale_properties(self):
        sizes = getUtility(IAvailableSizes)()
        return sizes.get('workspace_preview', (200, 200))

    def preview_type(self):
        return 'html'

    def download_url(self):
        return None
