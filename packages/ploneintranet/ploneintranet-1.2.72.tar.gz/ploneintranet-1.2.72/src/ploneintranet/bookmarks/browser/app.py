# coding=utf-8
from collections import defaultdict
from DateTime import DateTime
from datetime import date
from plone import api
from plone.app.blocks.interfaces import IBlocksTransformEnabled
from plone.memoize.view import memoize
from ploneintranet import api as pi_api
from ploneintranet.bookmarks.browser.base import BookmarkView
from ploneintranet.core import ploneintranetCoreMessageFactory as _
from ploneintranet.layout.interfaces import IAppView
from ploneintranet.search.interfaces import ISiteSearch
from zope.component import getUtility
from zope.i18nmessageid.message import Message
from zope.interface import implementer


@implementer(IAppView, IBlocksTransformEnabled)
class View(BookmarkView):
    ''' The view for this app
    '''
    app_name = 'bookmarks'

    app_types = [
        'ploneintranet.layout.app',
        'ploneintranet.news.app',
    ]
    document_types = [
        'Document', 'File', 'Image'
    ]
    people_types = [
        'ploneintranet.userprofile.userprofile',
    ]

    @property
    def workspace_types(self):
        return [
            portal_type for portal_type
            in api.portal.get_registry_record(
                'ploneintranet.workspace.workspace_type_filters'
            )
        ]

    def is_bookmarked(self, uid):
        ''' Check if an object is bookmarked by uid
        '''
        return self.ploneintranet_network.is_bookmarked('content', uid)

    @memoize
    def get_sortable_title(self, bookmark):
        ''' Return the bookmark sorting key
        '''
        title = bookmark.title
        if callable(title):
            title = title()
        if isinstance(title, Message):
            title = self.context.translate(title)
        return title.strip().lower()

    def get_first_letter(self, bookmark):
        title = self.get_sortable_title(bookmark)
        if not title:
            return _('No title')
        letter = title[0].upper()
        if isinstance(letter, unicode):
            letter = letter.encode('utf8')
        return letter

    def sort_bookmarks(self, bookmarks):
        ''' We want to sort the bookmarks by title,
        and title can be be an i18n Message
        '''
        return sorted(bookmarks, key=self.get_sortable_title)

    def my_bookmarks_of_type(self, portal_types=[]):
        ''' Get all the bookmarked content of the following portal_types
        '''
        query = self.request.get('SearchableText', '').lower()
        search_util = getUtility(ISiteSearch)
        uids = list(self.ploneintranet_network.get_bookmarks('content'))
        if not uids:
            return []
        response = search_util.query(
            query,
            filters={
                'UID': uids,
                'portal_type': portal_types,
            },
            step=9999,
        )
        return tuple(response)

    @memoize
    def my_bookmarked_workspaces(self):
        ''' Get all the bookmarked workspaces
        '''
        return self.my_bookmarks_of_type(self.workspace_types)

    @memoize
    def my_bookmarked_documents(self):
        ''' Get all the bookmarked documents
        '''
        return self.my_bookmarks_of_type(self.document_types)

    @memoize
    def my_bookmarked_apps(self):
        ''' Get all the bookmarked apps
        '''
        return self.my_bookmarks_of_type(self.app_types)

    @memoize
    def my_bookmarked_people(self):
        ''' Get all the bookmarked apps
        '''
        return self.my_bookmarks_of_type(self.people_types)

    @memoize
    def my_bookmarks(self):
        ''' Lookup all the bookmarks
        '''
        bookmarks = self.my_bookmarks_of_type()
        return tuple(sorted(bookmarks, key=self.get_sortable_title))

    @memoize
    def my_recent_bookmarks(self, limit=10):
        ''' Lookup my recent bookmarks
        '''
        userid = api.user.get_current().id
        dates = self.ploneintranet_network._bookmarked_on.get(userid, {})
        bookmarks = sorted(
            self.my_bookmarks_of_type(),
            key=lambda bookmark: dates.get(bookmark.UID),
            reverse=True,
        )
        return tuple(bookmarks[:limit])

    @memoize
    def most_popular_bookmarks(self, limit=10):
        ''' Lookup my recent bookmarks
        '''
        content = self.ploneintranet_network._bookmarked["content"]
        sorted_uids = sorted(
            content,
            key=lambda uid: len(content[uid])
        )
        # We slice this list taking a lot of margin
        # with respect to the requested limit
        # In fact, not all the content is visibility to the authenticated user
        # Hopefully the most bookmarked are also the most public ones
        sorted_uids = sorted_uids[-limit * 5:]
        if not sorted_uids:
            return ()

        search_util = getUtility(ISiteSearch)
        response = search_util.query(
            filters={
                'UID': sorted_uids,
            },
            step=limit * 5,
        )

        # Sort the response results by their
        # reversed position in the sorted_uids list
        response = sorted(
            response,
            key=lambda result: - sorted_uids.index(result.UID)
        )
        return tuple(response[:limit])

    @memoize
    def my_bookmarks_by_created(self):
        ''' Get all the bookmarked objects grouped by creation date
        '''
        items = defaultdict(list)
        today = date.today()
        for bookmark in self.my_bookmarks():
            try:
                created = bookmark.context['created']
            except KeyError:
                created = None
            if isinstance(created, DateTime):
                created = created.asdatetime()
            if hasattr(created, 'date'):
                day_past = (today - created.date()).days
            else:
                # happens, e.g., for apps
                day_past = 100
            if day_past < 1:
                period = _('Today')
            elif day_past < 7:
                period = _('Last week')
            elif day_past < 30:
                period = _('Last month')
            else:
                period = _('All time')
            items[period].append(bookmark)
        return items

    @memoize
    def my_bookmarks_by_bookmarked(self):
        ''' Get all the bookmarked objects grouped by bookmark date
        '''
        items = defaultdict(list)
        today = date.today()
        pn = self.ploneintranet_network
        userid = api.user.get_current().id
        for bookmark in self.my_bookmarks():
            bookmarked_on = pn.bookmarked_on(bookmark.UID, userid)
            if hasattr(bookmarked_on, 'date'):
                day_past = (today - bookmarked_on.date()).days
            else:
                # happens, e.g., for apps
                day_past = 100
            if day_past < 1:
                period = _('Today')
            elif day_past < 7:
                period = _('Last week')
            elif day_past < 30:
                period = _('Last month')
            else:
                period = _('All time')
            items[period].append(bookmark)
        return items

    @memoize
    def my_bookmarks_by_letter(self):
        ''' Get all the bookmarked objects grouped by first letter
        '''
        items = defaultdict(list)
        for bookmark in self.my_bookmarks():
            items[self.get_first_letter(bookmark)].append(bookmark)
        return items

    @memoize
    def my_bookmarks_by_workspace(self):
        ''' Get all the bookmarked objects grouped by workspace
        '''
        items = defaultdict(list)
        workspaces = api.portal.get()['workspaces']
        workspaces_path = '/'.join(workspaces.getPhysicalPath() + ('', ))
        for bookmark in self.my_bookmarks():
            try:
                path = bookmark.getPath()
            except AttributeError:
                # happens, e.g., for apps
                path = u''
            if path.startswith(workspaces_path):
                ws = workspaces.get(path.split('/')[3])
                if ws:
                    key = ws.title
                else:
                    key = _('Not in a workspace')
            else:
                key = _('Not in a workspace')
            items[key].append(bookmark)
        return items

    @memoize
    def my_bookmarks_grouped(self):
        ''' Get all the bookmarked objects grouped
        '''
        group_by = self.request.get('group_by', '')
        if group_by == 'workspace':
            return self.my_bookmarks_by_workspace()
        elif group_by == 'created':
            return self.my_bookmarks_by_created()
        elif group_by == 'bookmarked':
            return self.my_bookmarks_by_bookmarked()
        return self.my_bookmarks_by_letter()

    @memoize
    def my_bookmarks_sorted_groups(self):
        ''' The groups of my partition sorted
        '''
        group_by = self.request.get('group_by', '')
        if group_by in ('bookmarked', 'created'):
            return [
                _('Today'),
                _('Last week'),
                _('Last month'),
                _('All time'),
            ]

        groups = sorted(self.my_bookmarks_grouped())
        # We want this one to be at the end
        for key in (_('No title'), _('Not in a workspace')):
            if key in groups:
                value = groups.pop(groups.index(key))
                groups.append(value)
        return groups

    @property
    @memoize
    def apps_view(self):
        ''' Return the apps view
        '''
        return api.content.get_view(
            'apps.html',
            api.portal.get(),
            self.request,
        )

    def get_avatar_by_userid(self, userid):
        ''' Provide HTML tag to display the avatar
        '''
        return pi_api.userprofile.avatar_tag(
            username=userid,
        )
