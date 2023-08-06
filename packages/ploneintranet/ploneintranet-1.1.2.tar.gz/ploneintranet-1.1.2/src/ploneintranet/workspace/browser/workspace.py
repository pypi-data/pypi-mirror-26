from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from collective.workspace.interfaces import IWorkspace
from plone import api
from plone.memoize.view import memoize
from zope.interface import implements
from plone.app.blocks.interfaces import IBlocksTransformEnabled
import ploneintranet.api as pi_api
from ploneintranet.workspace.interfaces import IWorkspaceState
from ploneintranet.workspace.utils import parent_workspace
from json import dumps


class BaseWorkspaceView(BrowserView):
    """
    Base view class for workspace related view
    """
    @memoize
    def workspace(self):
        """Acquire the root workspace of the current context"""
        return parent_workspace(self.context)

    def can_manage_workspace(self):
        """
        does this user have permission to manage the workspace
        """
        return api.user.has_permission(
            "ploneintranet.workspace: Manage workspace",
            obj=self.context,
        )

    def can_add_status_updates(self):
        """
        Does this user have the permission to add status updates
        """
        return api.user.has_permission(
            "Plone Social: Add Microblog Status Update",
            obj=self.context)


class WorkspaceView(BaseWorkspaceView):
    """
    Default View of the workspace
    """
    implements(IBlocksTransformEnabled)


class WorkspaceState(BaseWorkspaceView):
    """
    Information about the state of the workspace
    """

    implements(IWorkspaceState)

    @memoize
    def state(self):
        if self.workspace() is not None:
            return api.content.get_state(self.workspace())


def format_users_json(users):
    """
    Format a list of users as JSON for use with pat-autosuggest

    :param list users: A list of user brains
    :rtype string: JSON {"user_id1": "user_title1", ...}
    """
    formatted_users = []
    for user in users:
        fullname = safe_unicode(user.Title)
        email = safe_unicode(user.email)
        uid = user.getId
        formatted_users.append({
            'id': uid,
            'text': u'{0} <{1}>'.format(fullname, email),
        })
    return dumps(formatted_users)


class ImagePickerJson(BrowserView):
    """
    Returns Images in current Workspace in a redactor json format
    [
        {
            "id": 1,
            "title": "Air Canada Landmark Agreement",
            "url": "/media/air-canada-landmark-agreement.jpg",
            "thumb": "/media/air-canada-landmark-agreement.jpg"
        },
        {
            "id": 2,
            "title": "A380",
            "url": "/media/air-france-a380.jpg",
            "thumb": "/media/air-france-a380.jpg",
        }
    ]
    """

    def __call__(self):
        catalog = api.portal.get_tool('portal_catalog')
        results = catalog(
            portal_type='Image',
            path={'query': '/'.join(self.context.getPhysicalPath())}
        )
        images = [
            {
                'id': img['getId'],
                'title': img['Title'],
                'url': img.getURL(),
                'thumb': '%s/@@images/image/preview' % img.getURL(),
            } for img in results
        ]
        return dumps(images)


class ImagePickerPanel(BrowserView):
    """
    Renders HTML for the image picker panel/modal of pat-raptor.
    """

    def get_images(self):
        catalog = api.portal.get_tool('portal_catalog')
        ps = catalog(
            portal_type='Image',
            path={'query': '/'.join(self.context.getPhysicalPath())}
        )
        return ps


class WorkspaceMembersJSONView(BrowserView):
    """
    Return workspace members in JSON for use with pat-autosuggest.
    Only members of the current workspace are found.
    """
    def __call__(self):
        q = safe_unicode(self.request.get('q', '').strip())
        if not q:
            return ""
        query = {'SearchableText': u'{0}*'.format(q)}
        users = pi_api.userprofile.get_users(
            context=self.context, full_objects=False, **query)
        return format_users_json(users)


class AllUsersJSONView(BrowserView):
    """
    Return a filtered list of users for pat-autosuggest.
    Any user can be found, not only members of the current workspace
    """
    def __call__(self):
        q = safe_unicode(self.request.get('q', '').strip())
        if not q:
            return ""
        query = {'SearchableText': u'{0}*'.format(q)}
        users = pi_api.userprofile.get_user_suggestions(
            context=self.context, full_objects=False, **query)
        return format_users_json(users)


class AllGroupsJSONView(BrowserView):
    """
    Return all groups in JSON for use in picker
    TODO: consolidate AllGroupsJSONView with AllUsersJSONView
    """
    def __call__(self):
        q = self.request.get('q', '').lower()
        groups = api.group.get_groups()
        group_details = []
        ws = IWorkspace(self.context)
        for group in groups:
            groupid = group.getId()
            if groupid == self.context.id:
                # don't add group to itself
                continue
            # XXX Filter out groups representing workspace roles. Review
            # whether we need/want this and/or can do it more efficiently.
            skip = False
            for special_group in ws.available_groups:
                if groupid.startswith('{}:'.format(special_group)):
                    skip = True
                    break
            if group.getProperty('state') == 'secret':
                skip = True
            if skip:
                continue
            title = group.getProperty('title') or groupid
            email = group.getProperty('email')
            if email:
                title = '%s <%s>' % (title, email)
            description = group.getProperty('description') or ''
            if q in title.lower() or q in description.lower():
                group_details.append({
                    'text': title,
                    'id': groupid,
                })
        return dumps(group_details)


class AllUsersAndGroupsJSONView(BrowserView):
    def __call__(self):
        q = self.request.get('q', '').strip()
        if not q:
            return ""
        acl_users = api.portal.get_tool('acl_users')
        results = []
        groups = acl_users.searchGroups(id=q)
        if groups:
            for group in groups:
                text = group['title'] or group['id']
                results.append({'id': group['id'], 'text': text})
        query = {'SearchableText': u'{0}*'.format(safe_unicode(q))}
        users = pi_api.userprofile.get_users(full_objects=False, **query)
        for user in users:
            fullname = user.Title
            email = user.email
            results.append({
                'id': user.getId,
                'text': u'{0} <{1}>'.format(fullname, email),
            })
        return dumps(results)
