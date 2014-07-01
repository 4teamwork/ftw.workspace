from ftw.meeting.interfaces import IMeeting
from ftw.workspace.browser.previews.default import DefaultPreview
from ftw.workspace.interfaces import IWorkspacePreview
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


HTML = """
<div class="MeetingPreviewWrapper" i18n:domain="ftw.workspace">
    <h2>{title}</h2>
    <p>{date_label} {date}</p>
    <p>{time_label} {time}</p>
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
               'time': '%s - %s' % (self.context.start().strftime('%H:%M'),
                                    self.context.end().strftime('%H:%M')),
               'date_label': self.context.translate('label_date', default='date:', domain='ftw.workspace'),
               'time_label': self.context.translate('label_time', default='time:', domain='ftw.workspace'),
               })

    def full_url(self):
        return self.context.absolute_url()

    def preview_type(self):
        return 'html'

    def download_url(self):
        return '{0}/export_ics'.format(self.context.absolute_url())

    def detail_url(self):
        return self.context.absolute_url() + '/meeting_preview'
