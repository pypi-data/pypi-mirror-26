# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_chain
from BTrees.OOBTree import OOBTree
from collective.workspace.pas import purge_workspace_pas_cache
from plone import api
from plone.dexterity.utils import iterSchemata
from plone.rfc822.interfaces import IPrimaryField
from ploneintranet.layout.app import IApp
from ploneintranet.workspace.interfaces import IWorkspaceFolder
from Products.CMFCore.interfaces import ISiteRoot
from urllib2 import urlparse
from zope.annotation import IAnnotations
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.schema import getFieldsInOrder

import config
import logging
import mimetypes


pl_message = MessageFactory('plonelocales')
log = logging.getLogger(__name__)

ANNOTATION_KEY = "ploneintranet.workspace.invitation_storage"

# The type map is used to deduct clear text names for classes and labels
# from portal types
TYPE_MAP = {
    'Event': 'event',
    'Folder': 'folder',
    'Document': 'rich document',
    'todo': 'task',
    'ploneintranet.workspace.mail': 'email',
    'ploneintranet.workspace.workspacefolder': 'workspace',
}


def get_storage(clear=False):
    """helper function to get annotation storage on the portal

    :param clear: If true is passed in, annotations will be cleared
    :returns: portal annotations
    :rtype: IAnnotations

    """
    portal = getUtility(ISiteRoot)
    annotations = IAnnotations(portal)
    if ANNOTATION_KEY not in annotations or clear:
        annotations[ANNOTATION_KEY] = OOBTree()
    return annotations[ANNOTATION_KEY]


def send_email(recipient,
               subject,
               message,
               sender="ploneintranet@netsight.co.uk"):
    """helper function to send an email with the sender preset

    """
    try:
        api.portal.send_email(
            recipient=recipient,
            sender=sender,
            subject=subject,
            body=message)
    except ValueError, e:
        log.error("MailHost error: {0}".format(e))


def parent_workspace(context):
    """ Return containing workspace
        Returns None if not found.
    """
    if IWorkspaceFolder.providedBy(context):
        return context
    for parent in aq_chain(context):
        if IWorkspaceFolder.providedBy(parent):
            return parent


def in_workspace(context):
    return IWorkspaceFolder.providedBy(parent_workspace(context))


def parent_app(context):
    """ Return containing workspace
        Returns None if not found.
    """
    if IApp.providedBy(context):
        return context
    for parent in aq_chain(context):
        if IApp.providedBy(parent):
            return parent


def in_app(context):
    return IApp.providedBy(parent_workspace(context))


def set_cookie(request, cookie_name, value):
    """
    Set a cookie to store state.
    This is mainly used by the sidebar to store what grouping was chosen
    """
    full_path = urlparse.urlparse(request.getURL()).path
    if not full_path:  # Test Requests may contain an empty path
        cookie_path = '/TestInstance'
    else:
        cookie_path = '/{0}'.format(full_path.split('/')[1])

    if (cookie_name in request and
        request.get(cookie_name) != value) or \
            cookie_name not in request:
        request.response.setCookie(
            cookie_name, value, path=cookie_path)


def guess_mimetype(file_name):
    content_type = mimetypes.guess_type(file_name)[0]
    # sometimes plone mimetypes registry could be more powerful
    if not content_type:
        mtr = api.portal.get_tool('mimetypes_registry')
        oct = mtr.globFilename(file_name)
        if oct is not None:
            content_type = str(oct)

    return content_type


def map_content_type(mimetype, portal_type=''):
    """
    takes a mimetype and returns a content type string as used in the
    prototype
    """
    content_type = ''
    if portal_type:
        content_type = TYPE_MAP.get(portal_type)

    if not content_type:
        if not mimetype or '/' not in mimetype:
            return content_type

        major, minor = mimetype.split('/')

        if mimetype in config.PDF:
            content_type = 'pdf'
        elif mimetype in config.DOC:
            content_type = 'word'
        elif mimetype in config.PPT:
            content_type = 'powerpoint'
        elif mimetype in config.ZIP:
            content_type = 'zip'
        elif mimetype in config.XLS:
            content_type = 'excel'
        elif mimetype in config.URI:
            content_type = 'link'
        elif mimetype in config.NEWS:
            content_type = 'news'

        elif major == 'text':
            content_type = 'rich document'
        elif major == 'audio':
            content_type = 'sound'
        elif major == 'video':
            content_type = 'video'
        elif major == 'image':
            content_type = 'image'

    return content_type


def purge_and_refresh_security_manager():
    """ This is necessary in case you have a cache on your acl_users folder.

    This method purges the configured cache on the acl_users folder and
    reinitialises the security manager for the current user.

    This is necessary as example when we are creating a workspace and right
    afterwards transition it into the private state. The transition is guarded
    by the TeamManager role which the current user just got when the workspace
    was created. This is however not yet reflected in the cached user object.
    This would not be an issue in the next upcoming request as the security
    context will be rebuilt then, but in the current request, this is a
    problem.
    """
    # Purge the cache on the current request object
    purge_workspace_pas_cache()

    # purge the acl_users cache
    acl_users = api.portal.get_tool('acl_users')
    if acl_users.ZCacheable_enabled():
        acl_users.ZCacheable_invalidate()

    # reinitialise the security manager
    current_user_id = api.user.get_current().getId()
    current_user = acl_users.getUser(current_user_id)
    newSecurityManager(None, current_user)


def get_primary_field(obj):
    primary = None
    for i in iterSchemata(obj):
        fields = getFieldsInOrder(i)
        for name, field in fields:
            if IPrimaryField.providedBy(field):
                primary = (name, field)
                break
    return primary
