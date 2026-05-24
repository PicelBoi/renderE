# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: MiscCorbaInterface.py
# Compiled at: 2007-01-12 11:17:30
import twccommon.Log
import tscard
interface = None

def signalEvent(channelName, eventType, eventValue):
    global _getInterface
    return _getInterface().signalEvent(channelName, eventType, eventValue)
    return


def runRenderScript(rsName, host='localhost', port=4000, nsName='Renderd'):
    return _getInterface().runRenderScript(rsName, host, port, nsName)
    return


def queueMovie(moviefile, host='localhost', port=4000, nsName='Vspoold'):
    tscard.queueMovie(moviefile)


def setMovieLooping(val, host='localhost', port=4000, nsName='Vspoold'):
    return _getInterface().setMovieLooping(val, host, port, nsName)
    return


def flushMovies(host='localhost', port=4000, nsName='Vspoold'):
    return _getInterface().flushMovies(host, port, nsName)
    return


def _getInterfaceInitial():
    global _getInterface
    global interface
    if interface == None:
        import twc.MiscCorbaInterfaceImpl
        interface = twc.MiscCorbaInterfaceImpl.InterfaceImpl()
    _getInterface = _getInterfaceLoaded
    return interface
    return


def _getInterfaceLoaded():
    return interface
    return


_getInterface = _getInterfaceInitial
