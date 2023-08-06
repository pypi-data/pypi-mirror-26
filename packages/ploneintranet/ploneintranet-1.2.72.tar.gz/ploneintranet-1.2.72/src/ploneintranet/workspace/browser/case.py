# coding=utf-8
from plone import api
from plone.memoize.view import memoize
from ploneintranet.workspace.browser.workspace import WorkspaceView
from ploneintranet.workspace.interfaces import IMetroMap
from ploneintranet.workspace.utils import parent_workspace
from Products.Five import BrowserView


class CaseView(WorkspaceView):
    """Variant of the WorkspaceView with additional methods for Case Workspaces
    """

    @property
    @memoize
    def metromap_sequence(self):
        return IMetroMap(self.context).metromap_sequence

    def milestone_state(self, milestone_id):
        """
        Determine whether the milestone should be considered finished or not.

        If it is the last milestone and it has no tasks, the final node should
        be considered finished so that the line is all green.
        """
        mm_seq = self.metromap_sequence
        milestone_ids = mm_seq.keys()
        is_last = milestone_id == milestone_ids[-1]
        second_last_milestone_id = milestone_ids[-2]
        state = 'unfinished'
        if mm_seq[milestone_id].get('finished'):
            state = 'finished'
        elif is_last and mm_seq[second_last_milestone_id].get('finished'):
            tasks = self.tasks()
            if not tasks[milestone_id]:
                state = 'finished'
        return state

    @property
    def transition_icons(self):
        context = self.context
        workflow = IMetroMap(context)._metromap_workflow
        if not workflow:
            return {}
        if 'transition_icons' in workflow.variables:
            return workflow.getInfoFor(context, 'transition_icons', {})
        else:
            return {
                'assign': 'icon-right-hand',
                'finalise': 'icon-pin',
                'request': 'icon-right-circle',
                'submit': 'icon-right-circle',
                'decide': 'icon-hammer',
                'close': 'icon-cancel-circle',
                'archive': 'icon-archive',
            }


class CaseWorkflowGuardView(BrowserView):
    """Enable transition to the next workflow state when there are no open
    tasks
    """

    @memoize
    def __call__(self):
        workspace = parent_workspace(self.context)
        wft = api.portal.get_tool('portal_workflow')
        case_milestone = wft.getInfoFor(workspace, 'review_state')

        catalog = api.portal.get_tool('portal_catalog')
        workspace_path = '/'.join(workspace.getPhysicalPath())
        open_tasks = catalog(
            path=workspace_path,
            portal_type='todo',
            review_state='open',
        )
        # Only prevent the current milestone from being closed if there are
        # open tasks assigned to the current milestone.
        # This ignores open tasks assigned to earlier milestones since they
        # aren't represented in the metromap.
        for task in open_tasks:
            if task.getObject().milestone == case_milestone:
                return False
        return True


class FreezeView(BrowserView):

    @property
    def frozen_state(self):
        """
        A workflow variable defines which workflow state should be interpreted
        as the "frozen" state.
        """
        wft = api.portal.get_tool('portal_workflow')
        return wft.getInfoFor(self.context, 'frozen_state', None)

    @property
    def metromap_state(self):
        ''' Return the state of the metromap (actual or before freezing)
        '''
        if self.is_frozen():
            return self.pre_frozen_state
        else:
            return api.content.get_state(self.context)

    def can_be_frozen(self):
        """
        An item can only be frozen if the assigned workflow has a workflow
        state which is configured as the "frozen" state.
        """
        return bool(self.frozen_state)

    def is_frozen(self):
        review_state = api.content.get_state(self.context)
        return review_state == self.frozen_state

    def frozen_date(self):
        wft = api.portal.get_tool('portal_workflow')
        ts = api.portal.get_tool('translation_service')
        frozen_date = wft.getInfoFor(self.context, 'time')
        return ts.toLocalizedTime(frozen_date)

    @property
    def pre_frozen_state(self):
        wft = api.portal.get_tool('portal_workflow')
        wf_id = wft.getWorkflowsFor(self.context)[0].getId()
        history = self.context.workflow_history.get(wf_id)
        previous_wf = history[-2]
        return previous_wf.get('review_state')

    def unfreeze(self):
        ''' Unfreeze the context
        '''
        previous_state = self.pre_frozen_state
        if previous_state:
            api.content.transition(self.context, to_state=previous_state)
        else:
            api.content.transition(self.context, 'back_to_new')
        # If we don't explicitly reindex the Case, the solr query for the
        # workspaces view won't find it.
        self.context.reindexObject()


class UnfreezeView(FreezeView):
    """
    Return to the workflow state that the item was at before being frozen.
    """

    def __call__(self):
        ''' Unfreeze the context and redirect to its view
        '''
        self.unfreeze()
        self.request.response.redirect(self.context.absolute_url())
