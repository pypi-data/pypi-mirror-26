# coding=utf-8
from AccessControl import Unauthorized
from plone import api
from plone.dexterity.utils import safe_unicode
from plone.memoize.view import memoize
from plone.tiles import Tile
from ploneintranet import api as piapi
from ploneintranet.core import ploneintranetCoreMessageFactory as _
from ploneintranet.network.interfaces import INetworkGraph
from ploneintranet.userprofile.content.userprofile import IUserProfile
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import logging
import urllib


logger = logging.getLogger(__name__)


class StreamBase(object):
    """Shared base class for activity streams"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.tag = None  # only used in TagStream below
        if 'last_seen' in request:
            self.last_seen = request.get('last_seen')
        else:
            self.last_seen = None
        self.stop_asking = False

    @property
    @memoize
    def count(self):
        ''' The count can be configured through the b_size parameter
        '''
        try:
            return int(self.request.form.get('b_size'))
        except TypeError:
            return 5

    @property
    def stream_filter(self):
        """we now default to the 'human' filter - but not in the TagStream"""
        return self.request.get('stream_filter', 'human')

    @property
    def next_max(self):
        if self.last_seen:
            return long(self.last_seen) - 1
        else:
            return None

    @property
    @memoize
    def toLocalizedTime(self):
        ''' Facade for the toLocalizedTime method
        '''
        return api.portal.get_tool('translation_service').toLocalizedTime

    @property
    @memoize
    def microblog_context(self):
        ''' Returns the microblog context
        '''
        return piapi.microblog.get_microblog_context(self.context)

    def filter_statusupdates(self, statusupdates):
        ''' This method filters the microblog StatusUpdates

        The idea is:
         - if a StatusUpdate is a comment return the parent StatusUpdate
         - show threads only once

        Additionally:
        - if a content_context has multiple content share posts,
          suppress older content shares without replies.

        The effectiveness of this is limited by the autoexpand:
        the current view "sees" only it's current 15 updates.

        Additionally, this performs a postprocessing filter on content updates
        in case a user has access to a microblog_context workspace
        but not to the (unpublished) content_context object
        '''
        seen_thread_ids = set()
        seen_content_contexts = set()
        good_statusupdates = []
        container = piapi.microblog.get_microblog()

        for su in statusupdates:
            if su.thread_id and su.thread_id in seen_thread_ids:
                # a reply on a toplevel we've already seen
                continue
            elif su.id in seen_thread_ids:
                # a toplevel we've already seen
                continue

            if su.thread_id:
                # resolve reply into toplevel
                thread_su = container.get(su.thread_id)
            else:
                thread_su = su

            # process a thread only once
            seen_thread_ids.add(thread_su.id)

            # content updates postprocessing filter
            try:
                content_context = su.content_context
            except Unauthorized:
                # skip thread on inaccessible content (e.g. draft)
                continue

            # double content share filter works on original reply/toplevel
            if content_context:
                if content_context in seen_content_contexts \
                   and not su.thread_id:
                    # older toplevel share, suppress
                    continue
                seen_content_contexts.add(content_context)

            good_statusupdates.append(thread_su)

        return good_statusupdates

    def get_statusupdates(self):
        ''' This will return all the StatusUpdates which are not comments

        The activity are sorted by reverse chronological order
        '''
        container = piapi.microblog.get_microblog()
        post_id = self.request.get('post_id')
        if post_id:
            try:
                return [container.get(post_id)]
            except KeyError:
                return []

        if self.microblog_context:
            # support ploneintranet.workspace integration
            statusupdates = container.context_values(
                self.microblog_context,
                max=self.next_max,
                limit=self.count,
            )
        elif IUserProfile.providedBy(self.context):
            # Get the updates for this user
            statusupdates = container.user_values(
                self.context.username,
                max=self.next_max,
                limit=self.count,
            )
        elif self.stream_filter == 'network':
            # Only activities from people and things I follow
            graph = api.portal.get_tool("ploneintranet_network")
            users = graph.unpack(graph.get_following(u'user'))
            users.append(api.user.get_current().id)  # show own updates also
            tags = graph.unpack(graph.get_following(u'tag'))
            statusupdates = container.values(
                max=self.next_max,
                limit=self.count,
                users=users,
                tags=tags
            )
        elif self.stream_filter == 'content':
            # show only content updates and replies to those
            statusupdates = container.is_content_values(
                max=self.next_max,
                limit=self.count,
            )
        elif self.stream_filter == 'human':
            # exclude auto-created content updates without replies
            statusupdates = container.is_human_values(
                max=self.next_max,
                limit=self.count,
            )
        elif self.stream_filter in ('interactions', 'posted', 'likes'):
            raise NotImplementedError("unsupported stream filter: %s"
                                      % self.stream_filter)
        else:
            # default implementation: all activities
            statusupdates = container.values(
                max=self.next_max,
                limit=self.count,
                tags=self.tag
            )
        return statusupdates

    @property
    @memoize
    def statusupdates_autoexpand(self):
        ''' The list of our activities
        '''
        # unfiltered for autoexpand management
        statusupdates = [x for x in self.get_statusupdates()]

        # filtered for display
        for su in self.filter_statusupdates(statusupdates):
            yield su

        # stop autoexpand when last batch is empty
        if len(statusupdates) == 0:
            self.stop_asking = True
        else:
            self.last_seen = statusupdates[-1].id

    @property
    @memoize
    def post_views(self):
        ''' The activity as views
        '''
        for statusupdate in self.statusupdates_autoexpand:
            yield api.content.get_view(
                'post.html',
                statusupdate,
                self.request
            )


class StreamTile(StreamBase, Tile):
    '''Stream as a tile, for use in other views (dashboard etc.)'''

    index = ViewPageTemplateFile("templates/stream_tile.pt")


@implementer(IPublishTraverse)
class TagStream(StreamBase, BrowserView):
    """Show the stream, filtered by a tag.

    Gets tag from the url.
    For example, /tagstream/foo will display
    the stream of activities tagged #foo.
    """

    @property
    def stream_filter(self):
        """do not apply the default 'human' filter"""
        return None

    def publishTraverse(self, request, name):
        if isinstance(name, unicode):
            self.tag = name
        else:
            self.tag = name.decode('utf8')
        # stop traversing, we have arrived
        request['TraversalRequestNameStack'] = []
        # return self so the publisher calls this view
        return self

    def handle_action(self):
        g = queryUtility(INetworkGraph)
        if g.is_following('tag', self.tag):
            g.unfollow('tag', self.tag)
        else:
            g.follow('tag', self.tag)

    @property
    def show_stream(self):
        """Optimize by not rendering stream on POST"""
        return self.request.method == 'GET'

    @property
    def following(self):
        g = queryUtility(INetworkGraph)
        return g.is_following('tag', self.tag)

    @property
    def url(self):
        return "{}/@@tagstream/{}".format(
            self.context.absolute_url(),
            urllib.quote(safe_unicode(self.tag).encode('utf8'))
        )

    def __call__(self):
        if self.request.method == 'POST':
            self.handle_action()
        if not self.tag:
            api.portal.show_message(
                message=_('No tag selected'),
                request=self.request,
                type="warning",
            )
            return self.request.response.redirect(self.context.absolute_url())
        return super(TagStream, self).__call__()
