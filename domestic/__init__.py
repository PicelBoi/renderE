# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: __init__.py
# Compiled at: 2007-01-12 11:33:26
import os, os.path, twc, twc.dsmarshal, twc.psp, twccommon, twccommon.PluginManager, types, string, domestic.BulletinInfo, twcWx.dataUtil as wxDataUtil, domestic.SunRiseSet as SunRiseSet, domestic.HeatSafetyTipManager as HeatSafetyTipManager
from domestic import dataUtil
from domestic.Heuristic import *
dsm = twc.dsmarshal
BulletinInfo = domestic.BulletinInfo

def tmpFile(dir, base='', ext='tmp'):
    global _ID
    fname = '%s/%s_%d.%s' % (dir, base, _ID, ext)
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    f = open(fname, 'w')
    _ID += 1
    return (fname, f)
    return


def checkActiveWarnings():
    interestlist = dsm.defaultedConfigGet('interestlist.county', [])
    bulletins = BulletinInfo.loadActiveBulletins(interestlist)
    bKeys = bulletins.keys()
    for key in bKeys:
        if bulletins[key].category == BulletinInfo.CAT_WARNING:
            return 1

    return 0
    return

def execfile(filename, globa, loca):
    with open(filename, "r", encoding="windows-1252") as f:
        exec(compile(f.read(), filename, 'exec'), globa, loca)

def checkRadarPrecip(RadarProductName, imageList=None):
    """Checks for significant radar returns (precip) in a given image
       list. If a list isn't provided, it will look up the latest images
       on disk. If a list IS provided, then we ignore the ProductName and
       ConfigSet. This method assumes that the imageList passed in only
       contains valid images and is already sorted from OLDEST to NEWEST."""
    radarReturns = 0
    imageRoot = os.path.join(os.environ["RENDEREROOT"], 'radar/us.cuts/')
    productString = 'Config.' + dsm.getConfigVersion() + '.' + RadarProductName
    if imageList == None:
        imageList = dataUtil.getValidFileList(dataPath=imageRoot, prefix=productString, suffix='*[0-9].tif', startTimeNdx=3, endTimeNdx=4, sortIndex=3)
    if len(imageList) == 0:
        twccommon.Log.warning('checkRadarPrecip: no valid images found for %s.' % (productString,))
        return radarReturns
    (issuetime, newestImageDataFileName) = imageList[len(imageList) - 1]
    (fname, ftype) = string.split(newestImageDataFileName, '.tif')
    statsFile = fname + '.data.stats'
    twccommon.Log.info('checkRadarPrecip: examining radar stats file %s' % (statsFile,))
    nsRain = {}
    if os.path.isfile(statsFile):
        execfile(statsFile, nsRain, nsRain)
        twccommon.Log.info('checkRadarPrecip: %s rainDensity = %d' % (productString, nsRain['rainDensity']))
    else:
        twccommon.Log.error('checkRadarPrecip: missing radar stats file %s' % (statsFile,))
    if 'rainDensity' in nsRain:
        rainDensity = nsRain['rainDensity']
    else:
        rainDensity = 5
        msg = 'checkRadarPrecip: Error reading stats file: %s. ' % (statsFile,)
        msg += 'Assuming rainDensity > 5 (echoes present).'
        twccommon.Log.warning(msg)
    if rainDensity < 5:
        radarReturns = 0
        twccommon.Log.info('checkRadarPrecip: no rain, so radarReturns set to 0')
    else:
        twccommon.Log.info('checkRadarPrecip: rain echoes found (rainDensity > 5), radarReturns set to 1')
        radarReturns = 1
    return radarReturns
    return


def checkCurrentConditionsPrecip(obsStations=None):
    hasPrecip = 0
    if obsStations == None:
        ob = dsm.defaultedConfigGet('Local_CurrentConditions')
        if ob == None:
            return hasPrecip
        obsStations = ob.obsStation
    obsList = []
    for stn in obsStations:
        obs = dsm.defaultedGet('obs.%s' % (stn,))
        if obs != None:
            obx = twccommon.DefaultedData(obs)
            obsList.append(obx.skyCondition)

    for skyCode in obsList:
        if skyCode != None:
            hasPrecip = wxDataUtil.skyConditionHasPrecip(skyCode)

    twccommon.Log.info('checkCurrentConditionsPrecip=%d' % (hasPrecip,))
    return hasPrecip
    return


def checkTextForecastPrecip(coopId=None):
    hasPrecip = 0
    if coopId == None:
        fcst = dsm.defaultedConfigGet('Local_TextForecast')
        if fcst == None:
            return hasPrecip
        coopId = fcst.coopId
    twccommon.Log.info('NO PRECIP FOR YOU! (checkTextForecast=0)')
    return hasPrecip
    return


_ID = 0
