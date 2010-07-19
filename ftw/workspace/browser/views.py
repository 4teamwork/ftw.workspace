from Products.Five.browser import BrowserView


class GetOwnershipView(BrowserView):

    def __call__(self):
        userid = self.context.getOwner(0).getId()
        return userid and userid or ''
