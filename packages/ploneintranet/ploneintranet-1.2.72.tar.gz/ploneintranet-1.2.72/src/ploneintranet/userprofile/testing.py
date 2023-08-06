# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2
from ploneintranet.testing import PLONEINTRANET_FIXTURE
from zope.configuration import xmlconfig

import ploneintranet.layout
import ploneintranet.todo
import ploneintranet.userprofile


class PloneintranetuserprofileLayer(PloneSandboxLayer):

    defaultBases = (
        PLONE_APP_CONTENTTYPES_FIXTURE,
        PLONEINTRANET_FIXTURE
    )

    products = ('Products.membrane', )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        xmlconfig.file(
            'configure.zcml',
            ploneintranet.layout,
            context=configurationContext
        )
        xmlconfig.file(
            'configure.zcml',
            ploneintranet.userprofile,
            context=configurationContext
        )
        xmlconfig.file(
            'configure.zcml',
            ploneintranet.docconv.client,
            context=configurationContext
        )
        xmlconfig.file(
            'configure.zcml',
            ploneintranet.search,
            context=configurationContext
        )
        xmlconfig.file(
            'configure.zcml',
            ploneintranet.todo,
            context=configurationContext
        )
        for p in self.products:
            z2.installProduct(app, p)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ploneintranet.layout:default')
        applyProfile(portal, 'ploneintranet.userprofile:testing')
        setRoles(portal, TEST_USER_ID, ['Manager'])

    def tearDownZope(self, app):
        """Tear down Zope."""
        for p in reversed(self.products):
            z2.uninstallProduct(app, p)


PLONEINTRANET_USERPROFILE_FIXTURE = PloneintranetuserprofileLayer()

PLONEINTRANET_USERPROFILE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEINTRANET_USERPROFILE_FIXTURE,),
    name="PloneintranetuserprofileLayer:Integration"
)
PLONEINTRANET_USERPROFILE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONEINTRANET_USERPROFILE_FIXTURE,),
    name="PloneintranetuserprofileLayer:Functional"
)

PLONEINTRANET_USERPROFILE_BROWSER_TESTING = FunctionalTesting(
    bases=(PLONEINTRANET_USERPROFILE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PloneintranetuserprofileLayer:Browser"
)
