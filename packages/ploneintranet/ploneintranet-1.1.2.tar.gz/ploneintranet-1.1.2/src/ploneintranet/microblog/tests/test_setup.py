import unittest2 as unittest

from plone import api
from plone.browserlayer.utils import registered_layers

from ploneintranet.microblog.testing import\
    PLONEINTRANET_MICROBLOG_INTEGRATION_TESTING

PROJECTNAME = 'ploneintranet.microblog'

PERMISSIONS_MEMBER = (
    'Plone Social: Add Microblog Status Update',
    'Plone Social: View Microblog Status Update',
    'Plone Social: Modify Own Microblog Status Update',
    'Plone Social: Delete Own Microblog Status Update',
)
PERMISSIONS_MANAGER_ONLY = (
    'Plone Social: Modify Microblog Status Update',
    'Plone Social: Delete Microblog Status Update',
)


class TestInstall(unittest.TestCase):

    layer = PLONEINTRANET_MICROBLOG_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_product_is_installed(self):
        qi = self.portal['portal_quickinstaller']
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IPloneIntranetMicroblogLayer', layers)

    def test_permissions_member(self):
        expected = ['Manager', 'Member', 'Site Administrator']
        for permission in PERMISSIONS_MEMBER:
            roles = self.portal.rolesOfPermission(permission)
            roles = [r['name'] for r in roles if r['selected']]
            self.assertListEqual(roles, expected)

    def test_permissions_manager(self):
        expected = ['Manager', 'Site Administrator']
        for permission in PERMISSIONS_MANAGER_ONLY:
            roles = self.portal.rolesOfPermission(permission)
            roles = [r['name'] for r in roles if r['selected']]
            self.assertListEqual(roles, expected)

    def test_add_folder(self):
        testfolder = api.content.create(type='Folder',
                                        title='testfolder',
                                        container=self.portal)
        self.assertIn(testfolder.id, self.portal.objectIds())

    def test_tool_added(self):
        self.assertIn('ploneintranet_microblog', self.portal)


class TestUninstall(unittest.TestCase):

    layer = PLONEINTRANET_MICROBLOG_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IPloneIntranetMicroblogLayer', layers)

    def test_tool_removed(self):
        self.assertNotIn('ploneintranet_microblog', self.portal)
