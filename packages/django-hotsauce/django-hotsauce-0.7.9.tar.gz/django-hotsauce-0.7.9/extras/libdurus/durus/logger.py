"""
$URL: svn+ssh://svn.mems-exchange.org/repos/trunk/durus/logger.py $
$Id: logger.py 29018 2006-10-31 21:03:13Z rmasse $
"""

import sys
from logging import getLogger, StreamHandler, Formatter, DEBUG

logger = getLogger('durus')
log = logger.log

def direct_output(f):
    logger.handlers[:] = []
    handler = StreamHandler(f)
    handler.setFormatter(Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    logger.setLevel(DEBUG)
    if f is sys.__stderr__:
        return
    if sys.stdout is sys.__stdout__:
        sys.stdout = file
    else:
        log(100, "sys.stdout already customized.")
    if sys.stderr is sys.__stderr__:
        sys.stderr = file
    else:
        log(100, "sys.stderr already customized.")

if not logger.handlers:
    direct_output(sys.stderr)

def is_logging(level):
    return logger.getEffectiveLevel() <= level

