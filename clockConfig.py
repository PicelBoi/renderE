# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: Config.py
# Compiled at: 2007-04-27 10:00:45
import twc

def setProductDirectory(path):
    _setValue('productDir', path)
    return


def setPackageDirectory(val):
    _setValue('packageDir', val)
    return


def setWorkDirectory(path):
    _setValue('workDir', path)
    return


def setClimoDataDirectory(path):
    _setValue('climoDataDir', path)
    return


def setTempDirectory(path):
    _setValue('tempDir', path)
    return


def setDefaultClockFile(file):
    _setValue('defaultClockFile', file)
    return


def setClockFileKey(key):
    _setValue('clockFileKey', key)
    return


def setPreroll(seconds):
    _setValue('preroll', seconds)
    return


def setSevereModeClockFileKey(key):
    _setValue('severeModeClockFileKey', key)
    return


def setChannel(chan):
    _setValue('channel', chan)
    return


def setPidFileDirectory(dir):
    _setValue('pidFileName', dir)
    return


def setAppName(name):
    _setValue('appName', name)
    return


def hideUserDefinedNames(hideNames=1):
    _setValue('hideUserDefinedNames', hideNames)
    return


_values = twc.Data()

def _setValue(valName, val):
    global _values
    _values.__dict__[valName] = val
    return


def getValues():
    return _values
    return

