# -*- coding: utf-8 -*-
""" This code heavily relies on the maintenance code of collective.solr and
    strives to provide a similar service """
from Acquisition import aq_base
from BTrees.IIBTree import IITreeSet
from collective.indexing.indexer import getOwnIndexMethod
from datetime import datetime
from logging import getLogger
from plone.memoize import ram
from plone.protect.interfaces import IDisableCSRFProtection
from ploneintranet.search.solr.indexers import ContentAdder
from ploneintranet.search.solr.indexers import ContentIndexer
from ploneintranet.search.solr.interfaces import ICheckIndexable
from ploneintranet.search.solr.interfaces import IConnection
from ploneintranet.search.solr.interfaces import IConnectionConfig
from ploneintranet.search.solr.interfaces import ISolrMaintenanceView
from Products.Archetypes.CatalogMultiplex import CatalogMultiplex
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from time import clock
from time import strftime
from time import time
from zope.component import adapts
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface


logger = getLogger('ploneintranet.search.maintenance')
MAX_ROWS = 1000000000


class BaseIndexable(object):

    implements(ICheckIndexable)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return isinstance(self.context, CatalogMultiplex) or \
            isinstance(self.context, CMFCatalogAware)


def findObjects(origin):
    """ generator to recursively find and yield all zope objects below
        the given start point """
    traverse = origin.unrestrictedTraverse
    base = '/'.join(origin.getPhysicalPath())
    cut = len(base) + 1
    paths = [base]
    for idx, path in enumerate(paths):
        obj = traverse(path)
        yield path[cut:], obj
        if hasattr(aq_base(obj), 'objectIds'):
            for id in obj.objectIds():
                paths.insert(idx + 1, path + '/' + id)


def timer(func=time):
    """ set up a generator returning the elapsed time since the last call """
    def gen(last=func()):
        while True:
            elapsed = func() - last
            last = func()
            yield '%.3fs' % elapsed
    return gen()


def checkpointIterator(function, interval=100):
    """ the iterator will call the given function for every nth invocation """
    counter = 0
    while True:
        counter += 1
        if counter % interval == 0:
            try:
                function()
            except:
                logger.exception('Error executing %r' % function)
        yield None


def notimeout(func):
    """ decorator to prevent long-running solr tasks from timing out """
    def wrapper(*args, **kw):
        """ wrapper with random docstring so ttw access still works """
        # manager = queryUtility(ISolrConnectionManager)
        # manager.setTimeout(None, lock=True)
        try:
            return func(*args, **kw)
        finally:
            pass
            # XXX Implement the timeout handling
            # manager.setTimeout(None, lock=False)
    return wrapper


class SolrMaintenanceView(BrowserView):
    """ helper view for indexing all portal content in Solr """
    implements(ISolrMaintenanceView)

    def mklog(self, use_std_log=False, write_to_response=True):
        """ helper to prepend a time stamp to the output """
        write = self.request.RESPONSE.write

        def log(msg, timestamp=True):
            if timestamp:
                msg = strftime('%Y/%m/%d-%H:%M:%S ') + msg
            if write_to_response:
                write(msg)
            if use_std_log:
                logger.info(msg)
        return log

    def disable_csrf(self):
        ''' Disable CSRF protection because we are also wriuting on the catalog
        '''
        alsoProvides(self.request, IDisableCSRFProtection)

    def optimize(self):
        """ optimize solr indexes """
        # This is probably too simple, we must pass in a higher timeout
        # Scorched can do that, we can't pass it through yet, though
        conn = IConnection(getUtility(IConnectionConfig))
        conn.optimize()
        return 'solr indexes optimized.'

    def clear(self):
        """ clear all data from solr, i.e. delete all indexed objects """
        conn = IConnection(getUtility(IConnectionConfig))
        conn.delete_all()
        return 'solr index cleared.'

    def reindex(self, batch=1000, skip=0, limit=0, ignore_portal_types=None,
                only_portal_types=None, idxs=[], no_log=False,
                index_fulltext=False):
        """ find all contentish objects (meaning all objects derived from one
            of the catalog mixin classes) and (re)indexes them """

        self.disable_csrf()

        if ignore_portal_types and only_portal_types:
            raise ValueError("It is not possible to combine "
                             "ignore_portal_types with only_portal_types")

        conn = IConnection(getUtility(IConnectionConfig))

        if not index_fulltext:
            logger.info("NOT indexing SearchableText. "
                        "Pass index_fulltext=True to do otherwise.")
            attributes = [x['name'] for x in conn.schema['fields']]
            attributes.remove(u'SearchableText')
            idxs = attributes
        else:
            logger.warn("Indexing SearchableText. This may take a while.")

        atomic = idxs != []
        zodb_conn = self.context._p_jar
        CI = ContentIndexer()

        log = self.mklog(write_to_response=not no_log)
        log('reindexing solr catalog...\n')
        if skip:
            log('skipping indexing of %d object(s)...\n' % skip)
        if limit:
            log('limiting indexing to %d object(s)...\n' % limit)
        real = timer()          # real time
        lap = timer()           # real lap time (for intermediate commits)
        cpu = timer(clock)      # cpu time
        processed = 0

        uniqueKey = conn.schema['uniqueKey']
        updates = {}            # list to hold data to be updated

        flush = notimeout(lambda: conn.commit(softCommit=True))

        def checkPoint():
            for data in updates.values():
                adder = data.pop('_solr_adder', set([]))
                adder.add(data)
            updates.clear()
            msg = 'intermediate commit (%d items processed, ' \
                  'last batch in %s)...\n' % (processed, lap.next())
            log(msg)
            logger.info(msg)
            flush()
            zodb_conn.cacheGC()
        cpi = checkpointIterator(checkPoint, batch)
        count = 0

        if atomic:
            log('indexing only {0} \n'.format(idxs))

        for path, obj in findObjects(self.context):
            try:
                if ICheckIndexable(obj)():

                    if getOwnIndexMethod(obj, 'indexObject') is not None:
                        log(
                            'skipping indexing of %r via private method.\n',
                            obj
                        )
                        continue

                    count += 1
                    if count <= skip:
                        continue

                    if ignore_portal_types:
                        if obj.portal_type in ignore_portal_types:
                            continue

                    if only_portal_types:
                        if obj.portal_type not in only_portal_types:
                            continue

                    attributes = None
                    if atomic:
                        attributes = idxs

                    # For atomic updates to work the uniqueKey must be present
                    # in *every* update operation.
                    if attributes and uniqueKey not in attributes:
                        attributes.append(uniqueKey)

                    data = CI._get_data(obj, attributes=attributes)

                    missing = False   # Do we have that in scorched?
                    if not missing or atomic:
                        value = data.get(uniqueKey, None)
                        if value is not None:
                            log('indexing %r\n' % obj)

                            pt = data.get('portal_type', 'default')
                            adder = queryMultiAdapter((obj, conn), name=pt)
                            if adder is None:
                                adder = ContentAdder(obj, conn)
                            data['_solr_adder'] = adder
                            # Do not boost, c.solr only feature
                            updates[value] = data
                            processed += 1
                            cpi.next()
                    else:
                        log('missing data, skipping indexing of %r.\n' % obj)
                    if limit and count >= (skip + limit):
                        break
            except:
                logger.exception(
                    'Failed reindexing: %r (%s)',
                    obj,
                    path,
                )

        checkPoint()
        conn.commit()
        log('solr index rebuilt.\n')
        msg = 'processed %d items in %s (%s cpu time).'
        msg = msg % (processed, real.next(), cpu.next())
        log(msg)
        logger.info(msg)

    def sync(self, batch=1000, preImportDeleteQuery='*:*'):
        """Sync the Solr index with the portal catalog. Records contained
        in the catalog but not in Solr will be indexed and records not
        contained in the catalog will be removed.
        """
        self.disable_csrf()

        conn = IConnection(getUtility(IConnectionConfig))
        key = conn.schema['uniqueKey']
        CI = ContentIndexer()
        zodb_conn = self.context._p_jar
        catalog = getToolByName(self.context, 'portal_catalog')
        getIndex = catalog._catalog.getIndex
        modified_index = getIndex('modified')
        uid_index = getIndex(key)
        log = self.mklog()
        real = timer()          # real time
        lap = timer()           # real lap time (for intermediate commits)
        cpu = timer(clock)      # cpu time
        # get Solr status
        flares = conn.search(
            q=preImportDeleteQuery,
            rows=MAX_ROWS,
            fl='%s modified' % key)

        solr_results = {}
        solr_uids = set()

        def _utc_convert(value):
            Y, m, d, H, M = value.utctimetuple()[:5]
            return ((((Y * 12 + m) * 31 + d) * 24 + H) * 60 + M)

        for flare in flares:
            uid = flare[key]
            solr_uids.add(uid)
            if 'modified' in flare:
                solr_results[uid] = _utc_convert(flare['modified'])
        # get catalog status
        cat_results = {}
        cat_uids = set()
        for uid, rid in uid_index._index.items():
            cat_uids.add(uid)
            cat_results[uid] = rid
        # differences
        index = cat_uids.difference(solr_uids)
        solr_uids.difference_update(cat_uids)
        unindex = solr_uids
        processed = 0
        # XXX Why the difference to the reindex flush?
        # flush = notimeout(lambda: conn.flush())
        flush = notimeout(lambda: conn.commit(softCommit=True))

        def checkPoint():
            msg = 'intermediate commit (%d items processed, ' \
                  'last batch in %s)...\n' % (processed, lap.next())
            log(msg)
            logger.info(msg)
            flush()
            zodb_conn.cacheGC()
        cpi = checkpointIterator(checkPoint, batch)
        # Look up objects
        uid_rid_get = cat_results.get
        rid_path_get = catalog._catalog.paths.get
        catalog_traverse = catalog.unrestrictedTraverse

        def lookup(uid, rid=None,
                   uid_rid_get=uid_rid_get, rid_path_get=rid_path_get,
                   catalog_traverse=catalog_traverse):
            if rid is None:
                rid = uid_rid_get(uid)
            if not rid:
                return None
            if not isinstance(rid, int):
                rid = tuple(rid)[0]
            path = rid_path_get(rid)
            if not path:
                return None
            try:
                obj = catalog_traverse(path)
            except AttributeError:
                logger.warning('AttributeError traversing to path: %s', path)
                return None
            except KeyError:
                logger.warning('KeyError traversing to path: %s', path)
                return None
            return obj
        log('processing %d "unindex" operations next...\n' % len(unindex))
        op = notimeout(lambda uid: conn.delete_by_ids(ids=[uid]))
        for uid in unindex:
            obj = lookup(uid)
            if obj is None:
                op(uid)
                processed += 1
                cpi.next()
            else:
                log('not unindexing existing object %r.\n' % uid)
        log('processing %d "index" operations next...\n' % len(index))
        op = notimeout(lambda obj: CI.index(obj))
        for uid in index:
            obj = lookup(uid)
            if ICheckIndexable(obj)():
                op(obj)
                processed += 1
                cpi.next()
            else:
                log('not indexing unindexable object %r.\n' % uid)
            if obj is not None:
                obj._p_deactivate()
        log('processing "reindex" operations next...\n')
        op = notimeout(lambda obj: CI.reindex(obj))
        cat_mod_get = modified_index._unindex.get
        solr_mod_get = solr_results.get
        done = unindex.union(index)
        for uid, rid in cat_results.items():
            if uid in done:
                continue
            if isinstance(rid, IITreeSet):
                rid = rid.keys()[0]
            if cat_mod_get(rid) != solr_mod_get(uid):
                obj = lookup(uid, rid=rid)
                if ICheckIndexable(obj)():
                    op(obj)
                    processed += 1
                    cpi.next()
                else:
                    log('not reindexing unindexable object %r.\n' % uid)
                if obj is not None:
                    obj._p_deactivate()
        conn.commit()
        log('solr index synced.\n')
        msg = 'processed %d object(s) in %s (%s cpu time).'
        msg = msg % (processed, real.next(), cpu.next())
        log(msg)
        logger.info(msg)

    # XXX I keep this for the engaged listener as this can also be achieved
    # with the sync
    def cleanup(self, batch=1000):
        """ remove entries from solr that don't have a corresponding Zope
            object or have a different UID than the real object"""
        # cleanup is required by the interface definition
        raise NotImplementedError()
    #     manager = queryUtility(ISolrConnectionManager)
    #     proc = SolrIndexProcessor(manager)
    #     conn = manager.getConnection()
    #     log = self.mklog(use_std_log=True)
    #     log('cleaning up solr index...\n')
    #     key = manager.getSchema().uniqueKey

    #     start = 0
    #     resp = SolrResponse(conn.search(q='*:*', rows=batch, start=start))
    #     res = resp.results()
    #     log('%s items in solr catalog\n' % resp.response.numFound)
    #     deleted = 0
    #     reindexed = 0
    #     while len(res) > 0:
    #         for flare in res:
    #             try:
    #                 ob = PloneFlare(flare).getObject()
    #             except Exception as err:
    #                 log('Error getting object, removing: %s (%s)\n' % (
    #                     flare['path_string'], err))
    #                 conn.delete(flare[key])
    #                 deleted += 1
    #                 continue
    #             if not IUUIDAware.providedBy(ob):
    #                 no_skipping_msg = 'Object %s of type %s does not ' + \
    #                     'support uuids, skipping.\n'
    #                 log(
    #                     no_skipping_msg %
    #                     ('/'.join(ob.getPhysicalPath()), ob.meta_type)
    #                 )
    #                 continue
    #             uuid = IUUID(ob)
    #             if uuid != flare[key]:
    #                 log('indexed under wrong UID, removing: %s\n' %
    #                     flare['path_string'])
    #                 conn.delete(flare[key])
    #                 deleted += 1
    #                 realob_res = SolrResponse(conn.search(q='%s:%s' %
    #                                           (key, uuid))).results()
    #                 if len(realob_res) == 0:
    #                     log('no sane entry for last object, reindexing\n')
    #                     data, missing = proc.getData(ob)
    #                     prepareData(data)
    #                     if not missing:
    #                         boost = boost_values(ob, data)
    #                         conn.add(boost_values=boost, **data)
    #                         reindexed += 1
    #                     else:
    #                         log('  missing data, cannot index.\n')
    #         log('handled batch of %d items, commiting\n' % len(res))
    #         conn.commit()
    #         start += batch
    #         resp = SolrResponse(conn.search(
    #             q='*:*', rows=batch, start=start))
    #         res = resp.results()
    #     finished_msg = 'solr cleanup finished, %s item(s) removed, ' + \
    #         '%s item(s) reindexed\n'
    #     msg = finished_msg % (deleted, reindexed)
    #     log(msg)
    #     logger.info(msg)


class SolrOptimizeView(BrowserView):
    """
    View to start solr optimization.
    """

    def __call__(self):
        return self.optimize()

    # prevent DoS by allowing max 1 call per 5 mins
    @ram.cache(lambda *args: time() // 300)
    def optimize(self):
        self._solr.optimize(waitSearcher=None)
        return "solr optimized {}".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    @property
    def _solr_conf(self):
        return queryUtility(IConnectionConfig)

    @property
    def _solr(self):
        self._connection = IConnection(self._solr_conf)
        return self._connection
