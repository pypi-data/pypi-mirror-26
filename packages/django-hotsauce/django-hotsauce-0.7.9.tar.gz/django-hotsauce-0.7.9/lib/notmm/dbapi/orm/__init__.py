"""Simplified ORM abstraction module for Schevo""" 

from ._databaseproxy import DatabaseProxy, ConnectionError
from ._relation import RelationProxy

#XXX: AnonymousUser should be defined in blogengine.contrib.anonymoususer
#from models import AnonymousUser
#from .model import ModelManager

from .schevo_compat import XdserverProxy
from .zodb_compat import ClientStorageProxy, ZODBFileStorageProxy

from management.commands import introspect

from notmm.utils.django_settings import LazySettings

#Add basic session management stuff 
#from .sql import (
#    ScopedSession as scoped_session,
#    with_session
#    )

_settings = LazySettings()
_installed_models = []


def get_models():
    return _installed_models

def setup():
    populate()

def populate(verbose=False):
    """Populate _installed_models with the list of configured models"""
    for app in _settings.INSTALLED_APPS:
        if verbose:
            log.debug("Configuring %s" % app)
        app_info = introspect.by_module_name(app)
        _installed_models.append(app_info)


__all__ = [
    'DatabaseProxy',
    'RelationProxy', 
    'XdserverProxy',
    'ConnectionError',
    #'models', 
    'schevo_compat',
    'zodb_compat'
    #'AnonymousUser',
    #'scoped_session',
    #'with_session',
    #'with_schevo_database']
    ]    
