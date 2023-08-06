# -*- coding: utf-8 -*-
from collective.workspace.interfaces import IWorkspace
from contextlib import contextmanager
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
from plone.testing import z2
from plone.testing.z2 import Browser
from ploneintranet.workspace.testing import PLONEINTRANET_WORKSPACE_FUNCTIONAL_TESTING  # noqa
from ploneintranet.workspace.testing import PLONEINTRANET_WORKSPACE_INTEGRATION_TESTING  # noqa

import unittest2 as unittest


@contextmanager
def temporary_registry_record(key, value):
    '''Temporarily set up a registry record
    '''
    pr = api.portal.get_tool('portal_registry')
    backup = pr._records[key].value
    pr._records[key].value = value
    try:
        yield value
    finally:
        pr._records[key].value = backup


class BaseTestCase(unittest.TestCase):

    layer = PLONEINTRANET_WORKSPACE_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.workspace_container = api.content.create(
            self.portal,
            'ploneintranet.workspace.workspacecontainer',
            'workspace-container',
            title='Workspace container'
        )
        self.request = self.portal.REQUEST
        self.portal_workflow = api.portal.get_tool('portal_workflow')

    def cleanup_request_annotations(self):
        ''' Invalidate the cache of the workspace
        '''
        try:
            delattr(self.request, '__anotations__')
        except AttributeError:
            pass

    def login(self, username):
        """
        helper method to login as specific user

        Before logging in cleanup the request annotations in case

        - some pas plugins is storing there informations about the current user
        - some memoized methods needs to be cleaned up

        :param username: the username of the user to add to the group
        :type username: str
        :rtype: None

        """
        self.cleanup_request_annotations()
        login(self.portal, username)

    def logout(self):
        """
        helper method to avoid importing the p.a.testing logout method
        """
        logout()

    def login_as_portal_owner(self):
        """
        helper method to login as site admin
        """
        z2.login(self.app['acl_users'], SITE_OWNER_NAME)

    def add_user_to_workspace(self, username, workspace, groups=None):
        """
        helper method which adds a user to team and then clears the cache

        :param username: the username of the user to add to the group
        :type username: str
        :param workspace: the workspace to add this user
        :type workspace: ploneintranet.workspace.workspacefolder
        :param groups: the groups to which this user should be added
        :type groups: set
        :rtype: None

        """
        IWorkspace(workspace).add_to_team(
            user=username,
            groups=groups,
        )


class FunctionalBaseTestCase(BaseTestCase):

    layer = PLONEINTRANET_WORKSPACE_FUNCTIONAL_TESTING

    def setUp(self):
        super(FunctionalBaseTestCase, self).setUp()
        self.browser = Browser(self.app)
        self.browser.handleErrors = False

    def browser_login_as_site_administrator(self):
        self.browser.open(self.portal.absolute_url() + '/login_form')
        self.browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        self.browser.getControl(name='__ac_password').value = \
            SITE_OWNER_PASSWORD
        self.browser.getForm(id='login-panel').submit()
