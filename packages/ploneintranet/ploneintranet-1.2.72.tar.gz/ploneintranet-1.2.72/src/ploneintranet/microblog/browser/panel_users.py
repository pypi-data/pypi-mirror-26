# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ploneintranet import api as pi_api
from .update_social import UpdateSocialBase
from plone.memoize.view import memoize_contextless


class Users(UpdateSocialBase):

    index = ViewPageTemplateFile('templates/panel_users.pt')
    input_name = 'users:list'
    input_type = 'checkbox'
    panel_id = 'panel-users'
    panel_type = 'mentions'

    user_ids = []
    selected_users = []
    selected_user_ids = []

    @property
    @memoize_contextless
    def selected_users(self):
        ''' Returns the selected users
        according to the "mentions" parameter in the request
        '''
        query = {'exact_getUserId': self.request.form.get('mentions', [])}
        user_generator = pi_api.userprofile.get_users(
            full_objects=False, **query)
        return list(user_generator)

    @property
    @memoize_contextless
    def selected_user_ids(self):
        ''' Returns the selected user ids
        according to the "mentions" parameter in the request
        '''
        return [user.getId for user in self.selected_users]

    @property
    @memoize_contextless
    def users(self):
        '''Get the users that match the usersearch filter.

        Users are sorted on fullname
        '''
        q = u'*%s*' % safe_unicode(
            self.request.form.get('usersearch', '').strip())
        q = q.replace('**', '')
        query = {'SearchableText': q}
        # We can only mention users that are enabled
        query['review_state'] = 'enabled'
        users = pi_api.userprofile.get_users(
            context=self.context, full_objects=False, **query)
        return sorted(users, key=lambda x: x.Title)

    @property
    @memoize_contextless
    def user_ids(self):
        ''' Returns the filtered user ids sorted by id
        '''
        return sorted([user.getId for user in self.users])

    @memoize_contextless
    def get_avatar_by_userid(self, userid):
        return pi_api.userprofile.avatar_tag(
            username=userid,
        )


class User(Users):

    index = ViewPageTemplateFile('templates/panel_users.pt')
    input_name = 'user'
    input_type = 'radio'
    panel_id = 'panel-user'
    panel_type = 'user'
