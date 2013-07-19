from AccessControl import Unauthorized
from Acquisition import aq_inner
from ZODB.POSException import ConflictError
from collective.quickupload import logger
from collective.quickupload.browser.uploadcapable import upload_lock
from collective.quickupload.interfaces import IQuickUploadFileSetter
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.registry.interfaces import IRegistry
from zope import component
from zope.container.interfaces import INameChooser
from zope.component import getUtility
import transaction


class WorkspaceQuickUploadCapableFileFactory(object):
    """Workspace specific Quick upload Adapter"""

    def __init__(self, context):
        self.context = aq_inner(context)

    def __call__(
        self, filename, title, description, content_type, data, portal_type):
        context = aq_inner(self.context)
        error = ''
        result = {}
        result['success'] = None
        charset = context.getCharset()
        name = filename.decode(charset)
        name, ext = name.rsplit('.', 1)

        # check the given portal type with the
        # qu addable types from the registry
        registry = getUtility(IRegistry)
        upload_addable = registry.get(
            'ftw.tabbedview.interfaces.ITabbedView.quickupload_addable_types')

        if portal_type not in upload_addable and upload_addable:
            portal_type = upload_addable[0]

        normalizer = component.getUtility(IIDNormalizer)
        chooser = INameChooser(self.context)

        temp = normalizer.normalize(name)
        newid = chooser.chooseName(temp, context)

        title = name

        # copied from collective.quickupload
        upload_lock.acquire()
        try:
            transaction.begin()
            try:
                context.invokeFactory(
                    type_name=portal_type,
                    id=newid,
                    title=title,
                    description=description)

            except Unauthorized:
                error = u'serverErrorNoPermission'
            except ConflictError:
                # rare with xhr upload / happens sometimes with flashupload
                error = u'serverErrorZODBConflict'
            except Exception, e:
                error = u'serverError'
                logger.exception(e)

            if error:
                error = u'serverError'
                logger.info("An error happens with setId from filename, "
                            "the file has been created with a bad id, "
                            "can't find %s", newid)
            else:
                obj = getattr(context, newid)
                if obj:
                    error = IQuickUploadFileSetter(obj).set(
                        data, filename, content_type)

                obj.processForm()

            #@TODO : rollback if there has been an error
            transaction.commit()
        finally:
            upload_lock.release()

        result['error'] = error
        if not error:
            result['success'] = obj
        return result
