#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2007-2017 Etienne Robillard <tkadm30@yandex.ru>
# All rights reserved.
"""BaseController API Version 0.7.8

Python extension module to implement MVC-style "controllers"
for Django and WSGI type apps. In short, ``BaseController`` derived
extensions are request handlers resolving a ``path_url`` string
to a matching ``view function``. The response handler (view function)
then resolve the appropriate HTTP response to the client.

TODO:
-Better module-level documentation (work-in-progress)
-Compatibility with mod_wsgi (Apache2) (YMMV...)
-Change all prints by log() hooks (work-in-progress)
-use signals to log messages from pubsub like BUS

Define and document the internal request handling stages when
using native Django views (WSGIHandler):
 __init__,         # application init -> self.init_request(env)
 init_request,     # setup the environment -> self.process_request(req)
 process_request,  # handle the request -> self.locals.request = req
 get_response,     # resolve request [PATH_INFO] -> response_callback
 application,      # response stage 2 [WSGI] -> response_callback(env, start_response)
"""

import sys
import os
import urllib
import logging
import django
import traceback
#import gevent

from gevent import monkey
monkey.patch_all()

from importlib import import_module
from gevent.local import local
from contextlib import contextmanager
from notmm.utils.wsgilib import (
    #HTTPClientError, 
    HTTPServerError, 
    HTTPRequest, 
    HTTPResponse,
    HTTPNotFound,
    HTTPUnauthorized
    #HTTPException
    )
from notmm.controllers.wsgi cimport BaseControllerMixIn
from notmm.release import VERSION as SOFTWARE_VERSION
from notmm.utils.django_compat import get_resolver, NoReverseMatch
from notmm.utils.django_settings import SettingsProxy
from werkzeug.local import LocalProxy

RequestClass = HTTPRequest

_requests = local()

_logger = logging.getLogger(__name__)

__all__ = ('BaseController', 'WSGIController', 'sessionmanager', 'get_current_request', 'request')

try:
    django.setup()
except:
    _logger.debug("django.setup() is disabled")


@contextmanager
def sessionmanager(environ):
    _requests.request = RequestClass(environ)
    yield
    _requests.request = None

def get_current_request():
    try:
        return _requests.request
    except AttributeError:
        raise TypeError("No request object for this thread")


request = LocalProxy(lambda: get_current_request())

class BaseController(BaseControllerMixIn):
    
    def sethandle(self, name, string_or_callable):
        """Adds custom response handlers to a BaseController subclass.
        """

        # If string_or_callable is in the form of "foo.bar.quux",
        # the callable function should be the last part of the
        # string
        handler = None
        if isinstance(string_or_callable, str):
            if string_or_callable.find('.') != -1:
                bits = string_or_callable.rsplit('.', 1)
                m = __import__(bits[0], globals(), locals(), fromlist=[''])
                for component in bits[1:]:
                    if hasattr(m, component):
                        handler = getattr(m, component)
                        break
                    else:
                        #print 'debug: module %s has no such member: %r' % (m, component)
                        continue
        elif callable(string_or_callable):
            handler = string_or_callable
        else:
            raise ValueError("Unexpected string_or_callable type: %r" % \
                type(string_or_callable))

        if not callable(handler) and isinstance(handler, str):
            # Attempt to import it
            # XXX write a native eval_import hook
            if 'debug.config.eval_import_func' in self.app_conf:
                handler_obj = self.app_conf['debug.config.eval_import_func'](handler)
            else:
                raise Exception("fatal error: debug.config.eval_import_func not set!")
        else:
            handler_obj = handler

        # XXX Use staticmethod(func) here, because we want to support the
        # same positional arguments named by this callable
        setattr(self, name, handler_obj)

        return None

    def __call__(self, environ, start_response, exc_info=None):
        # WSGI 1.0 mandates to return a callable object
        #self._environ.update(environ)
        if exc_info is not None:
            # TODO: exc_info verifications
            self.logger.debug(exc_info)
            return self.application(environ, start_response, exc_info)
        return self.application(environ, start_response)

    def application(self, environ, start_response):
        """
        Override this to change the default request/response
        handling.

        This method is used for properly returning a WSGI response instance
        by calling ``get_response``.

        The latter does the grunt work of routing the request to the
        proper callable function or class.

        """

        with sessionmanager(environ):
            request.environ.update(environ)
            #assert request.environ['PATH_INFO'] == request.path_url
            response = self.get_response(request=request)
        return response(environ, start_response)

    def registerWSGIHandlers(self, d):
        """Register appropriate wsgi callbacks (legacy method
        for backward compat only)"""
        for k, v in d:
            # "register" the callback function as a standard Django view
            # accessible by the controller extension
            self.sethandle(k, v)
        #self.registered = True
        return None
    
    def init_request(self, environ, request_class=RequestClass):
        """A method to execute before ``process_request``"""
        pass
            
    def get_request(self):
        return get_current_request()
        #pass

    request = property(get_request)

    def process_request(self, request):
        pass

    def get_response(self, request=None, method='GET', data={}):
        """Process ``path_url`` and return a callable function as
        the WSGI ``response`` callback.

        The callback view function is resolved using the built-in
        Django ``RegexURLResolver`` class.

        Returns a callable function (Response) or None if no
        view functions matched.

        See the docs in :notmm.utils.django_compat.RegexURLResolver:
        for details.

        This function may be overrided in custom subclasses to modify
        the response type.
        """
        # Match the location to a view or callable
        #path_info = self.get_path_info(self.environ)

        try:
            if self.debug:
                #assert self.request != None, 'invalid request object!'
                self.logger.debug("Resolving path=%r"%request.path_url)

            # Resolve the path (endpoint) to a view using legacy Django URL
            # resolver.
            (callback, args, kwargs) = self.resolver.resolve(str(request.path_url))
            if self.debug and self.logger:
                self.logger.debug("callback resolved=%r"%callback)
            # Create the wsgi ``response`` object.
            response = callback(request, *args, **kwargs)
        except NoReverseMatch as e:
            # Handle 404 responses with a custom 404 handler.
            self.logger.info('Document not found=%s'%request.path_url)
            self.logger.debug(e)
            #handleclienterror(self.request)

            return self.handle404(request)
        except (HTTPServerError, Exception):

            exc = traceback.format_exc(sys.exc_info)

            if self.debug:
                #print "FOOBAR: %s" % exc
                self.logger.debug(exc)
                #assert isinstance(request, RequestClass) == True, type(request)

            return self.handle500(request)
        except (HTTPUnauthorized), exc:
            if self.debug:
                self.logger.debug("Caught authorization exception")
                self.logger.debug(exc)
            return self.handle401(request)
        else:
            #manager.clear()
            return response
    def _environ_getter(self):
        """ Returns the current WSGI environment instance."""
        return self.request.environ
    environ = property(_environ_getter)

    def _method_getter(self):
        return self.environ['REQUEST_METHOD']
    method = property(_method_getter)

    def _debug_getter(self):
        """Global debug flag. 
        Set settings.DEBUG to False to disable debugging"""
        return bool(self.settings.DEBUG == True)
    debug = property(_debug_getter)

    def _get_path_info(self, env):
        return str(env.get('PATH_INFO', ''))


class WSGIController(BaseController):

    def __init__(self,
        settings=None,          #Django like settings module (default=$DJANGO_SETTINGS_MODULE)
        #New: dict based configuration (app_conf)
        #TODO document the changes in docs/config.txt
        app_conf={
            #'wsgi.request_class'        : HTTPRequest,     #WSGI Request middleware
            #'wsgi.response_class'       : HTTPResponse,    #WSGI Response middleware
            #'django.urlconf_class'      : None,           #Django URLConf module (default=$ROOT_URLCONF)
            'django.settings_autoload'  : True,          #Set this to False to disable Django settings autoloading (True)
            'logging_conf':None,      #Logging module to handle logging events at run-time  (experimental)
            'logging_instance':_logger,
            'logging.disabled': False,  #Set this to True to disable logging (experimental)
            #'experimental.enable_pubsub': False,#Put to this to False to disable
            #'experimental.enable_epool' : False,
            #'experimental.enable_i18n'  : False,
            #'debug.sheep.mode' :    0,
            #'debug.expert.mode':    0,
            #'debug.insane.mode':    10,
            #'debug.ponies.riding.unicorns': 1,
            #'debug.bugtracker.url': '',
            #'debug.homepage.url': 'https://wiki.python.org/moin/EtienneRobillard/DjangoHotSauce',
            #'debug.i18n.enable_unicode':True,
            #'debug.config.eval_import_func':paste_eval_import,
            #'license.registered': False,
            #'license.type': 'Apache License Version 2',
            #'license.owner.name': 'Etienne Robillard',
            #'license.owner.year': _current_date.year,
            #'license.owner.month': _current_date.month,
            #'license.version': SOFTWARE_VERSION,
            #'license.url': '',
        }):

        """
        Initializes a ``BaseController`` instance for processing
        standard Django view functions and handling basic error conditions.

        Available keyword arguments:

        - ``settings``: Django settings module (optional)
        - ``app_conf``: Dict of configuration options. (optional)
        """
        
        #self._session = local()
        #self._session.environ = {}

        # license registration flag
        # self.registered = app_conf.get('license.registered', False)

        #self.manager = ThreadLocalManager(default={'request': None})
        #self._request = self.init_request(self._environ)
        # initialize Django module by importing Django settings
        # if True. (Bool)
        autoload = app_conf.get('django.settings_autoload', True)
        if settings is None:
            self.settings = SettingsProxy(autoload=autoload).get_settings()
        else:
            self.settings = settings

        # Setup basic logging to /var/log/django.log (default)
        logging_disabled = app_conf.get('logging.disabled', False)
        if not logging_disabled:
            self.logger = _logger
        else:
            self.logger = None

        # If using legacy autoload mecanism, attempt to register user-specified
        # wsgi callbacks.
        if (autoload and hasattr(self.settings, 'CUSTOM_ERROR_HANDLERS')):
            self.registerWSGIHandlers(self.settings.CUSTOM_ERROR_HANDLERS)

        #if self.debug:
        #    log.info('logging initialized!')


        # Setup the urlconf
        # XXX This should only be necessary if using Django and is not
        # required for WSGI apps.
        #_urlconf_class = app_conf.get('django.urlconf_class', None)
        #if _urlconf_class is not None:
        #    setattr(self, 'urlconf', _urlconf_class(
        #        getattr(self.settings, 'ROOT_URLCONF')))
        #else:
        #    # work around: use django.conf.settings as
        #    # our last hope to make things work. (legacy mode)
        
        if (autoload and 'ROOT_URLCONF' in self.settings):
            setattr(self, 'urlconf', self.settings.ROOT_URLCONF)
            setattr(self, 'resolver', get_resolver(self.urlconf))
            if not hasattr(self.resolver, '_urlconf_module'):
                self.resolver._urlconf_module = import_module(self.urlconf)
        else:
            self.resolver = None
            self.urlconf = None
        
        # sanity checks 
        if self.debug:
            assert self.urlconf != None, 'urlconf instance cannot be None!'
            assert self.resolver != None, 'resolver instance cannot be None!'

        # Do something with app_conf here
        self.app_conf = app_conf

