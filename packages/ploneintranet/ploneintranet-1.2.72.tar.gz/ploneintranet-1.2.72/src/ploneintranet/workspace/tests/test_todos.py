# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from datetime import date
from datetime import timedelta
from plone import api
from ploneintranet import api as pi_api
from ploneintranet.workspace.tests.base import BaseTestCase
from zope.annotation import IAnnotations
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class TestTodos(BaseTestCase):
    """Test Todo items in Case Workspaces"""

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        pwft = api.portal.get_tool("portal_placeful_workflow")
        self.workspaces = api.content.create(
            type='ploneintranet.workspace.workspacecontainer',
            title='workspaces',
            container=self.portal,
        )
        self.case = api.content.create(
            type='ploneintranet.workspace.case',
            title='case',
            container=self.workspaces,
        )
        self.case.manage_addProduct[
            'CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        wfconfig = pwft.getWorkflowPolicyConfig(self.case)
        wfconfig.setPolicyIn('case_workflow')
        api.content.transition(self.case, 'assign')

    def test_todo_reopen_earlier_milestone(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='new',
        )
        api.content.transition(case_todo, 'finish')
        case_todo.reopen()
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'open',
        )

    def test_todo_reopen_current_milestone(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='prepare',
        )
        api.content.transition(case_todo, 'finish')
        case_todo.reopen()
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'open',
        )

    def test_todo_reopen_future_milestone(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='archived',
        )
        api.content.transition(case_todo, 'finish')
        case_todo.reopen()
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'planned',
        )

    def test_todo_initial_state_open(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='new',
        )
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'open',
        )

    def test_todo_initial_state_planned(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='complete',
        )
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'planned',
        )

    def test_todo_update_state_to_open(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='archived',
        )
        case_todo.milestone = 'new'
        notify(ObjectModifiedEvent(case_todo))
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'open',
        )

    def test_todo_update_state_to_planned(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='new',
        )
        case_todo.milestone = 'archived'
        notify(ObjectModifiedEvent(case_todo))
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'planned',
        )

    def test_update_todo_state_when_case_state_is_changed(self):
        wft = self.portal.portal_workflow
        pwft = api.portal.get_tool("portal_placeful_workflow")

        case2 = api.content.create(
            type='ploneintranet.workspace.case',
            title='case',
            container=self.workspaces,
        )
        case2.manage_addProduct[
            'CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        wfconfig = pwft.getWorkflowPolicyConfig(case2)
        wfconfig.setPolicyIn('case_workflow')

        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=case2,
            milestone='prepare',
        )

        self.assertEquals(wft.getInfoFor(case_todo, 'review_state'), 'planned')
        api.content.transition(case2, 'assign')
        self.assertEquals(wft.getInfoFor(case_todo, 'review_state'), 'open')

    def test_reject_case(self):
        """
        Rejecting a Case should set 'open' Todo items to 'planned'
        """
        wft = self.portal.portal_workflow
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='new',
        )
        self.assertEquals(wft.getInfoFor(case_todo, 'review_state'), 'open')

        api.content.transition(self.case, 'reject')
        self.assertEquals(wft.getInfoFor(case_todo, 'review_state'), 'planned')

        case_todo.milestone = 'bogus'
        api.content.transition(self.case, 'reset')
        self.assertEquals(wft.getInfoFor(case_todo, 'review_state'), 'planned')

        api.content.transition(self.case, 'reject')
        case_todo.milestone = 'new'
        api.content.transition(self.case, 'reset')
        self.assertEquals(wft.getInfoFor(case_todo, 'review_state'), 'open')

    def get_tasks(self, obj):
        ''' Get the tasks for this object
        '''
        return api.content.get_view(
            'view',
            obj,
            self.request.clone(),
        ).tasks()

    def test_todo_sorting(self):
        ''' Check if we can effectively sort todos

        They are sorted by due date if set, and otherwise by
        getObjPositionInParent.
        '''
        case = api.content.create(
            type='ploneintranet.workspace.case',
            title='case-test-sorting',
            container=self.workspaces,
        )

        pwft = api.portal.get_tool('portal_placeful_workflow')
        dispatcher = case.manage_addProduct['CMFPlacefulWorkflow']
        dispatcher.manage_addWorkflowPolicyConfig()
        wfconfig = pwft.getWorkflowPolicyConfig(case)
        wfconfig.setPolicyIn('case_workflow')
        api.content.transition(case, 'assign')

        api.content.create(
            type='todo',
            title='todo1',
            container=case,
            milestone='new',
        )
        api.content.create(
            type='todo',
            title='todo2',
            container=case,
            milestone='new',
        )
        self.assertEqual(
            [todo['title'] for todo in self.get_tasks(case)['new']],
            ['todo1', 'todo2'],
        )
        case.moveObjectsUp(['todo2'])
        self.assertEqual(
            [todo['title'] for todo in self.get_tasks(case)['new']],
            ['todo2', 'todo1'],
        )

        case.todo1.due = date.today()
        case.todo1.reindexObject()
        self.assertEqual(
            [todo['title'] for todo in self.get_tasks(case)['new']],
            ['todo1', 'todo2'],
        )

        case.todo2.due = date.today() - timedelta(days=1)
        case.todo2.reindexObject()
        self.assertEqual(
            [todo['title'] for todo in self.get_tasks(case)['new']],
            ['todo2', 'todo1'],
        )


class TestCasePermissioningTodos(BaseTestCase):
    """
        Test permission settings in Cases based on assignee status on a Todo
    """

    def setUp(self):
        super(TestCasePermissioningTodos, self).setUp()
        self.login_as_portal_owner()
        self.profile1 = pi_api.userprofile.create(
            username='janedoe',
            email='janedoe@doe.com',
            properties=dict(
                first_name=u'Jäne',
                last_name=u'Doe',
            )
        )
        self.profile2 = pi_api.userprofile.create(
            username='bobdoe',
            email='bobdoe@doe.com',
            properties=dict(
                fist_name=u'Bøb',
                last_name=u'Doe',
            )
        )
        self.portal = self.layer['portal']
        pwft = api.portal.get_tool("portal_placeful_workflow")
        self.workspaces = api.content.create(
            type='ploneintranet.workspace.workspacecontainer',
            title='workspaces',
            container=self.portal,
        )
        self.case = api.content.create(
            type='ploneintranet.workspace.case',
            title='case',
            container=self.workspaces,
        )
        # Add janedoe as member to the case
        self.add_user_to_workspace('janedoe', self.case)

        self.case.manage_addProduct[
            'CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        wfconfig = pwft.getWorkflowPolicyConfig(self.case)
        wfconfig.setPolicyIn('case_workflow')
        self.case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='prepare',
        )
        self.logout()

    def traverse_to_item(self, item):
        """ helper method to travers to an item by path """
        return api.content.get(path='/'.join(item.getPhysicalPath()))

    def logout(self):
        """
        Delete any cached localrole information from the request.
        """
        super(TestCasePermissioningTodos, self).logout()
        annotations = IAnnotations(self.request)
        keys_to_remove = []
        for key in annotations.keys():
            if (
                isinstance(key, basestring) and
                key.startswith('borg.localrole')
            ):
                keys_to_remove.append(key)
            if (
                isinstance(key, tuple) and
                key[0] == 'workspaces'
            ):
                keys_to_remove.append(key)

        for key in keys_to_remove:
            annotations.pop(key)

    def test_basic_permissioning(self):
        """
            Member janedoe can access the todo and the case, bobdoe cannot
        """
        self.login('janedoe')
        self.traverse_to_item(self.case_todo)
        self.traverse_to_item(self.case)
        self.logout()
        self.login('bobdoe')
        # bobdoe cannot access the todo and the case
        with self.assertRaises(Unauthorized):
            self.traverse_to_item(self.case_todo)
        with self.assertRaises(Unauthorized):
            self.traverse_to_item(self.case)

    def test_gain_permission_in_current_milestone(self):
        """
            Bobdoe is assigned to a Todo, and the Todo's milestone is currently
            active. He gains access immediately.
        """
        self.login('janedoe')
        self.case_todo.assignee = 'bobdoe'
        self.case_todo.milestone = 'new'
        notify(ObjectModifiedEvent(self.case_todo))
        self.logout()
        self.login('bobdoe')
        # bobdoe can access the Case and the Todo
        self.traverse_to_item(self.case_todo)
        self.traverse_to_item(self.case)

    def test_remove_permission_when_unassigned(self):
        """
            Bobdoe is assigned to a Todo, and the Todo's milestone is currently
            active. He is then unassigned again. He loses access.
        """
        self.login('janedoe')
        self.case_todo.assignee = 'bobdoe'
        self.case_todo.milestone = 'new'
        notify(ObjectModifiedEvent(self.case_todo))
        existing_users = self.case.existing_users_by_id()
        # bobdoe is now a Guest member of the case
        self.assertTrue('bobdoe' in existing_users)
        self.assertEqual(existing_users['bobdoe']['role'], 'Guest')
        self.case_todo.assignee = ''
        notify(ObjectModifiedEvent(self.case_todo))
        existing_users = self.case.existing_users_by_id()
        # bobdoe is no longer a Guest member of the case
        self.assertFalse('bobdoe' in existing_users)
        self.logout()
        self.login('bobdoe')
        # bobdoe cannot access the todo and the case
        with self.assertRaises(Unauthorized):
            self.traverse_to_item(self.case_todo)
        with self.assertRaises(Unauthorized):
            self.traverse_to_item(self.case)

    def test_no_permission_in_inactive_milestone(self):
        """
            Bobdoe is assigned to a Todo, and the Todo's milestone is currently
            not active. He does not gain access.
        """
        self.login('janedoe')
        self.case_todo.assignee = 'bobdoe'
        self.logout()
        self.login('bobdoe')
        # bobdoe cannot access the todo and the case
        # because the todo's milestone is not yet active
        with self.assertRaises(Unauthorized):
            self.traverse_to_item(self.case_todo)
        with self.assertRaises(Unauthorized):
            self.traverse_to_item(self.case)

    def test_gain_permission_in_activated_milestone(self):
        """
            Bobdoe is assigned to a Todo, and the Todo's milestone is currently
            not active. The Case is switched to that milestone. He then gains
            access.
        """
        self.login('janedoe')
        self.case_todo.assignee = 'bobdoe'
        self.logout()
        self.login_as_portal_owner()
        self.assertFalse('bobdoe' in self.case.existing_users_by_id())
        # Switch the case workflow to the task's milestone
        api.content.transition(self.case, 'assign')
        existing_users = self.case.existing_users_by_id()
        # bobdoe is now a Guest member of the case
        self.assertTrue('bobdoe' in existing_users)
        self.assertEqual(existing_users['bobdoe']['role'], 'Guest')
        self.logout()
        self.login('bobdoe')
        self.traverse_to_item(self.case_todo)
        self.traverse_to_item(self.case)

    def test_remove_permission_in_inactive_milestone(self):
        """
            Bobdoe is assigned to a Todo, and the Todo's milestone is currently
            active. The Case is then switched to another milestone. He then
            loses access.
        """
        self.login_as_portal_owner()
        self.case_todo.assignee = 'bobdoe'
        self.case_todo.milestone = 'new'
        notify(ObjectModifiedEvent(self.case_todo))
        # Switch the case workflow away from the task's milestone
        api.content.transition(self.case, 'assign')
        self.logout()
        self.login('bobdoe')
        # bobdoe can no longer access the case and the todo
        with self.assertRaises(Unauthorized):
            self.traverse_to_item(self.case_todo)
        with self.assertRaises(Unauthorized):
            self.traverse_to_item(self.case)

    def test_keep_permission_when_still_assigned(self):
        """
            Bobdoe is assigned to 2 Todos, which have 2 different milestones.
            The Case workflow is switched away from the 1st Todo's milestone
            and reaches the 2nd Todo's milestone. He keeps his access.
        """
        self.login('janedoe')
        self.case_todo.assignee = 'bobdoe'
        self.case_todo.milestone = 'new'
        notify(ObjectModifiedEvent(self.case_todo))
        # Create a second task, for milestone "prepare"
        case_todo2 = api.content.create(
            type='todo',
            title='Another Case ToDo',
            container=self.case,
            milestone='prepare',
        )
        case_todo2.assignee = 'bobdoe'
        self.logout()
        self.login_as_portal_owner()
        # Switch the case workflow away from the first task's milestone
        api.content.transition(self.case, 'assign')
        self.logout()
        self.login('bobdoe')
        # bobdoe can still access the case and the todo, since
        # case_todo2 is currently active
        self.traverse_to_item(self.case_todo)
        self.traverse_to_item(self.case)
        self.traverse_to_item(case_todo2)

    def test_no_permission_when_milestones_not_active(self):
        """
            Bobdoe is assigned to 2 Todos, which have 2 different milestones.
            The Case workflow is switched away from the 1st Todo's milestone
            and does not reach the 2nd Todo's milestone. He loses his access.
        """
        self.login('janedoe')
        self.case_todo.assignee = 'bobdoe'
        self.case_todo.milestone = 'new'
        notify(ObjectModifiedEvent(self.case_todo))
        # Create a second task, for milestone "prepare"
        case_todo2 = api.content.create(
            type='todo',
            title='Another Case ToDo',
            container=self.case,
            milestone='complete',
        )
        case_todo2.assignee = 'bobdoe'
        self.logout()
        self.login_as_portal_owner()
        # Switch the case workflow away from the task's milestone
        api.content.transition(self.case, 'assign')
        self.logout()
        self.login('bobdoe')
        # bobdoe can not access the case and the todos, since both are in a
        # milestone that is currently not active
        with self.assertRaises(Unauthorized):
            self.traverse_to_item(self.case_todo)
        with self.assertRaises(Unauthorized):
            self.traverse_to_item(self.case)
        with self.assertRaises(Unauthorized):
            self.traverse_to_item(case_todo2)

    def test_membership_is_kept_if_added_globally(self):
        """
            Bobdoe becomes a guest member of the case when he gets assigned to
            a Todo in an active milestone.
            Boddoe is then made into a regular team member. He keeps that
            membership even if the Case workflow moves away from the Todo's
            milestone.
        """
        self.login_as_portal_owner()
        self.case_todo.assignee = 'bobdoe'
        self.case_todo.milestone = 'new'
        notify(ObjectModifiedEvent(self.case_todo))
        existing_users = self.case.existing_users_by_id()
        # bobdoe is now a Guest member of the case
        self.assertTrue('bobdoe' in existing_users)
        self.assertEqual(existing_users['bobdoe']['role'], 'Guest')
        # Make bobdoe a regular member
        self.add_user_to_workspace('bobdoe', self.case)
        existing_users = self.case.existing_users_by_id()
        # bobdoe is now a regular member of the case
        self.assertTrue('bobdoe' in existing_users)
        self.assertNotEqual(existing_users['bobdoe']['role'], 'Guest')
        # Switch the case workflow away from the task's milestone
        api.content.transition(self.case, 'assign')
        self.logout()
        self.login('bobdoe')
        # bobdoe can still access the case and the todo, since
        # he is now a regular member
        self.traverse_to_item(self.case_todo)
        self.traverse_to_item(self.case)
