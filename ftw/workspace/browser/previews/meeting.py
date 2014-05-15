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
    <h2> {title}</h2>
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
        return HTML.format(**{'title': self.context.Title()})
        return '<img height="200px" src="{0}" alt={1} title={1}/>'.format(
            self.full_url(),
            _(u'text_no_preview', default=u'No Preview')
            )

    def full_url(self):
        return self.context.absolute_url()

    def get_scale_properties(self):
        sizes = getUtility(IAvailableSizes)()
        return sizes.get('workspace_preview', (200, 200))

    def preview_type(self):
        return 'html'

    def download_url(self):
        return None
