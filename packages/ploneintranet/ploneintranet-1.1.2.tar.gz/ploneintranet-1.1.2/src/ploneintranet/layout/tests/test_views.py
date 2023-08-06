# coding=utf-8
from json import loads
from mock import patch
from plone import api
from ploneintranet import api as pi_api
from ploneintranet.layout.adapters.app_tiles import BaseTile
from ploneintranet.layout.interfaces import IPloneintranetLayoutLayer
from ploneintranet.layout.testing import IntegrationTestCase
from zope.interface import alsoProvides


class FakeCurrentUser(object):
    ''' This mocks a membrane user ofr out tests
    '''


class TestViews(IntegrationTestCase):

    def setUp(self):
        ''' Custom shared utility setup for tests.
        '''
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.folder = api.content.create(
            container=self.portal,
            type='Folder',
            title='Test contextless folder'
        )
        alsoProvides(self.request, IPloneintranetLayoutLayer)

    def get_view(self, name, obj=None, **params):
        ''' Retutn a view with a fresh request on the context of obj
        If obj is None use the portal
        '''
        if obj is None:
            obj = self.portal
        request = self.request.clone()
        request.form.update(params)
        return api.content.get_view(name, obj, request)

    def test_date_picker_i18n_json(self):
        ''' We want pat-date-picker i18n
        '''
        view = self.get_view('date-picker-i18n.json')
        observed = loads(view())
        expected = {
            u'nextMonth': u'next_month_link',
            u'previousMonth': u'prev_month_link',
            u'months': [
                u'January',
                u'February',
                u'March',
                u'April',
                u'May',
                u'June',
                u'July',
                u'August',
                u'September',
                u'October',
                u'November',
                u'December'
            ],
            u'weekdays': [
                u'Sunday',
                u'Monday',
                u'Tuesday',
                u'Wednesday',
                u'Thursday',
                u'Friday',
                u'Saturday'
            ],
            u'weekdaysShort': [
                u'Sun',
                u'Mon',
                u'Tue',
                u'Wed',
                u'Thu',
                u'Fri',
                u'Sat'
            ]
        }
        self.assertDictEqual(
            observed,
            expected,
        )

    def test_dashboard_tiles(self):
        ''' Check if the dashboard tiles are correctly configured
        through the registry
        '''
        view = self.get_view('dashboard.html')
        self.assertTupleEqual(
            view.activity_tiles(),
            (
                u'./@@contacts_search.tile',
                u'./@@news.tile',
                u'./@@my_documents.tile',
            )
        )
        self.assertTupleEqual(
            view.task_tiles(),
            (
                u'./@@contacts_search.tile',
                u'./@@news.tile',
                u'./@@my_documents.tile',
                u'./@@workspaces.tile?workspace_type=ploneintranet.workspace.workspacefolder',  # noqa
                u'./@@workspaces.tile?workspace_type=ploneintranet.workspace.case',   # noqa
                u'./@@events.tile',
                u'./@@tasks.tile',
            )
        )

    def test_apps_view(self):
        ''' Check the @@apps view
        '''
        view = self.get_view('apps.html')
        self.assertListEqual(
            [tile.sorting_key for tile in view.tiles()],
            [
                (10, u'contacts'),
                (20, u'messages'),
                (30, u'todo'),
                (40, u'calendar'),
                (50, u'slide-bank'),
                (60, u'image-bank'),
                (70, u'news'),
                (80, u'case-manager'),
                (90, u'app-market'),
            ]
        )

    def get_app_tile(self, path=''):
        ''' Return a fresh app tile with the given path
        '''
        tile = BaseTile(self.portal)
        tile.path = path
        return tile

    def test_app_basetile_not_found(self):
        ''' Check the not_found property of the app tile adapter
        '''
        # The path is empty, so we have nothing to look for
        tile = self.get_app_tile()
        self.assertTrue(tile.not_found)

        # if we set a path, we have to find it event if we are anonymous
        tile = self.get_app_tile('dashboard.html')
        self.assertFalse(tile.not_found)

        tile = self.get_app_tile('dashboard.html')
        with api.env.adopt_roles({'Anonymous'}):
            self.assertFalse(tile.not_found)

    def test_app_basetile_unauthorized(self):
        ''' Check the unauthorized property of the app tile adapter
        '''
        # If we have not set a path, we cannot traverse to anything,
        # so we cannot say if it is authorized or not
        tile = self.get_app_tile()
        with self.assertRaises(AttributeError):
            tile.unauthorized

        # If we set an existing path, we will have a different response
        # according to our roles in context
        tile = self.get_app_tile('dashboard.html')
        self.assertFalse(tile.unauthorized)

        tile = self.get_app_tile('dashboard.html')
        with api.env.adopt_roles({'Anonymous'}):
            self.assertTrue(tile.unauthorized)

    def test_app_basetile_url(self):
        ''' Check the url property of the app tile adapter
        '''
        # If we do not set a path the tile url defaults to app-not-available
        tile = self.get_app_tile()
        self.assertEqual(
            tile.url,
            'http://nohost/plone/app-not-available.html#document-content'
        )

        # Otherwise the tile knows how to transform the path in to a url
        tile = self.get_app_tile('dashboard.html')
        self.assertEqual(tile.url, 'http://nohost/plone/dashboard.html')

        # The tile should be disabled if the path is not allowed
        tile = self.get_app_tile('dashboard.html')
        with api.env.adopt_roles({'Anonymous'}):
            self.assertEqual(tile.url, 'http://nohost/plone/dashboard.html')

    def test_app_basetile_modal(self):
        ''' Check the modal property of the app tile adapter
        '''
        # With an empty path, when clicking on a tile,
        # we will get an alert in a modal
        tile = self.get_app_tile()
        self.assertEqual(tile.modal, 'pat-modal')

        # Otherwise we will open the tile
        tile = self.get_app_tile('dashboard.html')
        self.assertEqual(tile.modal, '')

        # Even if we are unauthorized
        tile = self.get_app_tile('dashboard.html')
        with api.env.adopt_roles({'Anonymous'}):
            self.assertEqual(tile.modal, '')

    def test_app_basetile_disabled(self):
        ''' Check the disabled property of the app tile adapter
        '''
        # The tile should be disabled if path is not set (default)
        tile = self.get_app_tile()
        self.assertEqual(tile.disabled, 'disabled')

        # The tile should be enabled because the path is allowed
        tile = self.get_app_tile('dashboard.html')
        self.assertEqual(tile.disabled, '')

        # The tile should be disabled if the path is not allowed
        tile = self.get_app_tile('dashboard.html')
        with api.env.adopt_roles({'Anonymous'}):
            self.assertEqual(tile.disabled, 'disabled')

    def test_webstats_js(self):
        ''' Check if the view works and if it is correctly cached
        '''
        NEW_JS = u'<div>webstats_js</div>'
        OLD_JS = api.portal.get_registry_record('plone.webstats_js')

        view1_portal = self.get_view('webstats_js')
        view1_folder = self.get_view('webstats_js', obj=self.folder)
        view2_portal = self.get_view('webstats_js',)
        # Test empty registry record
        self.assertEqual(view1_portal(), OLD_JS)
        self.assertEqual(view1_folder(), OLD_JS)

        # Test modified registry record
        api.portal.set_registry_record('plone.webstats_js', NEW_JS)

        # This comes from cache
        self.assertEqual(view1_portal(), OLD_JS)
        self.assertEqual(view1_folder(), OLD_JS)
        # this does not
        self.assertEqual(view2_portal(), NEW_JS)

        # reset the registry record
        api.portal.set_registry_record('plone.webstats_js', OLD_JS)

    def test_dashboard_view_default_dashboard(self):
        ''' Check the various methods of the dashboard view
        '''
        view = self.get_view('dashboard.html')
        # we are not a membrane user so persistency will not work
        # the default is to return activity
        self.assertEqual(pi_api.userprofile.get_current(), None)
        self.assertEqual(view.default_dashboard(), 'activity')

        # but we can ask for everything
        view = self.get_view('dashboard.html', dashboard='test')
        self.assertEqual(view.default_dashboard(), 'test')

        # now we use a fake user for testing the persistency
        with patch(
            'ploneintranet.api.userprofile.get_current',
            return_value=FakeCurrentUser(),
        ):
            view = self.get_view('dashboard.html', dashboard='evil')
            self.assertEqual(view.default_dashboard(), 'evil')
            user = pi_api.userprofile.get_current()
            # value is not set because it is not a good one
            with self.assertRaises(AttributeError):
                user.dashboard_default
            # if we specify a good one it will be set correctly
            view = self.get_view('dashboard.html', dashboard='task')
            self.assertEqual(view.default_dashboard(), 'task')
            self.assertEqual(user.dashboard_default, 'task')
            # now the view default persists to task, and not to activity
            view = self.get_view('dashboard.html')
            self.assertEqual(view.default_dashboard(), 'task')
            self.assertEqual(user.dashboard_default, 'task')
