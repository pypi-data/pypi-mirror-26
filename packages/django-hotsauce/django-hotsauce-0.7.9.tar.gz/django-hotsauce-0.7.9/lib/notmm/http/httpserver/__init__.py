#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (C) 2007-2013 Etienne Robillard <erob@gthcfoundation.org>
# All rights reserved.
# <LICENSE=APACHEV2> 
"""WSGI helper functions and classes for development purposes.

"""

import sys
import urllib
import logging
import time
from wsgiref import simple_server, validate

from notmm.utils.configparse import string_getter, int_getter
from notmm.utils.wsgilib import translogger 
from notmm.release import BASEVERSION

import reloader

from django.utils.termcolors import colorize as _colored
    
log = logging.getLogger(__name__)

__all__ = ('WSGIServerBase', 'BannerBase', 'get_bind_addr', 'daemonize')

class BannerBase(object):
    """This is a simple startup banner.

    Usage:
        >>> banner = BannerBase(fp=sys.stderr, ('127.0.0.1', '8000'))
        >>> banner.show()
    """

    default_format = "%Y-%m-%d %H:%M:%S %Z %z"
    debug_msg_handler = log.info

    def __init__(self, fp=debug_msg_handler, bind_addr=('127.0.0.1', '8000'),
                 settings=None):
        self.bind_addr = bind_addr
        fmt = self.get_default_format(settings)
        self.start_time = time.strftime(fmt)
        self.server_uri = 'http://%s:%i/' % bind_addr
        if not isinstance(self.bind_addr, tuple):
            raise ValueError("Error: invalid bind_addr type: %r" \
                % type(self.bind_addr))

        #assert len(self.bind_addr) == 2, \
        #    'bind_addr must contains exactly two elements'

    def get_default_format(self, settings):
        try:
            fmt = settings.DATETIME_INPUT_FORMATS[0]
        except (AttributeError, IndexError):
            return self.default_format
        else:
            return fmt
    
    def debug(self, message, color='cyan', **kwargs):
        """Write a string to the terminal with colored output"""
        self.debug_msg_handler(_colored(message, color, **kwargs))

    def show(self, registered=False):
        """Override this method to handle the formatting of the banner"""

        self.debug("Initializing on %s" % self.start_time)
        self.debug("Starting HTTP server on %s" % self.server_uri)
        #colored("notmm %s "%(notmm.__version__)) 
        #colored("%s"%notmm.__copyright__)
        # XXX this part need more work ! :)
        if not registered:
            self.debug("Django-hotsauce %s (Open Source Edition)" % BASEVERSION)
        else:
            self.debug("Django-hotsauce %s (FooCorp Inc)" % BASEVERSION)
        #self.debug("To register your copy online, visit http://www.gthcfoundation.org/software/django-hotsauce/#licensing")
        #colored("Found a bug? Submit a bug report to http://notmm.org/bug")
        
        return self

class WSGIServerBase(object):
    """Wrapper class to configure a simple HTTP server instance"""
    
    # Uncomment this to enable cherrypy based http daemon
    # serverClass = wsgiserver.CherryPyWSGIServer
    
    serverClass = simple_server # wsgiref
    
    def __init__(self, wsgi_app, bind_addr, debug=False):
        """HTTPServer.__init__"""
        self.host = bind_addr[0]
        self.port = bind_addr[1]
        if debug:
            # run the wsgi app in using wsgiref validator
            # middleware
            self.request_handler = validate.validator(wsgi_app)
        else:
            self.request_handler = wsgi_app

        #
        b = BannerBase(bind_addr=bind_addr)
        b.show()
    
        self.server = self.serverClass.make_server(self.host, self.port, self.request_handler)
    
    def serve(self):
        self.server.serve_forever()

def get_bind_addr(app_conf, section='httpserver', listen_port=8000):
    """
    Return a 2-element tuple containing the hostname and port
    to listen for remote connections.
    """

    host = string_getter(app_conf, section, 'host') or urllib.localhost()
    port = int_getter(app_conf, section, 'port') or listen_port

    return (host, port)

def daemonize(wsgi_app, bind_addr, logging=False, autoreload=True, debug=True):
    """
    Create an instance of a validating WSGI server for 
    development purposes.
    
    XXX: enabling WSGI validation (debug=True) may trigger
    a deadlock for POST input data processing.
    """
    
    # Install translogger middleware if logging is enabled
    if logging:
        request_handler = translogger.TransLogger(wsgi_app)
    else:
        request_handler = wsgi_app
    
    # Add optional autoreloading support (see the docstring for help
    # on installing this)
    if autoreload:
        try:
            reloader.install()
        except ImportError:
            pass


    # init the wsgi server 
    server = WSGIServerBase(request_handler, bind_addr, debug=debug)

    try:
        server.serve()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
    except:
        raise

class HTTPServer(WSGIServerBase):
    pass

class GeventHTTPServer(WSGIServerBase):    
    pass
