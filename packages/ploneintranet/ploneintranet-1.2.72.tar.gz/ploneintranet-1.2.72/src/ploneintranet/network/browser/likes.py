# -*- coding: utf-8 -*-
from plone import api
from plone.app.uuid.utils import uuidToCatalogBrain
from plone.memoize.view import memoize
from plone.protect import PostOnly
from ploneintranet import api as piapi
from ploneintranet.core import ploneintranetCoreMessageFactory as _
from ploneintranet.network.interfaces import INetworkTool
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import uuid


class NotAllowed(Exception):
    pass


class ToggleLike(BrowserView):
    """The view 'toggle_like' callable on a normal context.
    """

    index = ViewPageTemplateFile('templates/toggle_like.pt')

    def __init__(self, context, request):
        self.context = context  # the item being liked
        self.request = request
        self.util = getUtility(INetworkTool)
        self.item_id = api.content.get_uuid(self.context)
        self.like_type = "content"

    @property
    @memoize
    def likerids(self):
        ''' The id of the people that like this content
        '''
        return self.util.get_likers(
            self.like_type,
            item_id=self.item_id,
        )

    @property
    @memoize
    def likers(self):
        ''' The id of the people that like this content

        If it includes the current user, return Myself as the first element
        '''
        likers = []
        userid = api.user.get_current().id
        include_myself = False
        for likerid in self.likerids:
            if likerid == userid:
                include_myself = True
            else:
                liker = piapi.userprofile.get(likerid)
                if liker:
                    likers.append(liker.fullname)
                else:
                    likers.append(likerid)
        likers.sort()
        if include_myself:
            likers.insert(0, self.context.translate(_(u'Myself')))
        if not likers:
            return
        return _(
            'liked_by',
            default=u'Liked by: ${likers}',
            mapping={'likers': u', '.join(likers)}
        )

    def total_likes(self):
        return len(self.likerids)

    def __call__(self):
        """ """
        if not self.validate_id(self.item_id):
            return 'No valid item-id: %s' % self.item_id

        self.is_liked = self.util.is_liked(
            self.like_type,
            item_id=self.item_id,
        )

        # toogle like only if the button is clicked
        if 'like_button' in self.request:
            self.handle_toggle()

        if self.is_liked:
            self.verb = self.context.translate(_(u'Unlike'))
        else:
            self.verb = self.context.translate(_(u'Like'))
        self.unique_id = uuid.uuid4().hex
        return self.index()

    def action(self):
        return "%s/@@toggle_like" % self.context.absolute_url()

    def handle_toggle(self):
        """
        Perform the actual like/unlike action.
        Since this does a db write it cannot be called with a GET.
        """
        PostOnly(self.request)

        if not self.is_liked:
            self.util.like(self.like_type, self.item_id)
        else:
            self.util.unlike(self.like_type, self.item_id)
        self.is_liked = not self.is_liked

    def validate_id(self, item_id):
        """Check if item_id is a valid UUID"""
        if uuidToCatalogBrain(item_id) is not None:
            return True


@implementer(IPublishTraverse)
class ToggleLikeStatusUpdate(ToggleLike):
    """The special view 'toggle_like' callable on the navroot.

    This works around the limitation that you cannot traverse to a
    StatusUpdate.
    Instead of calling statusupdate/@@like we call portal/@@like/statusid

    It uses publishTraverse to allow passing the id of an object as a path:
    /@@toggle_like/1453656
    """

    index = ViewPageTemplateFile('templates/toggle_like.pt')

    def __init__(self, context, request):
        """Need to override __init__ to not fetch self.item_id from context"""
        self.context = context  # INavigationRoot
        self.request = request
        self.util = getUtility(INetworkTool)
        self.like_type = "update"

    def publishTraverse(self, request, name):
        """Extract self.item_id from URL /@@toggle_like/123456"""
        self.item_id = str(name)
        return self

    def __call__(self):
        """Because self.item_id is set via publishTraverse we need
        an extra check"""
        if not getattr(self, 'item_id', False):
            raise KeyError(
                _('No item id given in sub-path. '
                  'Use .../@@toggle_like/123456')
            )
        return super(ToggleLikeStatusUpdate, self).__call__()

    def action(self):
        portal_url = api.portal.get().absolute_url()
        return "/".join((portal_url,
                         '@@toggle_like_statusupdate',
                         self.item_id))

    def validate_id(self, item_id):
        """Check if the item_id is the id of a StatusUpdate"""
        if item_id.isdigit():
            container = piapi.microblog.get_microblog()
            if container and int(item_id) in container._status_mapping:
                return True
