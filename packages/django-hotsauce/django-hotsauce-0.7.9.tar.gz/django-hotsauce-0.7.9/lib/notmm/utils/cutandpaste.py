# this file is deprecated! should go away in 0.4.5-beta4
# Copyright (C) 2007-2013 Etienne Robillard
# All rights reserved.
# <LICENSE=ISC>
"""Several helper functions."""

import sys,time,urllib
from notmm.release import BASEVERSION

try:
    import termcolor
    _colored = termcolor.colored
except (ImportError, AttributeError):
    from django.utils.termcolors import colorize as _colored
    
__all__ = ('stdout', 
           'colored', 
           'notification',
           'SimpleHTTPBanner', 
           'get_bind_addr', 
           'daemonize')


def stdout(s):
    return sys.stderr.write("%s\n"%s)

def colored(message, color='cyan', **kwargs):
    """Write a string to the terminal with colored output"""
    stdout(_colored(message, color, **kwargs))

_event_types = {
    'info': lambda s: colored(s, color='blue', attrs=['bold']),
    'debug': lambda s: colored(s, color='white', attrs=['bold']),
    'warning': lambda s: colored(s, color='orange', attrs=['bold'])
}
info = _event_types['info']
notification = info


