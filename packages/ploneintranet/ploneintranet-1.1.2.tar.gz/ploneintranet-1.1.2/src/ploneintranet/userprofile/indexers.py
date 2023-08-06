from ploneintranet.userprofile.content.userprofile import IUserProfile
from Products.membrane.interfaces import IMembraneUserObject
from plone.indexer.decorator import indexer


@indexer(IUserProfile)
def Title(ob, **kw):
    """Add support for the Title index/metadata from Products.membrane"""
    user = IMembraneUserObject(ob, None)
    if user:
        return user.get_full_name()
    return ""
