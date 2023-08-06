from .. import base
from ..interfaces import ISiteSearch
from .interfaces import IConnection
from .interfaces import IConnectionConfig
from .interfaces import IMaintenance
from .interfaces import IQuery
from AccessControl.SecurityManagement import getSecurityManager
from Acquisition import aq_base
from plone import api
from Products.CMFPlone.utils import safe_unicode
from scorched.exc import SolrError
from scorched.search import LuceneQuery
from zope.component import getUtility
from zope.interface import implementer

import collections
import logging
import scorched.search
import urlparse


logger = logging.getLogger(__name__)


def prepare_data(data):
    """Prepare data (from Plone) for use with SOLR.

    Mutates the supplied mapping in-place.

    :param data: The data mapping.
    :type data: collections.MutableMapping
    """
    arau = data.get('allowedRolesAndUsers')
    if arau is not None:
        arau = list(v.replace(':', '$') for v in arau)
        data['allowedRolesAndUsers'] = arau


class SpellcheckOptions(scorched.search.Options):
    """Alternate SpellcheckOptions implementation.

    This implements sub-options for the Solr spellchecker.
    The scorched implementation just allows turning it on.

    This may be pushed back upstream if deemed successfull.
    """
    option_name = 'spellcheck'
    opts = {
        'accuracy': float,
        'collate': bool,
        'maxCollations': int,
        'onlyMorePopular': bool,
        'extendedResults': bool,
        'q': str,
        'reload': bool,
        'build': bool,
    }

    def __init__(self, original=None):
        super(SpellcheckOptions, self).__init__()
        fields = collections.defaultdict(dict)
        self.fields = getattr(original, 'fields', fields)

    def field_names_in_opts(self, opts, fields):
        if fields:
            opts[self.option_name] = True


class Search(scorched.search.SolrSearch):
    function_query_boost = base.RegistryProperty('function_query_boost',
                                                 prefix=__package__)

    def _init_common_modules(self):
        super(Search, self)._init_common_modules()
        self.spellchecker = SpellcheckOptions()

    def spellcheck(self, **kw):
        newself = self.clone()
        spellchecker = newself.spellchecker
        query = kw.get('q', '')
        if isinstance(query, unicode):
            kw['q'] = query.encode('utf-8')
        spellchecker.update(**kw)
        return newself

    def execute(self, constructor=None):
        """ Override the execute method of scorched so that
        we can prepend our boosting. Only boost when doing fulltext search.
        """
        options = self.options()
        boost_query = self.function_query_boost
        if boost_query and 'SearchableText' in options['q']:
            boost = u"{{!boost b={boost_query}}}".format(
                boost_query=boost_query
            )
            options['q'] = boost + options['q']
        ret = self.interface.search(**options)
        if constructor:
            ret = self.constructor(ret, constructor)
        return ret

    def __str__(self):
        return "{}: {} && {}".format(
            repr(self), str(self.query_obj), str(self.filter_obj))


@implementer(IConnectionConfig)
class ConnectionConfig(object):

    _url = None

    def __init__(self, host, port, basepath, core):
        self.host = host
        self.port = port
        self.basepath = basepath.lstrip('/')
        self.core = core

    @classmethod
    def from_url(cls, url):
        pr = urlparse.urlparse(url)
        (host, port) = pr.netloc.split(':', 1)
        (basepath, core) = filter(bool, pr.path.split('/'))
        cfg = cls(host, port, '/' + basepath, core)
        return cfg

    @property
    def url(self):
        if self._url is None:
            format_url = 'http://{host}:{port}/{basepath}/{core}'.format
            self._url = format_url(**vars(self))
        return self._url


class Connection(object):
    """A descriptor representing a Solr connection object."""

    def __init__(self):
        self._conn = None

    def __get__(self, obj, objtype):
        if self._conn is None:
            self._conn = IConnection(getUtility(IConnectionConfig))
        return self._conn

    def __del__(self):
        del self._conn


@implementer(IMaintenance)
class Maintenance(object):

    connection = Connection()

    @classmethod
    def _find_objects_to_index(cls, origin):
        """ generator to recursively find and yield all zope objects below
            the given start point """
        traverse = origin.unrestrictedTraverse
        basepath = '/'.join(origin.getPhysicalPath())
        cut = len(base) + 1
        paths = [basepath]
        for (idx, path) in enumerate(paths):
            obj = traverse(path)
            yield (path[cut:], obj)
            if hasattr(aq_base(obj), 'objectIds'):
                for id_ in obj.objectIds():
                    paths.insert(idx + 1, path + '/' + id_)

    def warmup_spellchcker(self):
        """Build the Solr spellchecker."""
        search = IQuery(self.connection)
        response = search.query().spellcheck(build=True).execute()
        return response

    def purge(self):
        conn = self.connection
        response = conn.delete_all()
        conn.commit(waitSearcher=True, expungeDeletes=True)
        conn.optimize(waitSearcher=True)
        return response


@implementer(ISiteSearch)
class SiteSearch(base.SiteSearch):
    """A Site search utility using SOLR as the engine.

    This implementation uses the `scorched` bindings to
    generate the lucene query used to deliver site search results.

    This logic combining the query and filter parameters to the query.

    The resulting logical query is similar to the following:

        ((Title == VALUE OR Description == VALUE OR SearchableText == VALUE)
        AND (FILTER1 == VALUE OR FILTER)
        AND (allowedRolesAndUsers=... OR allowedRolesAndUsers=..) ...

    """
    connection = Connection()
    phrase_field_boosts = base.RegistryProperty('phrase_field_boosts',
                                                prefix=__package__)
    field_limit = base.RegistryProperty('field_limit',
                                        prefix=__package__)

    def _create_query_object(self, phrase):
        """Create the query object given the search `phrase`.

        :param phrase: The phrase to query SOLR with.
        :type phrase: sr
        :returns: A query object.
        :rtype query: ploneintranet.search.solr.search.Search
        """
        phrase = safe_unicode(phrase)
        Q = self.Q
        phrase_query = Q()
        if phrase:
            # boosting incompatible with wildcard phrase
            boosts = self.phrase_field_boosts
            for phrase_field in self.phrase_fields:
                phrase_q = Q(**{phrase_field: phrase})
                boost = boosts.get(phrase_field)
                if boost is not None:
                    phrase_q **= boost
                phrase_query |= phrase_q
        return IQuery(self.connection).query(Q(phrase_query))

    def _apply_filters(self, query, filters):
        if isinstance(filters, LuceneQuery):
            return query.filter(filters)
        Q = self.Q
        if 'path' not in filters:
            filters.update(
                path='/'.join(api.portal.get().getPhysicalPath()),
            )
        for key, value in filters.items():
            if key == 'path':
                key = 'path_parents'
            if isinstance(value, list):
                # create an OR subquery for this filter
                subquery = Q()
                for item in value:
                    # item can be a string, force unicode
                    subquery |= Q(**{key: safe_unicode(item)})
                query = query.filter(subquery)
            else:
                query = query.filter(Q(**{key: value}))
        return query

    def _apply_facets(self, query):
        return query.facet_by(fields=self.facet_fields, limit=-1)

    def _apply_date_range(self, query, start_date, end_date):
        filter_query = query.filter
        if start_date and end_date:
            query = filter_query(modified__range=(start_date, end_date))
        elif end_date is not None:
            query = filter_query(modified__lt=end_date)
        else:
            query = filter_query(modified__gt=start_date)
        return query

    def _apply_spellchecking(self, query, phrase):
        query = query.highlight('Description')
        return query.spellcheck(q=phrase, collate=True, maxCollations=1)

    def _paginate(self, query, start, step):
        return query.paginate(start=start, rows=step)

    def _apply_debug(self, query):
        return query.debug()

    def _apply_security(self, query):
        Q = self.Q
        # _listAllowedRolesAndUsers method requires
        # the actual user object so we can't use plone.api here
        user = getSecurityManager().getUser()
        catalog = api.portal.get_tool(name='portal_catalog')
        arau = catalog._listAllowedRolesAndUsers(user)
        data = dict(allowedRolesAndUsers=arau)
        prepare_data(data)
        # avoid recursion exception by constructing a flat query
        arau_q = Q().__or__(Q())  # construct toplevel OR
        valid_opts = data['allowedRolesAndUsers']
        sub_qs = [Q(allowedRolesAndUsers=v) for v in valid_opts]
        if len(sub_qs) > 900:
            logger.info(
                "Many arau clauses: {}. Please configure Solr "
                "maxBooleanClauses high enough to avoid SolrError.".format(
                    len(sub_qs)))
        # add subqueries directly on toplevel, refs #695
        arau_q.add(sub_qs, {})
        # you can check validity with: str(arau_q)
        return query.filter(arau_q)

    @classmethod
    def _collect_query_params(cls, iface, bucket):
        """Collect original query paramters for debugging purposes.

        :param iface: The Zope interface used for the query.
        :type iface: zope.interface.Interface
        :param bucket: The container which field names will be inserted.
        :type bucket: collections.MutableMapping
        """
        params = collections.OrderedDict()
        query_spec = iface['query']
        for name in query_spec.required:
            params[name] = bucket[name]
        for name in query_spec.optional:
            if name in bucket:
                params[name] = bucket[name]
        return params

    def execute(self, query, secure=True, **kw):
        if secure:
            query = self._apply_security(query)
        sort = kw.get('sort')
        if sort:
            # valid sort values:
            #  - 'field': sort results ascending by field
            #  - '-field': sort results descending by field
            if isinstance(sort, basestring):
                sort = [sort]
            for field in sort:
                query = query.sort_by(field)
        if self.field_limit:
            query = query.field_limit(self.field_limit)

        try:
            response = query.execute()
        except SolrError, exc:
            raise SolrError("{} on query: {}".format(
                            exc.message, query.debug().options()))
        if kw.get('debug'):
            # you will have to reformat path_parents for solr console queries
            # path_parents:\\/Plone\\/foo -> path_parents:"/Plone/foo"
            logger.info(query.debug().options())
        query_params = self._collect_query_params(ISiteSearch, dict(kw))
        response.query_params = query_params
        return response

    @property
    def Q(self):
        """Forward reference to the :py:class:`LuceneQuery` factory."""
        return self.connection.Q
