# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: HeatSafetyTipManager.py
# Compiled at: 2007-01-12 11:33:26
"""
Provides a way to read in the Heat Safety Tips File and insert them into 
a list.  Will also return the correct tupple to product requesting data.
"""
import os
_tipList = []
_index = 0

def execfile(filename, globa, loca):
    with open(filename, "r", encoding="windows-1252") as f:
        exec(compile(f.read(), filename, 'exec'), globa, loca)


def init(fileName):
    ns = {}
    ns['addTip'] = addTip
    execfile(fileName, ns, ns)
    return


def addTip(title, tip):
    _tipList.append((title, tip))
    return


def getTip():
    global _index
    str = _tipList[_index]
    _index = (_index + 1) % len(_tipList)
    return str
    return

import nethandler as nh
import domestic.HeatSafetyTipManager as hsm
hsm.init(nh.requestNetAssetExt("/usr/twc/domestic/data/heatSafetyTips.data"))