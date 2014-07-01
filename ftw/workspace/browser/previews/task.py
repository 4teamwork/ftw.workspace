from ftw.task.interfaces import ITask
from ftw.workspace.browser.previews.default import DefaultPreview
from ftw.workspace.interfaces import IWorkspacePreview
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from ftw.task.browser.task import getUserInfos

HTML = """
<div class="MeetingPreviewWrapper" i18n:domain="ftw.workspace">
    <h2>{title}</h2>
    <p>{label_state} {state}</p>
    <p>{label_due_date} {duedate}</p>
    <p>{label_responsible} {responsible}
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
        state = self.context.portal_workflow.getInfoFor(self.context,
                                                        'review_state')
        state = self.context.translate(state)
        return HTML.format(
            **{'title': self.context.Title(),
               'state': state,
               'duedate': self.context.end_date.strftime('%d.%m.%Y %H:%M'),
               'responsible': ', '.join(user_id),
               'label_responsible': self.context.translate(
                    'label_responsible',
                    default="responsible",
                    domain="ftw.workspace"),
                'label_due_date': self.context.translate('label_due_date',
                                                         default="due date:",
                                                         domain="ftw.workspace").encode('utf8'),
                'label_state': self.context.translate('label_state',
                                                         default="state:",
                                                         domain="ftw.workspace"),

               })

    def full_url(self):
        return self.context.absolute_url()

    def preview_type(self):
        return 'html'
