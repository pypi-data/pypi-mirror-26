from functools import partial
from pkg_resources import resource_filename
from plone import api
from plone.app import testing
from plone.namedfile import NamedBlobFile
from ploneintranet.search.interfaces import ISearchResponse
from ploneintranet.search.interfaces import ISearchResult
from ploneintranet.search.interfaces import ISiteSearch
from ploneintranet.search.testing import login_session
from ploneintranet.search.testing import TEST_USER_1_NAME
from zope.interface.verify import verifyObject

import abc
import collections
import datetime
import transaction
import unittest


class ContentSetup(object):
    """Defines a comment set of content re-usable accross different  cases."""

    @abc.abstractmethod
    def _make_utility(self, *args, **kw):
        """Return the utility under test."""

    def _record_debug_info(self, query_response):
        """This is a hook that allows sub-classes to record query responses.

        Useful for debugging tests.
        """

    def _query(self, util, *args, **kw):
        response = util.query(*args, **kw)
        self._record_debug_info(response)
        return response

    def setUp(self):
        super(ContentSetup, self).setUp()
        container = self.layer['portal']
        self._setup_content(container)

    def _setup_content(self, container):
        create_doc = partial(self._create_content,
                             type='Document',
                             container=container,
                             safe_id=False)

        self.doc1 = create_doc(
            title=u'Test Doc 1',
            description=(u'This is a test document. '
                         u'Hopefully some stuff will be indexed.'),
            subject=(u'test', u'my-tag'),
        )
        self.doc1.modification_date = datetime.datetime(2001, 9, 11, 0, 10, 1)

        self.doc2 = create_doc(
            title=u'Test Doc 2',
            description=(u'This is another test document. '
                         u'Please let some stuff be indexed. '),
            subject=(u'test', u'my-other-tag'),
        )
        self.doc2.modification_date = datetime.datetime(2002, 9, 11, 0, 10, 1)

        self.doc3 = create_doc(
            title=u'Lucid Dreaming',
            description=(
                u'An interesting prose by Richard Feynman '
                u'which may leave the casual reader perplexed. '
                u'Nothing to do with the weather.')
        )
        self.doc3.modification_date = datetime.datetime(2002, 9, 11, 1, 10, 1)

        self.doc4 = create_doc(
            title=u'Weather in Wales',
            description=u'Its raining cats and dogs, usually.',
            subject=(u'trivia', u'boredom', u'british-hangups')
        )
        self.doc4.modification_date = datetime.datetime(2002, 9, 11, 1, 10, 1)

        self.doc5 = create_doc(
            title=u'Sorted and indexed.',
            description=u'Not relevant',
            subject=(u'solr', u'boost', u'values')
        )
        self.doc5.modification_date = datetime.datetime(1999, 01, 11, 2, 3, 8)

        self.doc6 = create_doc(
            title=u'Another relevant title',
            description=u'Is Test Doc 2 Sorted and indexed?',
            subject=(u'abra', u'cad', u'abra')
        )
        self.doc6.modification_date = datetime.datetime(1994, 04, 05, 2, 3, 4)

        # Trigger collective.indexing
        transaction.commit()


class SearchTestsBase(ContentSetup):
    """Defines the base test case for the search utility.

    Each implementor of ISiteSite should implement at least one
    sub-test case.

    :seealso: The search utility API is described by
              ploneintranet.search.interfaces.ISiteSearch
    """

    def _check_type_iterable(self, response):
        self.assertIsInstance(response, collections.Iterable)
        result = next(iter(response), None)
        self.assertIsNotNone(result)

    def checkFacets(self, response, field, expected):
        ''' Given a search response check that the
        facets are generated as expected
        '''
        observed = sorted(
            response.facets[field],
            key=lambda x: (x['count'], x['name'])
        )
        self.assertListEqual(observed, expected)

    def test_response_iterable(self):
        util = self._make_utility()
        response = util.query('hopefully')
        self._check_type_iterable(response)

    def test_response_boolean_state(self):
        util = self._make_utility()
        response = util.query('hopefully')
        self.assertTrue(response)
        response = util.query('unobtainium')
        self.assertFalse(response)

    def test_response_length(self):
        util = self._make_utility()
        response = util.query('hopefully')
        self.assertEqual(len(response), 1)
        response = util.query('unobtainium')
        self.assertEqual(len(response), 0)

    def test_results_iterable(self):
        util = self._make_utility()
        response = util.query('hopefully')
        self._check_type_iterable(response.results)

    def test_interface_compliance(self):
        util = self._make_utility()
        verifyObject(ISiteSearch, util)
        search_response = util.query(
            'Test',
        )
        verifyObject(ISearchResponse, search_response)
        for search_result in search_response:
            verifyObject(ISearchResult, search_result)

    def test_results_to_object(self):
        ''' All the results have a getObject() method that returns
        a Plone object
        '''
        util = self._make_utility()
        verifyObject(ISiteSearch, util)
        search_response = util.query(
            'Test',
        )
        [x.getObject() for x in search_response]

    def test_results_review_state(self):
        ''' All the results have a review_state property
        method that returns a string (it may be empty)
        '''
        util = self._make_utility()
        verifyObject(ISiteSearch, util)
        search_response = util.query(
            'Test',
        )
        for x in search_response:
            self.assertIsInstance(x.review_state, basestring)

    def test_query_phrase_only(self):
        util = self._make_utility()
        response = self._query(util, 'hopefully')
        self.assertEqual(response.total_results, 1)
        result = next(iter(response), None)
        self.assertIsNotNone(result)
        self.assertEqual(result.title, self.doc1.Title())
        self.assertEqual(result.url, self.doc1.absolute_url())
        self.checkFacets(
            response,
            'friendly_type_name',
            [{'name': u'Page', 'count': 1}]
        )
        self.checkFacets(
            response,
            'tags',
            [{'name': u'my-tag', 'count': 1}, {'name': u'test', 'count': 1}]
        )

    def test_query_partial_match(self):
        util = self._make_utility()
        response = self._query(util, 'hope')
        self.assertEqual(response.total_results, 1)
        response = self._query(util, 'doc')
        self.assertEqual(response.total_results, 3)

    def test_query_with_empty_filters(self):
        util = self._make_utility()
        response = util.query(u'stuff', filters={})
        self.checkFacets(
            response,
            'tags',
            [
                {'count': 1, 'name': u'my-other-tag'},
                {'count': 1, 'name': u'my-tag'},
                {'count': 2, 'name': u'test'},
            ]
        )
        self.checkFacets(
            response,
            'friendly_type_name',
            [{'count': 2, 'name': 'Page'}]
        )

    def test_query_with_empty_phrase(self):
        util = self._make_utility()
        # Need either phrase or filter
        with self.assertRaises(api.exc.MissingParameterError):
            util.query()

        response = util.query(filters={
            'portal_type': 'Document',
        })
        self.assertEqual(len(response.facets['tags']), 11)
        self.assertEqual(response.total_results, 6)

    def test_path_query_with_empty_phrase(self):
        portal = self.layer['portal']
        folder1 = self._create_content(
            type='Folder',
            container=portal,
            title=u'Test Folder 1',
            description=(u'This is a test folder. '),
            safe_id=False
        )
        self._setup_content(folder1)

        util = self._make_utility()
        response = util.query(
            filters=dict(path='/plone/test-folder-1',
                         portal_type='Document'))
        self.assertEqual(response.total_results, 6)

        response = util.query(
            filters=dict(path='/plone',
                         portal_type='Document'))
        self.assertEqual(response.total_results, 12)

    def test_query_filter_by_friendly_type(self):
        img_path = resource_filename(
            'ploneintranet', 'userprofile/tests/test_avatar.jpg')
        with open(img_path, 'rb') as fp:
            img_data = fp.read()
        self.image1 = self._create_content(
            type='Image',
            container=self.layer['portal'],
            title=u'A Test image',
            description=u'Info about this image',
            file=NamedBlobFile(
                data=img_data,
                contentType='image/jpeg',
                filename=fp.name.decode('utf-8'),
            )
        )
        transaction.commit()

        util = self._make_utility()
        response = util.query(
            u'Test',
            filters={'friendly_type_name': ['Image']}
        )
        self.assertEqual(response.total_results, 1)
        result = next(iter(response))
        self.assertEqual(result.title, self.image1.title)

        response = util.query(
            u'Test',
            filters={'friendly_type_name': ['Page', ]}
        )
        self.assertEqual(response.total_results, 3)
        self.assertEqual(
            set([x.friendly_type_name for x in response]),
            {'Page'},
        )

        response = util.query(
            u'Test',
            filters={'friendly_type_name': ['Image', 'Page', ]}
        )
        self.assertEqual(response.total_results, 4)
        self.assertEqual(
            set([x.friendly_type_name for x in response]),
            {'Page', 'Image', },
        )

    def test_query_filter_by_creator(self):
        self._create_content(
            type='Document',
            id='test_creator',
            title="A different title",
            container=self.layer['portal'],
        )
        obj = self.layer['portal']['test_creator']
        obj.setCreators(['my_alter_ego'])
        obj.reindexObject()
        transaction.commit()
        util = self._make_utility()
        self.assertListEqual(
            [u'A different title'],
            [
                x.getObject().title
                for x in util.query('', filters={'Creator': 'my_alter_ego'})
            ],
        )

    def test_query_filter_by_UID(self):
        util = self._make_utility()
        filters = {'UID': self.layer['portal']['lucid-dreaming'].UID()}
        self.assertListEqual(
            [u'Lucid Dreaming'],
            [
                x.getObject().title
                for x in util.query('', filters=filters)
            ]
        )

    def test_query_facets_invalid(self):
        util = self._make_utility()
        self.assertRaises(LookupError,
                          util.query,
                          u'stuff',
                          filters=dict(ploneineternet=u'mytag'))

    def test_query_tags_facet(self):
        util = self._make_utility()
        response = self._query(util, 'stuff')
        self.assertEqual(response.total_results, 2)
        self.checkFacets(
            response,
            'tags',
            [
                {'name': u'my-other-tag', 'count': 1},
                {'name': u'my-tag', 'count': 1},
                {'name': u'test', 'count': 2},
            ],
        )
        # Limit search by a tag from one of the docs//
        response = self._query(util, 'stuff',
                               filters={'tags': [u'my-other-tag']})
        self.assertEqual(response.total_results, 1)
        self.checkFacets(
            response,
            'tags',
            [
                {'name': u'my-other-tag', 'count': 1},
                {'name': u'test', 'count': 1},
            ],
        )

    def test_query_friendly_type_facet(self):
        util = self._make_utility()
        response = self._query(util, 'hopefully')
        self.assertEqual(response.total_results, 1)
        self.checkFacets(
            response,
            'friendly_type_name',
            [{'count': 1, 'name': u'Page'}],
        )
        response = self._query(util, 'stuff')
        self.assertEqual(response.total_results, 2)
        self.checkFacets(
            response,
            'friendly_type_name',
            [{'count': 2, 'name': u'Page'}],
        )

    def test_batching_returns_all_tags(self):
        ''' Check that we are collecting the right tags
        and that they are presented correctly for faceting
        '''
        util = self._make_utility()
        response = self._query(util, u'stuff', step=1)
        self.assertEqual(response.total_results, 2)
        self.assertEqual(len(list(response)), 1)
        self.checkFacets(
            response,
            'tags',
            [
                {'count': 1, 'name': u'my-other-tag'},
                {'count': 1, 'name': u'my-tag'},
                {'count': 2, 'name': u'test'},
            ],
        )

    def test_delete_content(self):
        util = self._make_utility()

        def query_check_total_results(expected_count):
            response = self._query(util, u'Another')
            self.assertEqual(response.total_results, expected_count)

        query_check_total_results(2)
        with api.env.adopt_roles(roles=['Manager']):
            self._delete_content(self.doc2)
            self._delete_content(self.doc6)
            transaction.commit()

        assert self.doc2.getId() not in self.layer['portal'].keys()
        query_check_total_results(0)

    def _check_spellcheck_response(self, query_term, expect_suggestion):
        util = self._make_utility()
        response = self._query(util, query_term)
        self.assertEqual(response.spell_corrected_search, expect_suggestion)

    def test_spell_corrected_search(self):
        self._check_spellcheck_response('', None)
        self._check_spellcheck_response(u'', None)
        self._check_spellcheck_response(u'*:*', None)

        # Test a correctly spelt terms have no spell_corrected_search
        self._check_spellcheck_response(u'Lucid', None)
        self._check_spellcheck_response(u'leave', None)
        self._check_spellcheck_response(u'Test', None)

        # These corrected spellings should work (depending on configuration.
        self._check_spellcheck_response(u'anathar', u'another')
        self._check_spellcheck_response(u'Rcichad', u'richard')
        self._check_spellcheck_response(u'Anather', u'another')
        self._check_spellcheck_response(u'Perplaxed', u'perplexed')
        self._check_spellcheck_response(u'Peplexed', u'perplexed')
        self._check_spellcheck_response(u"reining cots n' dags",
                                        u"raining cats n' dogs")

    def test_date_range_query(self):
        util = self._make_utility()
        query = util.query
        phrase = u'document'
        (min_dt, max_dt) = (datetime.datetime.min, datetime.datetime.max)

        # Start date in the future yields no results
        response = query(phrase, start_date=max_dt)
        self.assertEqual(response.total_results, 0)

        # Start in the future, no results
        response = query(phrase, start_date=max_dt)
        self.assertEqual(response.total_results, 0)

        # Same start and end date in the future yields no results
        response = query(phrase, start_date=max_dt, end_date=max_dt)
        self.assertEqual(response.total_results, 0)

        # Same start and end date in the past yields no results
        response = query(phrase, start_date=min_dt, end_date=min_dt)
        self.assertEqual(response.total_results, 0)

        response = query(u'Dreaming', start_date=min_dt, end_date=max_dt)
        self.assertEqual(response.total_results, 1)
        result = next(iter(response))
        self.assertEqual(result.title, u'Lucid Dreaming')

        response = query(phrase, start_date=min_dt, end_date=max_dt)
        self.assertEqual(response.total_results, 2)

        result_titles = list(result.title for result in response)
        expected_titles = [doc.Title() for doc in (self.doc2, self.doc1)]
        self.assertEqual(set(result_titles),
                         set(expected_titles))

    def test_relevancy(self):
        util = self._make_utility()
        query = util.query
        response = query(u'weather')
        expected_order = [self.doc4.Title(), self.doc3.Title()]
        actual_order = [result.title for result in response]
        self.assertEqual(actual_order, expected_order)

        response = query(u'Test Doc 2')
        expected_order = [self.doc5.Title(), self.doc6.Title()]
        actual_order = [result.title for result in response]

        response = query(u'Relevant')
        expected_order = [self.doc5.Title(), self.doc6.Title()]
        actual_order = [result.title for result in response]

    def test_search_result_sorting(self):
        util = self._make_utility()
        query = util.query
        for field in (
            'modified',
            'sortable_title',
        ):
            ascending = query('indexed', sort=field)
            ascending_titles = [result.title for result in ascending]
            descending = query('indexed', sort='-' + field)
            descending_titles = [result.title for result in descending]
            descending_titles.reverse()
            self.assertEqual(
                ascending_titles,
                descending_titles,
                msg='Error while sorting by {field}'.format(field=field)
            )

    def test_file_content_matches(self):
        path = resource_filename('ploneintranet.search.tests',
                                 'fixtures/lorum-ipsum.pdf')
        with open(path, 'rb') as fp:
            data = fp.read()
        # Indexing SearchableText is now done async, so trigger it
        self.layer['portal'].REQUEST.set('attributes', 'SearchableText')
        self._create_content(
            type='File',
            container=self.layer['portal'],
            title=u'Test File 1',
            description=(u'This is a test file. '),
            safe_id=False,
            file=NamedBlobFile(
                data=data,
                contentType='application/pdf',
                filename=fp.name.decode('utf-8'))
        )
        transaction.commit()
        util = self._make_utility()
        query = util.query
        response = query(u'Maecenas urna elit')
        results = list(response)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, u'Test File 1')


class PermissionTestsBase(ContentSetup):
    """Permissions tests.

    These tests should ensure combinations of users and roles can
    only see the content they are permitted by the permissions system.
    """

    def setUp(self):
        super(PermissionTestsBase, self).setUp()
        testing.login(self.layer['portal'], testing.TEST_USER_NAME)

    def test_documents_owned_by_other_not_visible_same_role(self):
        with login_session(TEST_USER_1_NAME):
            util = self._make_utility()
            response = self._query(util, 'Test Doc')
            self.assertEqual(response.total_results, 0)
            response = self._query(util, 'Test Doc', secure=False)
            self.assertEqual(response.total_results, 3)

    def test_review_state_changes(self):
        """Does the search respect view permissions?"""
        api.content.transition(obj=self.doc2, transition='publish')
        self.doc2.reindexObject()
        transaction.commit()

        testing.logout()
        util = self._make_utility()

        # Check anonymous access
        response = self._query(util, 'hopefully')
        self.assertEqual(response.total_results, 0)
        response = self._query(util, 'another')
        self.assertEqual(response.total_results, 1)

        with login_session(TEST_USER_1_NAME):
            response = self._query(util, 'hopefully')
            self.assertEqual(response.total_results, 0)
            response = self._query(util, 'another')
            self.assertEqual(response.total_results, 1)

            with api.env.adopt_roles(['Manager']):
                api.content.transition(obj=self.doc1, transition='publish')
                self.doc1.reindexObject()
                transaction.commit()

            response = self._query(util, 'hopefully')
            self.assertEqual(response.total_results, 1)

    def test_group_changes(self):
        """Does the search respect group permissions?"""
        api.group.create(groupname='TestUsers')
        api.group.grant_roles(
            groupname='TestUsers',
            obj=self.doc1,
            roles=['Owner', ],
        )
        self.doc1.reindexObject()
        transaction.commit()

        testing.logout()

        util = self._make_utility()

        with login_session(TEST_USER_1_NAME):
            response = self._query(util, 'hopefully')
            self.assertEqual(response.total_results, 0)

        # Add user to the group - they should now doc1
        # the item in search results
        api.group.add_user(
            groupname='TestUsers',
            username=TEST_USER_1_NAME)

        with login_session(TEST_USER_1_NAME):
            response = self._query(util, 'hopefully')
            self.assertEqual(response.total_results, 1)


class TestNothing(unittest.TestCase):
    """
    The above tests are run from:
    ../tests/test_zcatalog
    ../solr/tests/test_solr_search

    To make this base module easily discoverable for developers it has been
    renamed to test_base. Unittest then requires there to be a test.
    """

    def test_nothing(self):
        """No-op test to satisfy unittest suite discovery"""
        pass
