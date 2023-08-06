from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.CMFPlone import utils
from Products.CMFPlone.browser.interfaces import INavigationBreadcrumbs
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from Products.Five import BrowserView
from plone.app.layout.navigation.root import getNavigationRoot
from ploneintranet.layout.interfaces import INoBarcelonetaLayer
from zope.component import getMultiAdapter
from zope.interface import implements


class OneLevelBreadcrumbs(BrowserView):
    # Only show first level breadcrumbs, nothing else.  Note that in
    # workspaces we override this to show two levels.
    levels = 1
    implements(INavigationBreadcrumbs)

    def breadcrumbs(self):
        if not INoBarcelonetaLayer.providedBy(self.request):
            # We are in the CMS, so we want the default.
            view = getMultiAdapter(
                (self.context, self.request), name='orig_breadcrumbs_view')
            return tuple(view.breadcrumbs())
        context = aq_inner(self.context)
        context_path = '/'.join(context.getPhysicalPath())
        root_path = getNavigationRoot(context)
        if context_path == root_path:
            # We are the navigation root.
            return ()
        # We now iteratively look for a parent and check if this is
        # the navigation root.
        chain = aq_chain(context)
        for index, parent in enumerate(chain):
            try:
                parent_path = '/'.join(parent.getPhysicalPath())
            except AttributeError:
                # This is probably the root request object, so we
                # somehow did not find a suitable parent.
                return ()
            if parent_path == root_path:
                # We have found the root.
                break
            # The parent is not yet the navigation root, so set the
            # item and try the next parent in the chain.
            item = parent
        # Get the interesting part of the chain.
        chain = list(reversed(chain[:index]))
        # Some things want to be hidden from the breadcrumbs.
        chain = [
            elem for elem in chain
            if not IHideFromBreadcrumbs.providedBy(elem)]
        # Restrict to the wanted maximum of levels
        chain = chain[:self.levels]
        crumbs = []
        for item in chain:
            crumbs.append(
                {'absolute_url': item.absolute_url(),
                 'Title': utils.pretty_title_or_id(item, item)})
        return tuple(crumbs)


class TwoLevelBreadcrumbs(OneLevelBreadcrumbs):
    levels = 2
