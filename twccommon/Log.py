# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: Log.py
# Compiled at: 2006-04-03 09:02:55
import sys, traceback, logging
CRIT = logging.CRITICAL
ERR = logging.ERROR
WARN = logging.WARNING
INFO = logging.INFO
DBG = logging.DEBUG
globalPfx = None
interface = None
identstr = "defaultident"

def setIdent(ident):
    """Set the identifing name that is printed w/ each log entry."""
    global identstr
    identstr = ident
    return


def setLevel(level):
    """Set the logging level so that lower level messages are not logged."""
    if level < CRIT or level > DBG:
        raise RuntimeError('invalid log level')
    logging.getLogger().setLevel(level=level)
    return


def setPrefix(pfx):
    global globalPfx
    globalPfx = pfx
    return


def clearPrefix():
    global globalPfx
    globalPfx = None
    return


def tryPrefix(msg, pfx):
    """Use the prefix-arg instead of the gloabal-prefix if one is passed in"""
    if pfx == None:
        pfx = globalPfx
    if pfx == None:
        return msg
    else:
        return '%s: %s' % (pfx, msg)
    return


def critical(msg, pfx=None):
    logging.critical(tryPrefix(msg, pfx))
    return


def error(msg, pfx=None):
    logging.error(tryPrefix(msg, pfx))
    return


def warning(msg, pfx=None):
    logging.warning(tryPrefix(msg, pfx))
    return


def info(msg, pfx=None):
    logging.info(tryPrefix(msg, pfx))
    return


def debug(msg, pfx=None):
    logging.debug(tryPrefix(msg, pfx))
    return

exc_id = 0
def logCurrentException(prefix=''):
    global exc_id
    try:
        (etype, val, tb) = sys.exc_info()
        msg = traceback.format_exception(etype, val, tb)
        if prefix:
            msg = [prefix] + msg
        for i, mstr in enumerate(msg):
            error(mstr)
        with open(f"logged_exc{exc_id}.txt", "w") as f:
            f.write("\n".join(msg))
        exc_id += 1
    finally:
        etype = val = tb = None
    return


def _getInterfaceInitial():
    global _getInterface
    global interface
    logging.getLogger().setLevel(INFO)
    return interface
    return


def _getInterfaceLoaded():
    return


_getInterface = _getInterfaceInitial
