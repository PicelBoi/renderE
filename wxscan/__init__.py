# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: __init__.py
# Compiled at: 2007-04-27 10:00:47
import os, twc, twc.dsmarshal as dsm, twc.psp, twccommon, string, twcWx.dataUtil as wxDataUtil
from wxscan import dataUtil

def execfile(filename, globa, loca):
    with open(filename, "r", encoding="windows-1252") as f:
        exec(compile(f.read(), filename, 'exec'), globa, loca)

def checkRadarPrecip(RadarProductName, location='us', imageList=None):
    """Checks for significant radar returns (precip) in a given image
       list. If a list isn't provided, it will look up the latest images
       on disk. If a list IS provided, then we ignore the ProductName and
       ConfigSet. This method assumes that the imageList passed in only
       contains valid images and is already sorted from OLDEST to NEWEST."""
    radarReturns = 0
    imageRoot = '/twc/data/volatile/images/radar/%s.cuts/' % location
    productString = 'Config.' + dsm.getConfigVersion() + '.' + RadarProductName
    if imageList == None:
        imageList = dataUtil.getValidFileList(dataPath=imageRoot, prefix=productString, suffix='*[0-9].tif', startTimeNdx=3, endTimeNdx=4, sortIndex=3)
    if len(imageList) == 0:
        twccommon.Log.warning('checkRadarPrecip: no valid images found for %s.' % (productString,))
        return radarReturns
    (issuetime, newestImageDataFileName) = imageList[len(imageList) - 1]
    (fname, ftype) = string.split(newestImageDataFileName, '.tif')
    statsFile = fname + '.data.index'
    twccommon.Log.info('checkRadarPrecip: examining radar index file %s' % (statsFile,))
    nsRain = {}
    if os.path.isfile(statsFile):
        execfile(statsFile, nsRain, nsRain)
    else:
        twccommon.Log.error('checkRadarPrecip: missing radar index file %s' % (statsFile,))
    if nsRain.has_key('loopRainDensity'):
        loopRainDensity = nsRain['loopRainDensity']
        twccommon.Log.info('checkRadarPrecip: %s loopRainDensity = %d' % (productString, loopRainDensity))
    else:
        loopRainDensity = 5
        msg = 'checkRadarPrecip: Error reading loopRainDensity from index file: %s. ' % (statsFile,)
        msg += 'Assuming loopRainDensity > 5 (echoes present).'
        twccommon.Log.warning(msg)
    if nsRain.has_key('maxPrecipType'):
        maxPrecipType = nsRain['maxPrecipType']
        twccommon.Log.info('checkRadarPrecip: %s maxPrecipType = %d' % (productString, maxPrecipType))
    else:
        maxPrecipType = 3
        msg = 'checkRadarPrecip: Error reading maxPrecipType from index file: %s. ' % (statsFile,)
        msg += 'Assuming maxPrecipType = 3 (winter colors present).'
        twccommon.Log.warning(msg)
    radarReturns = 1
    if loopRainDensity < 5:
        twccommon.Log.info('checkRadarPrecip: no rain, so radarReturns set to 0')
        radarReturns = 0
    else:
        twccommon.Log.info('checkRadarPrecip: rain echoes found (loopRainDensity > 5), radarReturns set to 1')
    winterColors = 1
    if maxPrecipType < 2:
        twccommon.Log.info("checkRadarPrecip: either 'no precip' or 'rain' detected")
        winterColors = 0
    else:
        twccommon.Log.info('checkRadarPrecip: mixed precip or snow detected')
    return (radarReturns, winterColors)
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


def getPkgAttribs(package, packageInst, default=None):
    keys = _fmtAttribKeys(_pkgKeyTemplates, package=package, packageInst=packageInst)
    attrs = _getAttribList(keys, default)
    attrs.package = package
    attrs.packageInst = packageInst
    return attrs
    return


def getProdAttribs(package, packageInst, product, productInst, pkgAttribs):
    keys = _fmtAttribKeys(_prodKeyTemplates, package=package, packageInst=packageInst, product=product, productInst=productInst)
    attrs = _getAttribList(keys, pkgAttribs)
    attrs.package = package
    attrs.packageInst = packageInst
    attrs.product = product
    attrs.productInst = productInst
    return attrs
    return


def getAttribs(params, default=None):
    keys = _pkgKeyTemplates + _prodKeyTemplates
    keys = _fmtAttribKeys(keys, **params.__dict__)
    attrs = _getAttribList(keys, default)
    return attrs
    return
import nethandler

def buildPresentationScript(srcDir, dstDir, pkgName, pkgInst, prod, prodInst, extraParams=None):
    ns = {}
    params = twc.Data()
    ns['params'] = params
    if extraParams:
        params.__dict__.update(extraParams.__dict__)
    params.package = pkgName
    params.packageInst = pkgInst
    params.product = prod
    params.productInst = prodInst
    srcName = srcDir + '/' + prod + '.rs'
    f = open(nethandler.requestNetAssetExt(srcName), 'r')
    page = f.read()
    f.close()
    page = twc.psp.evalRenderScript(page, ns, getattr(params, 'shareDir', []))
    (dstName, f) = tmpFile(dstDir)
    f.write(page)
    f.close()
    return dstName
    return


def tmpFile(dir):
    global _ID
    fname = '%s/%d.rsc' % (dir, _ID)
    f = open(fname, 'w')
    _ID += 1
    return (fname, f)
    return


def writePid(pidFileName):
    f = open(pidFileName, 'w')
    pid = os.getpid()
    f.write('%d\n' % pid)
    f.close()
    return


_ID = 0
_pkgKeyTemplates = ['default', '%(package)s', '%(package)s.%(packageInst)s']
_prodKeyTemplates = [16, 17, 18, 19, 20]

def _fmtAttribKeys(keys, **kw):
    skeys = []
    for key in keys:
        try:
            skeys.append(key % kw)
        except KeyError:
            pass

    return skeys
    return


def _getAttribList(keys, default=None):
    attribList = []
    for key in keys:
        try:
            attribList.append(dsm.configGet(key))
        except:
            pass

    return twccommon.mergeStructs(attribList, default)
    return

