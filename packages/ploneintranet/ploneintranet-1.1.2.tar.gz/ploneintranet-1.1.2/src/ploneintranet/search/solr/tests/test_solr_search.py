import unittest

import transaction
from zope.component import getUtility
from zope.interface.verify import verifyObject

from ploneintranet.search.tests import test_base
from ploneintranet.search.interfaces import ISearchResponse
from ploneintranet.search.solr import testing


class TestConnectionConfig(unittest.TestCase):
    """Unittests for ZCML directive."""

    def _make_utility(self, *args, **kw):
        from ploneintranet.search.solr.solr_search import ConnectionConfig
        return ConnectionConfig(*args, **kw)

    def test_interface_compliance(self):
        from ploneintranet.search.solr.interfaces import IConnectionConfig
        obj = self._make_utility('localhost', '1111', '/solr', 'core1')
        verifyObject(IConnectionConfig, obj)

    def test_url(self):
        obj = self._make_utility('localhost', '1111', '/solr', 'core1')
        self.assertEqual(obj.url, 'http://localhost:1111/solr/core1')


class TestSolrSearch(test_base.SearchTestsBase,
                     testing.FunctionalTestCase):
    """Integration tests for SiteSearch utility.

    The actual tests are defined in test_base.
    """

    def _make_utility(self, *args, **kw):
        from ploneintranet.search.solr.solr_search import SiteSearch
        return SiteSearch()

    def _record_debug_info(self, response):
        self._last_response = response.context.original_json

    def setUp(self):
        super(TestSolrSearch, self).setUp()
        from ploneintranet.search.solr.interfaces import IMaintenance
        getUtility(IMaintenance).warmup_spellchcker()

    def test_query_with_complex_filters(self):
        util = self._make_utility()
        Q = util.Q
        filters = Q(Title=u'Test Doc 1') | Q(Title=u'Test Doc 2')
        filters &= Q(portal_type='Document')
        response = util.query('Test Doc', filters=filters, debug=True)
        self.assertEqual(response.total_results, 2)

    def test_raw_query_with_complex_filters(self):
        util = self._make_utility()
        query = util.connection.query('Test Doc')
        query = query.filter(query.Q(Title=u'Test Doc 1') |
                             query.Q(Title=u'Test Doc 2') &
                             query.Q(portal_type='Document'))
        response = ISearchResponse(util.execute(query))
        self.assertEqual(response.total_results, 2)

    def test_partial_updates(self):
        """Partial updates are not supported."""
        self.doc1.title = u'Star Wars Part 7'
        self.doc1.reindexObject(idxs=['Title'])
        transaction.commit()

        util = self._make_utility()

        response = util.query(u'Wars')
        self.assertEqual(response.total_results, 1)

        # Change a index without changing object.
        self.doc1.reindexObject(idxs=['review_state'])
        transaction.commit()
        response = util.query(u'Wars')
        self.assertEqual(response.total_results, 1)

        self.doc1.description = u'Luke Skywalker'
        self.doc1.reindexObject(idxs=['Description', 'NotASolrIndex'])
        transaction.commit()

        response = util.query(u'Skywalker')
        self.assertEqual(response.total_results, 1)

        self.doc1.title = u'JaJa Binks'
        self.doc1.reindexObject(idxs=['NotASolrIndex'])
        transaction.commit()

        response = util.query(u'JaJa')
        self.assertEqual(response.total_results, 0)


class TestSolrPermissions(test_base.PermissionTestsBase,
                          testing.FunctionalTestCase):
    """Integration tests for SiteSearch permissions.

    The actual tests are defined in test_base.
    """

    def _make_utility(self, *args, **kw):
        from ploneintranet.search.solr.solr_search import SiteSearch
        return SiteSearch()

    def _record_debug_info(self, response):
        self._last_response = response.context.original_json
