# coding: utf-8

"""Utility methods for working with WSGI servers."""
from __future__ import absolute_import, print_function, unicode_literals, division

import sys
import six
import logging
import webob.dec
import webob.exc
from oslo_config import cfg

__all__ = ["Application", "Middleware", "Debug"]

CONF = cfg.CONF
LOG = logging.getLogger(__name__)
_ = (lambda v: v)


class Application(object):
    """Base WSGI application wrapper.

    Subclasses need to implement __call__.
    """

    @classmethod
    def factory(cls, global_config, **local_config):
        """Used for paste app factories in paste.deploy config files.
        Any local configuration (that is, values under the [app:APPNAME]
        section of the paste config) will be passed into the `__init__` method
        as kwargs.
        A hypothetical configuration would look like:
            [app:wadl]
            latest_version = 1.3
            paste.app_factory = nova.api.fancy_api:Wadl.factory
        which would result in a call to the `Wadl` class as
            import nova.api.fancy_api
            fancy_api.Wadl(latest_version='1.3')
        You could of course re-implement the `factory` method in subclasses,
        but using the kwarg passing it shouldn't be necessary.
        """
        return cls(**local_config)

    def __call__(self, environ, start_response):
        r"""Subclasses will probably want to implement __call__ like this:
        @webob.dec.wsgify(RequestClass=Request)
        def __call__(self, req):
          # Any of the following objects work as responses:
          # Option 1: simple string
          res = 'message\n'
          # Option 2: a nicely formatted HTTP exception page
          res = exc.HTTPForbidden(explanation='Nice try')
          # Option 3: a webob Response object (in case you need to play with
          # headers, or you want to be treated like an iterable, or or or)
          res = Response();
          res.app_iter = open('somefile')
          # Option 4: any wsgi app to be run next
          res = self.application
          # Option 5: you can get a Response object for a wsgi app, too, to
          # play with headers etc
          res = req.get_response(self.application)
          # You can then just return your response...
          return res
          # ... or set req.response and return None.
          req.response = res
        See the end of http://pythonpaste.org/webob/modules/dec.html
        for more info.
        """
        raise NotImplementedError(_('You must implement __call__'))


class Middleware(Application):
    """Base WSGI middleware.
    These classes require an application to be
    initialized that will be called next.  By default the middleware will
    simply call its wrapped app, or you can override __call__ to customize its
    behavior.
    """

    @classmethod
    def factory(cls, global_config, **local_config):
        """Used for paste app factories in paste.deploy config files.
        Any local configuration (that is, values under the [filter:APPNAME]
        section of the paste config) will be passed into the `__init__` method
        as kwargs.
        A hypothetical configuration would look like:
            [filter:analytics]
            redis_host = 127.0.0.1
            paste.filter_factory = nova.api.analytics:Analytics.factory
        which would result in a call to the `Analytics` class as
            import nova.api.analytics
            analytics.Analytics(app_from_paste, redis_host='127.0.0.1')
        You could of course re-implement the `factory` method in subclasses,
        but using the kwarg passing it shouldn't be necessary.
        """
        def _factory(app):
            return cls(app, **local_config)
        return _factory

    def __init__(self, application):
        self.application = application

    def process_request(self, req):
        """Called on each request.
        If this returns None, the next application down the stack will be
        executed. If it returns a response then that response will be returned
        and execution will stop here.
        """
        return None

    def process_response(self, response):
        """Do whatever you'd like to the response."""
        return response

    @webob.dec.wsgify(RequestClass=webob.Request)
    def __call__(self, req):
        response = self.process_request(req)
        if response:
            return response
        response = req.get_response(self.application)
        return self.process_response(response)


class Debug(Middleware):
    """Helper class for debugging a WSGI application.
    Can be inserted into any WSGI application chain to get information
    about the request and response.
    """

    @webob.dec.wsgify(RequestClass=webob.Request)
    def __call__(self, req):
        print(('*' * 40) + ' REQUEST ENVIRON')
        for key, value in req.environ.items():
            print(key, '=', value)
        print()
        resp = req.get_response(self.application)

        print(('*' * 40) + ' RESPONSE HEADERS')
        for (key, value) in six.iteritems(resp.headers):
            print(key, '=', value)
        print()

        resp.app_iter = self.print_generator(resp.app_iter)

        return resp

    @staticmethod
    def print_generator(app_iter):
        """Iterator that prints the contents of a wrapper string."""
        print(('*' * 40) + ' BODY')
        for part in app_iter:
            sys.stdout.write(part)
            sys.stdout.flush()
            yield part
        print()


def get_app(app, middleware_cls, **kwargs):
    """A convenient function to wrap the middlewares."""

    def _get_cls(cls):
        if isinstance(cls, six.string_types):
            cls = __import__(cls)
        return cls

    for m in reversed(middleware_cls):
        cls = _get_cls(m)
        try:
            app = cls(app, kwargs)
        except TypeError:
            app = cls(app)

    return app
