from ftw.task.interfaces import ITask
from ftw.workspace.browser.previews.default import DefaultPreview
from ftw.workspace.interfaces import IWorkspacePreview
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from ftw.task.browser.task import getUserInfos

HTML = """
<div class="MeetingPreviewWrapper">
    <h2>{title}</h2>
    <p>Status: {state}</p>
    <p>F\xc3\xa4lligkeit: {duedate}</p>
    <p>Zust\xc3\xa4ndig: {responsible}
</div>
"""


class TaskPreview(DefaultPreview):
    """Default preview"""

    implements(IWorkspacePreview)
    adapts(ITask, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def preview(self):
        user_id = []
        for responsible in self.context.responsibility:
            user_id.append(getUserInfos(self.context, responsible)['name'])
        return HTML.format(
            **{'title': self.context.Title(),
               'state': self.context.portal_workflow.getInfoFor(self.context,'review_state'),
               'duedate': self.context.end_date.strftime('%d.%m.%Y %H:%M'),
               'responsible': ', '.join(user_id)
               })

    def full_url(self):
        return self.context.absolute_url()

    def preview_type(self):
        return 'html'
