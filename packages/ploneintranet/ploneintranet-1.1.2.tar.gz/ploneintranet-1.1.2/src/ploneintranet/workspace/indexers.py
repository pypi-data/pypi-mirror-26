# coding=utf-8
from .case import ICase
from datetime import datetime
from plone.app.contenttypes.interfaces import IDocument
from plone.app.contenttypes.interfaces import IFile
from plone.app.contenttypes.interfaces import IImage
from plone.app.contenttypes.interfaces import ILink
from plone.app.contenttypes.interfaces import INewsItem
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.utils import datify
from plone.indexer.decorator import indexer
from ploneintranet.workspace.workspacefolder import IWorkspaceFolder
from utils import guess_mimetype


@indexer(IDocument)
def mimetype_document(object, **kw):
    return object.format


@indexer(IFile)
def mimetype_file(object, **kw):
    if hasattr(object, 'file') and hasattr(object.file, 'filename'):
        mimetype = guess_mimetype(object.file.filename)
        if mimetype.strip():
            return mimetype
    return 'application/octet-stream'


@indexer(IImage)
def mimetype_image(object, **kw):
    if hasattr(object, 'image') and hasattr(object.image, 'filename'):
        mimetype = guess_mimetype(object.image.filename)
        if mimetype.strip():
            return mimetype
    return 'application/octet-stream'


@indexer(ILink)
def mimetype_link(object, **kw):
    return 'text/x-uri'


@indexer(INewsItem)
def mimetype_newsitem(object, **kw):
    return 'message/news'


@indexer(IDexterityContent)
def due_dexterity(obj):
    """
    dummy to prevent indexing child objects
    """
    raise AttributeError("This field should not indexed here!")


@indexer(ICase)
def due_case(obj):
    """
    :return: value of field due for cases
    """
    date = getattr(obj, 'due', None)
    date = datify(date)
    return date is None and datetime.max or date


@indexer(IDexterityContent)
def is_division_dexterity(obj):
    """
    dummy to prevent indexing child objects
    """
    raise AttributeError("This field should not indexed here!")


@indexer(IWorkspaceFolder)
def is_division(object, **kw):
    """Indexes if this object represents a division"""
    return getattr(object, 'is_division', False)


@indexer(IDexterityContent)
def is_archived_dexterity(obj):
    """
    The default search query is for all items which haven't been archived
    """
    return False


@indexer(IWorkspaceFolder)
def is_archived(object, **kw):
    """Indexes if this object is not archived

    Return False both when a workspace has no 'archival_date' attribute, and
    also when it is set to None.
    """
    return bool(getattr(object, 'archival_date'))


@indexer(IDexterityContent)
def division_dexterity(obj):
    """
    dummy to prevent indexing child objects
    """
    raise AttributeError("This field should not indexed here!")


@indexer(IWorkspaceFolder)
def division(object, **kw):
    """Indexes the division UID if present

    Since this index is a UUIDIndex it needs to return either a UID or None
    """
    return getattr(object, 'division', None) or None
