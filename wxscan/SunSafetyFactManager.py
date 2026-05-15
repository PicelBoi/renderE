# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: SunSafetyFactManager.py
# Compiled at: 2007-04-27 10:00:47
"""
Provides a way to read in the Sun Safety Facts File and break them into 
winter and summer sun safety fact lists.  Will also return the correct
tupple to product requesting data.
"""
import random, os, time
import nethandler
_summerFactList = []
_winterFactList = []
_summerIndex = 0
_winterIndex = 0
_fileName = None
_lastModified = 0

def execfile(filename, globa, loca):
    with open(filename, "r", encoding="windows-1252") as f:
        exec(compile(f.read(), filename, 'exec'), globa, loca)

def init(fileName):
    global _fileName
    global _lastModified
    global _summerFactList
    global _summerIndex
    global _winterFactList
    global _winterIndex
    if _fileName is None:
        _fileName = fileName
        fn = nethandler.requestNetAssetExt(_fileName)
        _lastModified = os.stat(fn)[8]
    else:
        fn = nethandler.requestNetAssetExt(_fileName)
    lastModified = os.stat(fn)[8]
    if lastModified > _lastModified:
        _lastModified = lastModified
        _summerFactList = []
        _winterFactList = []
        _summerIndex = 0
        _winterIndex = 0
    ns = {}
    ns['addFact'] = addFact
    ns['addTip'] = addFact
    execfile(fn, ns, ns)
    return


def addFact(summer, fact, source):
    if summer:
        _summerFactList.append((fact, source))
    else:
        _winterFactList.append((fact, source))
    return


def getFact(summer):
    global _lastModified
    global _summerFactList
    global _summerIndex
    global _winterFactList
    global _winterIndex
    lastModified = os.stat(_fileName)[8]
    if lastModified > _lastModified:
        _lastModified = lastModified
        _summerFactList = []
        _winterFactList = []
        _summerIndex = 0
        _winterIndex = 0
        ns = {}
        ns['addFact'] = addFact
        execfile(_fileName, ns, ns)
    if summer:
        if len(_summerFactList):
            str = _summerFactList[_summerIndex]
            _summerIndex = (_summerIndex + 1) % len(_summerFactList)
        else:
            str = None
    elif len(_winterFactList):
        str = _winterFactList[_winterIndex]
        _winterIndex = (_winterIndex + 1) % len(_winterFactList)
    else:
        str = None
    return str
    return

