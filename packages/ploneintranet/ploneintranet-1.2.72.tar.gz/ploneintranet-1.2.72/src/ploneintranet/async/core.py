"""
Generically re-usable async infrastructure for Plone.
"""

import logging
from zope.component import getMultiAdapter
from zope.interface import implementer
from BeautifulSoup import BeautifulSoup
import requests

from ploneintranet.async.interfaces import IAsyncTask
logger = logging.getLogger(__name__)


def _key_for_task(**kwargs):
    return '-'.join(sorted([str(x) for x in kwargs.values()]))


class DispatchError(Exception):
    pass


# pre-processor in Plone before handing off to Celery

@implementer(IAsyncTask)
class AbstractPost(object):
    """
    Execute a HTTP POST request asynchronously via Celery.

    Extracts authentication credentials from a original request
    and submits a new post request, taking special care
    that all calls are properly serialized.

    Sets a `X-celery-task-name` http header for task request routing
    in HAProxy etc. YMMV.

    This task is suitable as a base class for more specialized
    subclasses. It is structured as if it were an adapter but
    it is not registered or used as an adapter.

    See tasks.Post for an actual implementation example.
    """

    task = None  # set this in your concrete subclass
    url = None
    # set this to true and the dispatcher will use redis to keep a counter
    # in redis and the task is first executed if the counter is back to 0
    # the method to calculate a unique key currently uses the url and the
    # task.name to identify tasks that can be debounced.
    debounce = False

    def __init__(self, context, request):
        """Extract credentials."""
        self.context = context
        self.request = request
        self.headers = {'X-celery-task-name': self.task.name}

        # Plone auth will be set as '__ac' cookie
        self.cookies = request.cookies
        # Zope basic auth
        if self.request._auth:
            # avoid error: Can't pickle <type 'instancemethod'>
            auth = self.request._auth  # @property?
            self.headers['Authorization'] = auth

        # we need context and request for CSRF protection
        authenticator = getMultiAdapter((self.context, self.request),
                                        name=u"authenticator")
        self.data = {'_authenticator': authenticator.token()}

    def __call__(self, url=None, data={}, headers={}, cookies={}, **kwargs):
        """Start a Celery task that will execute a post request.

        The optional `url` argument may be used to override `self.url`.
        The optional `data`, `headers` and `cookies` args will update
        the corresponding self.* attributes.

        `self.task.apply_async` will be called
        and is expected to call `url` with
        `self.headers` as request headers,
        `self.cookie` as request cookies, and `self.data` as post data
        via the python request library.

        `**kwargs` will be passed through as arguments to celery
        `apply_async` so you can set async execution options like
        `countdown`, `expires` or `eta`.

        Returns a <class 'celery.result.AsyncResult'> when running async,
        or a <class 'celery.result.EagerResult'> when running in sync mode.
        """
        if not url:
            url = self.url
        if not url:
            url = self.context.absolute_url()
        elif url.startswith('/'):
            url = "%s%s" % (self.context.absolute_url(), url)
        elif not url.startswith('http'):
            url = "%s/%s" % (self.context.absolute_url(), url)
        self.data.update(data)
        self.headers.update(headers)
        self.cookies.update(cookies)

        if self.debounce is True:
            # Debounce the call
            key = _key_for_task(url=url, task=self.task.name)
            # loaded here to avoid circular imports
            from ploneintranet.async.celerytasks import app
            conn = app.backend
            # Self healing
            if conn.client.get(key) < 0:
                conn.client[key] = 0
            val = conn.client.incr(key)
            logger.info("generate_and_add_preview: Debouncing:" +
                        " key %s incremented to %s" % (key, val))

        logger.info("Dispatching async: %s(%s, ...)", self.task.name, url)
        # calling code should handle redis.exceptions.ConnectionError
        return self.task.apply_async(
            (url, self.data, self.headers, self.cookies),
            **kwargs)


# executed within Celery. To see the log messages:
# bin/celery -A ploneintranet.async.celerytasks worker -l debug

def dispatch(url, data={}, headers={}, cookies={}):
    """
    Execute a HTTP POST via the requests library.
    This is not a task but a building block for Celery tasks.

    :param url: URL to be called by celery, resolvable behind
                the webserver (i.e. {portal_url}/path/to/object)
    :type url: str

    :param data: POST variables to pass through to the url
    :type data: dict

    :param headers: request headers.
    :type headers: dict

    :param cookies: request cookies. Normally contains __ac for Plone.
    :type cookies: dict

    Debugging
    ---------

    This code path is executed in Celery, not in Plone!
    You cannot insert a pdb. Instead, debug via log messages.
    To see the log messages, run celery manually:

    bin/celery -A ploneintranet.async.celerytasks worker -l debug

    """
    logger.info('Calling %s', url)
    logger.debug('headers: %s' % str(headers))
    logger.debug('data: %s' % str(data))
    resp = requests.post(url,
                         headers=headers,
                         cookies=cookies,
                         data=data)
    if resp.status_code != 200:
        logger.error("Invalid response %s: %s on <%s>: %s",
                     resp.status_code, resp.reason, url, resp.text)
        if 'error has been logged' in resp.text:
            errcode = BeautifulSoup(resp.text).code.string
            logger.error(
                "Error logged in {portal_url}/error_log/showEntry?id=%s",
                errcode)
        # trigger retry in celerytasks.py
        raise DispatchError(resp.text)
    elif 'login_form' in resp.text \
         or 'Insufficient Privileges' in resp.text:
        logger.error("Unauthorized (masked as 200 OK)")
        # it does not make sense to retry this one, so no raise
    else:
        # success
        logger.info("%s: %s", resp.status_code, resp.reason)
        logger.debug(resp.text)
