import unittest
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import helpers

from plone.testing import z2

from zope.configuration import xmlconfig


class PloneintranetinvitationsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ploneintranet.invitations
        xmlconfig.file(
            'configure.zcml',
            ploneintranet.invitations,
            context=configurationContext
        )

    def tearDownZope(self, app):
        pass

    def setUpPloneSite(self, portal):
        helpers.applyProfile(portal, 'ploneintranet.invitations:default')

PLONEINTRANET_INVITATIONS_FIXTURE = PloneintranetinvitationsLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEINTRANET_INVITATIONS_FIXTURE,),
    name='PloneintranetinvitationsLayer:Integration'
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONEINTRANET_INVITATIONS_FIXTURE, z2.ZSERVER_FIXTURE),
    name='PloneintranetinvitationsLayer:Functional'
)


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
