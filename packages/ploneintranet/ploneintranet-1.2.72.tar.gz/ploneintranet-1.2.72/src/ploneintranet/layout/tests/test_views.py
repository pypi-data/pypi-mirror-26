# coding=utf-8
from contextlib import contextmanager
from json import loads
from lxml import html
from mock import patch
from plone import api
from ploneintranet import api as pi_api
from ploneintranet.layout.interfaces import IPloneintranetLayoutLayer
from ploneintranet.layout.testing import IntegrationTestCase
from ploneintranet.layout.utils import in_app
from Products.Five import BrowserView
from zope.i18n import translate
from zope.interface import alsoProvides


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


class FakeCurrentUser(object):
    ''' This mocks a membrane user ofr out tests
    '''


class AppWithParametersView(BrowserView):

    def __call__(self):
        return self.request.form


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
        self.create_apps()
        alsoProvides(self.request, IPloneintranetLayoutLayer)

    def create_apps(self):
        ''' We create addition apps for testing purposes
        '''
        for app in [
            {'title': 'Empty app', 'app': ''},
            {'title': 'Private app', 'app': 'robots.txt'},
            {'title': 'Public app', 'app': 'robots.txt'},
            {
                'title': 'App with parameters',
                'app': '@@app-with-parameters',
                'app_parameters': '{"foo": "bar"}'
            },
            {
                'title': 'Conditional App',
                'app': 'robots.txt',
                'condition': 'python:False',
            },
            {
                'title': 'Redirect App',
                'app': '@@app-redirect-to-url',
                'app_parameters': '{"url": "https://www.example.com"}',
            },
        ]:
            api.content.create(
                self.portal.apps,
                type='ploneintranet.layout.app',
                title=app['title'],
                app=app['app'],
                app_parameters=app.get('app_parameters', u''),
                condition=app.get('condition', ''),
            )
        api.content.transition(
            self.portal.apps['public-app'],
            to_state='published'
        )

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
                u'./@@bookmarks.workspaces.tile',
                u'./@@bookmarks.apps.tile',
                u'./@@bookmarks.tile?id_suffix=-dashboard',
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

        This is tricky, because apps may register tiles outside of
        this package ploneintranet.layout, but this package should NOT
        have any outside dependencies (to avoid dependency loops).
        '''
        view = self.get_view('apps.html')
        found = {app.getId() for app in view.apps()}
        configured = {
            'contacts',
            'messages',
            'calendar',
            'slide-bank',
            'image-bank',
            'case-manager',
            'app-market'
        }
        # We want all the configured app to be really there
        # there may be more e.g. bookmarks but out of test scope here
        self.assertSetEqual(configured.difference(found), set([]))

    def test_app_view(self):
        app_view = self.get_app_view('private-app')
        self.assertTrue(app_view().startswith('Sitemap'))

    def test_app_view_parameters(self):
        # This is a testing app with parameters that return the parameters
        app_view = self.get_app_view('app-with-parameters')
        self.assertDictEqual(app_view(), {u'foo': u'bar'})

    def test_app_redirect(self):
        app_view = self.get_app_view('redirect-app')
        self.assertEquals(app_view(), 'https://www.example.com')

    def get_app_view(self, app_id):
        ''' Return the app view for the given app_id
        '''
        app = self.portal.apps[app_id]
        return app.app_view(self.request)

    def get_app_tile(self, app_id):
        ''' Return the app tile view for the given app_id
        '''
        app = self.portal.apps[app_id]
        return api.content.get_view(
            'app-tile',
            app,
            self.request.clone()
        )

    def test_app_basetile_not_found(self):
        ''' Check the not_found property of the app tile adapter
        '''
        # The path is empty, so we have nothing to look for
        tile = self.get_app_tile('empty-app')
        self.assertTrue(tile.not_found)

        # if we set a path, we have to find it even if we are anonymous
        tile = self.get_app_tile('private-app')
        self.assertFalse(tile.not_found)

        tile = self.get_app_tile('private-app')
        with api.env.adopt_roles({'Anonymous'}):
            self.assertFalse(tile.not_found)

    def test_app_basetile_unauthorized(self):
        ''' Check the unauthorized property of the app tile adapter
        '''
        # If we have not set a path, we cannot traverse to anything,
        # so we cannot say if it is authorized or not
        tile = self.get_app_tile('empty-app')
        with self.assertRaises(AttributeError):
            tile.unauthorized

        # If we set an existing path, we will have a different response
        # according to our roles in context
        tile = self.get_app_tile('private-app')
        self.assertFalse(tile.unauthorized)

        tile = self.get_app_tile('private-app')
        with api.env.adopt_roles({'Anonymous'}):
            self.assertTrue(tile.unauthorized)

    def test_app_basetile_modal(self):
        ''' Check the modal property of the app tile adapter
        '''
        # With an empty path, when clicking on a tile,
        # we will get an alert in a modal
        tile = self.get_app_tile('empty-app')
        self.assertEqual(tile.modal, 'pat-modal')

        # Otherwise we will open the tile
        tile = self.get_app_tile('private-app')
        self.assertEqual(tile.modal, '')

        # Even if we are unauthorized
        tile = self.get_app_tile('private-app')
        with api.env.adopt_roles({'Anonymous'}):
            self.assertEqual(tile.modal, 'pat-modal')

    def test_app_basetile_url(self):
        ''' Check the url property of the app tile adapter
        '''
        # With an empty path, when clicking on a tile,
        # we will get an alert in a modal
        tile = self.get_app_tile('empty-app')
        self.assertEqual(
            tile.url,
            'http://nohost/plone/@@app-not-available.html#document-content',
        )

        # Otherwise we will open the tile
        tile = self.get_app_tile('private-app')
        self.assertEqual(
            tile.url,
            'http://nohost/plone/apps/private-app/robots.txt',
        )

        # Even if we are unauthorized
        tile = self.get_app_tile('private-app')
        with api.env.adopt_roles({'Anonymous'}):
            self.assertEqual(
                tile.url,
                'http://nohost/plone/@@app-unauthorized#document-content',
            )

    def test_app_basetile_disabled(self):
        ''' Check the disabled property of the app tile adapter
        '''
        # The tile should be disabled if path is not set (default)
        tile = self.get_app_tile('empty-app')
        self.assertEqual(tile.disabled, 'disabled')

        # The tile should be enabled because the path is allowed
        tile = self.get_app_tile('private-app')
        self.assertEqual(tile.disabled, '')

        # The tile should be disabled if the path is not allowed
        tile = self.get_app_tile('private-app')
        with api.env.adopt_roles({'Anonymous'}):
            self.assertEqual(tile.disabled, 'disabled')

    def test_app_basetile_condition(self):
        ''' Check the condition property of the app tile adapter
        '''
        tile = self.get_app_tile('conditional-app')
        self.assertFalse(tile.condition())

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

    def test_custom_dashboard(self):
        # We need a fake user to test persist tile ordering and display options
        with patch(
            'ploneintranet.api.userprofile.get_current',
            return_value=FakeCurrentUser(),
        ):
            user = pi_api.userprofile.get_current()
            view = self.get_view('dashboard.html', dashboard='custom')
            available_custom_tiles = list(view.available_custom_tiles())
            reversed_available_custom_tiles = available_custom_tiles[::-1]
            self.assertListEqual(
                view.custom_tiles().keys(),
                available_custom_tiles,
            )
            # The view is called
            self.assertIn('@@news.tile?portletspan=span-1', view())
            # and we do not write anything on the user
            self.assertRaises(AttributeError, getattr, user, 'custom_tiles')
            # We now test if we can modify the order of the tiles
            params = {
                'display-%s' % tile: 'span-2'
                for tile in available_custom_tiles
            }
            params['tiles_order'] = reversed_available_custom_tiles
            edit = self.get_view(
                'edit-dashboard',
                **params
            )
            edit.maybe_update_tiles()

            # Now the data persist on the user
            self.assertEqual(
                user.custom_tiles.keys(),
                reversed_available_custom_tiles,
            )
            self.assertEqual(
                user.custom_tiles['./@@news.tile?title=News']['display'],
                'span-2',
            )

    def test_in_app_dashboard(self):
        view = self.get_view('dashboard.html')
        self.assertFalse(in_app(view))

    def test_in_app_apptile(self):
        tile = self.get_app_tile('empty-app')
        self.assertTrue(in_app(tile))

    def test_in_app_dashboard_context(self):
        view = self.get_view('dashboard.html')
        self.assertFalse(in_app(view.context))

    def test_in_app_apptile_context(self):
        tile = self.get_app_tile('empty-app')
        self.assertTrue(in_app(tile.context))

    def test_login_splash(self):
        ''' Test that the ploneintranet.layout.login_splash actually changes
        the image on the login_form page
        '''
        DEFAULT_IMAGE_PATH = (
            u'++theme++ploneintranet.theme/'
            u'generated/media/logos/plone-intranet-square-dp.svg'
        )
        DEFAULT_IMAGE_TAG = (
            u'<img src="http://nohost/plone/%s" />' % DEFAULT_IMAGE_PATH
        )
        # There is a registry record that sets the path to an inmage
        self.assertEqual(
            api.portal.get_registry_record(
                'ploneintranet.layout.login_splash'
            ),
            DEFAULT_IMAGE_PATH
        )
        # If we render the login form we will find the relative img tag in it
        self.assertIn(
            DEFAULT_IMAGE_TAG,
            self.portal.login_form()
        )

        # We can change the registry and the login form will be updated
        api.portal.set_registry_record(
            'ploneintranet.layout.login_splash',
            u'cest-ne-pas-a-splash.svg'
        )
        self.assertIn(
            u'<img src="http://nohost/plone/cest-ne-pas-a-splash.svg" />',
            self.portal.login_form()
        )

        # If, for some reason, there is no record in the registry do not break
        # and return the dafault
        pr = api.portal.get_tool('portal_registry')
        pr.records.__delitem__('ploneintranet.layout.login_splash')
        self.assertIn(
            DEFAULT_IMAGE_TAG,
            self.portal.login_form()
        )

    def test_proto_slow(self):
        ''' the is_slow function
        '''
        with temporary_registry_record(
            'ploneintranet.layout.known_bad_ips',
            (u'666.666.666.666',)
        ):
            proto = self.get_view('proto')
            self.assertFalse(proto.is_slow())
            proto.request.__annotations__.pop('plone.memoize')
            proto.request.environ.update({'REMOTE_ADDR': u'666.666.666.666 1'})
            self.assertTrue(proto.is_slow())

    def test_splashpage(self):
        with patch(
            'ploneintranet.api.userprofile.get_current',
            return_value=FakeCurrentUser(),
        ):
            with temporary_registry_record(
                'ploneintranet.layout.splashpage_enabled',
                True,
            ):
                view = self.get_view('dashboard.html')
                self.assertEqual(view.splashpage_uid, u'splashpage-1')
                self.assertTrue(view.show_splashpage)
                # This emulates the user closing the splashpage
                view.request = self.request.clone()
                view.request.form['splashpage_uid'] = u'splashpage-1'
                view()
                self.assertFalse(view.show_splashpage)
                # Check if we can force the splashpage to appear again
                view.request = self.request.clone()
                view.request.form['splashpage_uid'] = u'force'
                view()
                self.assertTrue(view.show_splashpage)

    def test_toggle_lock(self):
        # The portal does not support TTW locking
        view = self.get_view('toggle-lock')
        self.assertEqual(view.lock_info, None)
        self.assertEqual(view.lock_operations, None)

        # A Document does support TTW locking
        obj = api.content.create(
            title="Example page",
            container=self.folder,
            type="Document"
        )
        view = self.get_view('toggle-lock', obj)
        self.assertEqual(view.lock_info, None)
        self.assertNotEqual(view.lock_operations, None)
        view.lock()
        # Purge the cache
        view.request.__annotations__.pop('plone.memoize')
        self.assertEqual(view.lock_info['creator'], 'test_user_1_')
        view.unlock()
        # Purge the cache
        view.request.__annotations__.pop('plone.memoize')
        self.assertEqual(view.lock_info, None)

    def test_on_screen_help(self):
        view = self.get_view('on-screen-help')
        # Test that we can create bubble links if the bubble is well known
        self.assertEqual(view.link_to(1), '')
        self.assertIn('Help', view.link_to('hamburger'))

        # Check if we have a default bubble with no or wrong parameters
        self.assertIn(view._fallback_bubble['title'], view())
        view = self.get_view('on-screen-help', q='1')
        self.assertIn(view._fallback_bubble['title'], view())
        view = self.get_view('on-screen-help', q='hamburger')
        self.assertIn(
            translate(view.bubbles['hamburger']['description']), view())

        # check that we can set up custom bubbles
        custom_bubbles_json = (
            u'{"foo-bar": {'
            u'    "title": "Foo", "description": "<p>Bar baz</p>"'
            u'}}'
        )
        self.assertNotIn('foo-bar', view.bubbles)
        with temporary_registry_record(
            'ploneintranet.layout.custom_bubbles',
            custom_bubbles_json,
        ):
            view = self.get_view('on-screen-help', q='foo-bar')
            self.assertIn('foo-bar', view.bubbles)
            self.assertIn('Bar baz', view())

        # We can disable the bubbles through the registry
        with temporary_registry_record(
            'ploneintranet.layout.bubbles_enabled',
            'Disabled',
        ):
            view = self.get_view('on-screen-help')
            self.assertDictEqual(view.bubbles, {})

        # We can force the bubbles through the registry
        with temporary_registry_record(
            'ploneintranet.layout.bubbles_enabled',
            'On',
        ):
            page = self.portal.test_rendering()
            self.assertIn(
                'osh-on',
                html.fromstring(page).find('.//body').attrib['class'],
            )
