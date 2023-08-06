from plone import api
import logging

from Products.CMFPlone.interfaces import INavigationSchema
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


log = logging.getLogger(__name__)


def setupVarious(context):
    log.info('setupVarious')
    portal = api.portal.get()
    catalog = api.portal.get_tool('portal_catalog')
    if len(catalog(portal_type='ploneintranet.library.app')) == 0:
        api.content.create(
            type='ploneintranet.library.app',
            title='Library',
            container=portal)

    # profiles/default/registry.xml has no effect
    registry = getUtility(IRegistry)
    nav_settings = registry.forInterface(INavigationSchema, prefix="plone")
    plone_utils = api.portal.get_tool('plone_utils')
    nav_settings.displayed_types = tuple(plone_utils.getUserFriendlyTypes())
