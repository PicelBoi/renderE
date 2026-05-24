# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: init.py
# Compiled at: 2007-01-12 11:33:37
import domestic.HeatSafetyTipManager, twcWx.ClimatologyDataManager, twc.dsmarshal, twccommon.Log, nethandler as nh
dsm = twc.dsmarshal

def init(config):
    global _config
    _config = config
    _setClimIds(dsm.defaultedGet('interestlist.climId', []))
    setHeatSafetyDataFile(_config.heatSafetyDataFile)
    return


def setClimIds(climIds):
    _setClimIds(climIds)
    return


def setHeatSafetyDataFile(fname):
    print('using heat-safety-tips data: %s' % (fname,))
    domestic.HeatSafetyTipManager.init(fname)
    return


def uninit():
    return


_config = None

def _setClimIds(climIds):
    twccommon.Log.info('using climIds: %s' % (str(climIds),))
    twcWx.ClimatologyDataManager.processDataFile(climIds)
    return

