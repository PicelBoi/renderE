# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: wxdata.py
# Compiled at: 2007-01-12 11:33:26
import re, time, types, shutil, twc.dsmarshal, twc.DataStoreInterface, twc.InterestList, twc.MiscCorbaInterface, twccommon, twccommon.Log, domestic.BulletinInfo, os, glob
import domesticpy.plugin.playman.playCmd.pm as pcpm
from xml.sax import make_parser, handler
import nethandler as nh
ds = twc.DataStoreInterface
dsm = twc.dsmarshal
BulletinInfo = domestic.BulletinInfo
CHANNEL_NAME = 'SystemEventChannel'
MAP_ACTIVE_KEY = 'mapcuts.active'
MAP_PENDING_KEY = 'mapcuts.pending'
MAP_FORCE_KEY = 'mapcuts.force'

class IconParserHandler(handler.ContentHandler):

    def __init__(self):
        self._data = {}
        return

    def startElement(self, name, attrs):
        if name == 'record':
            self._data[(str(attrs.get('wxId')), str(attrs.get('night', '0')))] = (str(attrs.get('wxId')), str(attrs.get('movie')), str(attrs.get('sfx_name')), str(attrs.get('night', '0')))
        return


def getTextFcstMultimedia(audioCode):
    sCodeRe = re.compile('S([0-9]{4})([0-9])')
    for audioElement in audioCode.split(':'):
        sCodeMatch = sCodeRe.match(audioElement)
        if sCodeMatch:
            sCode = sCodeMatch.groups()[0]
            sDayPart = sCodeMatch.groups()[1]
            if sDayPart in ['2', '4']:
                sDayPart = '1'
            else:
                sDayPart = '0'
            try:
                sCode = str(int(sCode))
            except ValueError:
                pass
            else:
                break
    else:
        return (None, None)

    parser = make_parser()
    iconHandler = IconParserHandler()
    parser.setContentHandler(iconHandler)
    fname = '/media/mappings/textForecast/AnimatedIcons.xml'
    if not os.path.exists(fname):
        fname = nh.requestNetAssetExt('/media/mappings/textForecast/AnimatedIcons.xml')
    parser.parse(fname)
    data = iconHandler._data
    try:
        mapping_element = data[(sCode, sDayPart)]
    except KeyError:
        if sDayPart == '1':
            try:
                mapping_element = data[(sCode, '0')]
            except KeyError:
                mapping_element = (None, None, None, None)

        else:
            mapping_element = (None, None, None, None)

    return (mapping_element[1], mapping_element[2])
    return


def getBulletinInterestList(ugc):
    cl = getUGCInterestList(ugc, 'county')
    zl = getUGCInterestList(ugc, 'zone')
    return cl + zl
    return


def getUGCInterestList(ugc, type):
    locs = []
    mo = _ugcRegex.search(ugc)
    while mo != None:
        (start, end) = mo.span()
        sl = ugc[start:end]
        ugc = ugc[end:]
        locs.extend(_parseUGCStateList(sl))
        mo = _ugcRegex.search(ugc)

    il = _getInterestList(type)
    locs = list(filter((lambda e: e in il), locs))
    return locs
    return


def setDailyRec(loc, data, obsTimeT):
    currTemp = getattr(data, 'temp', None)
    if currTemp:
        twccommon.Log.debug('currTemp = %d' % currTemp)
        dailyRec = twc.Data(currHighTemp=currTemp, currLowTemp=currTemp)
        save = 0
        try:
            dkey = 'daily.%s.recordTemps' % loc
            dailyRec = dsm.get(dkey)
            if currTemp > dailyRec.currHighTemp:
                save = 1
                dailyRec.currHighTemp = currTemp
            if currTemp < dailyRec.currLowTemp:
                save = 1
                dailyRec.currLowTemp = currTemp
        except:
            save = 1

        if save == 1:
            (y, m, d, H, M, S, wd, jd, dst) = time.localtime(obsTimeT)
            midnight = time.mktime((y, m, d + 1, 0, 0, 0, 0, 0, -1))
            dsm.set(dkey, dailyRec, int(midnight))
    return


def setData(loc, type, data, expiration, update=0):
    if type == 'obs':
        setDailyRec(loc, data, expiration - 75 * 60)
    key = '%s.%s' % (type, str(loc))
    _setData(key, data, expiration, update)
    twccommon.Log.debug('set %s' % (key,))
    if type == 'hdln':
        log_msg = 'set hdln for location %s' % loc
        twccommon.Log.info(log_msg)
        modifiedHeadlines = []
        matchCategories = ((4, 'INLAND HURRICANE WATCH', re.compile('INLAND HURRICANE WATCH'), 'HURRICANE WATCH'), (3, 'HURRICANE WATCH', re.compile('(?<!INLAND )HURRICANE WATCH'), 'HURRICANE WATCH'), (2, 'INLAND HURRICANE WARNING', re.compile('INLAND HURRICANE WARNING'), 'HURRICANE WARNING'), (1, 'HURRICANE WARNING', re.compile('(?<!INLAND )HURRICANE WARNING'), 'HURRICANE WARNING'))
        for i in range(len(data.headlines)):
            headline = data.headlines[i]
            compareHeadline = (' ').join(headline.upper().split())
            matchAppender = []
            for (v, match, headlineRe, abb) in matchCategories:
                if headlineRe.search(compareHeadline):
                    matchAppender = [(v, i, abb, headline)]

            modifiedHeadlines += matchAppender

        modifiedHeadlines.sort()
        if len(modifiedHeadlines) > 0:
            d = twc.Data(header=modifiedHeadlines[0][2], message=modifiedHeadlines[0][3])
            dsm.set('hurricaneStatement', d, expiration)
            ds.commit()
        else:
            try:
                dsm.remove('hurricaneStatement')
                ds.commit()
            except KeyError:
                pass

    return


def setDaypartData(loc, type, data, validTime, numDayparts, expiration, update=0):
    (Y, M, D, h, m, s, wday, day, dst) = time.localtime(validTime)
    window = 24 / numDayparts
    h = h / window * window
    validTime = time.mktime((int(Y), int(M), int(D), int(h), 0, 0, int(wday), int(day), -1))
    key = '%s.%s.%d' % (type, str(loc), validTime)
    _setData(key, data, expiration, update)
    twccommon.Log.debug('set %s' % (key,))
    return


def setBulletin(loc, data, expiration):
    setBulletins([(loc, data, expiration)])
    return


def setBulletins(blist):
    setlist = []
    for (loc, data, expiration) in blist:
        info = BulletinInfo.getBulletinProperties(data.pil, data.pilExt)
        il = _getInterestList('county')
        if loc in il[1:]:
            if not info.multicountied:
                continue
        data.county = loc
        data.expiration = expiration
        setlist.append((loc, info.group))
        which = '%s.%d' % (loc, info.group)
        key = 'bulletin.' + which
        dsm.set(key, data, expiration, 0)
        key = 'bulletin.lastIssue.%s' % data.pil
        dsm.set(key, data.issueTime, 0, 0)
        key = 'bulletin.lastIssue.%s%s' % (data.pil, data.pilExt)
        dsm.set(key, data.issueTime, 0, 0)
        ds.commit()

    if len(setlist):
        _signalRPC('playman.playCmd.bulletin.setList', (setlist,))
        twccommon.Log.info('set bulletins %s' % setlist)
    return


def cancelBulletin(loc, pil, pilExt):
    cancelBulletins([(loc, pil, pilExt)])
    return


def cancelBulletins(l):
    setlist = []
    for (loc, pil, pilExt) in l:
        info = BulletinInfo.getBulletinProperties(pil, pilExt)
        which = '%s.%d' % (loc, info.group)
        key = 'bulletin.%s' % (which,)
        try:
            dsm.remove(key)
            ds.commit()
            setlist.append((loc, info.group))
        except KeyError:
            pass

    if len(setlist):
        _signalRPC('playman.playCmd.bulletin.cancelList', (setlist,))
        twccommon.Log.info('cancel bulletins %s' % setlist)
    return


def setImageData(type, fname):
    twccommon.Log.info('setImageData(%s, %s)' % (type, fname))
    (imgType, imgLoc) = type.split('.')
    if imgType in ['map', 'radar', 'satellite', 'radarSatellite']:
        fnName = 'execd.imageProc.%s.process' % imgType
    else:
        fnName = 'execd.imageProc.image.process'
    _signalRPC(fnName, (imgType, imgLoc, fname))
    twccommon.Log.info('set %s image: %s' % (type, fname))
    return

import mapcut
def setMapCut(type):
    mapcut.process(type)
    twccommon.Log.info('set map cut: %s' % type)
    return


def setMapData(key, data, expiration, update=0):
    mapForceKey = MAP_FORCE_KEY
    try:
        mapCutRequired = dsm.get(mapForceKey)
    except:
        mapCutRequired = 0

    mapDataKey = key + '.MapData'
    try:
        old = twc.DefaultedData(dsm.get(mapDataKey))
        for (k, v1) in data.__dict__.items():
            v2 = getattr(old, k, None)
            if v2 != v1:
                mapCutRequired = 1
                break

    except:
        mapCutRequired = 1

    if mapCutRequired:
        pendingKey = MAP_PENDING_KEY
        try:
            mapPendingList = dsm.get(pendingKey)
        except KeyError:
            mapPendingList = []
        else:
            if mapPendingList.count(key) < 1:
                mapPendingList.append(key)
                dsm.set(pendingKey, mapPendingList, 0)
                ds.commit()
            twccommon.Log.info('set %s' % (mapDataKey,))
            _setData(mapDataKey.replace("Config.0", "Config.1"), data, expiration, update)
            setMapCut(key.replace("Config.0", "Config.1"))
    return


def setInterestList(*args):
    if len(args) == 3:
        ilType, configVersion, val = args
    elif len(args) == 2:
        ilType, val = args
        configVersion = 1
    if type(val) != list:
        raise RuntimeError('invalid interest list; should be a list of strings')
    key = 'Config.%s.interestlist.%s' % (configVersion, ilType)
    try:
        old = dsm.get(key)
    except KeyError:
        old = None

    if old != val:
        dsm.set(key, val, 0)
        ds.commit()
        twccommon.Log.info('setting %s to: %s' % (key, val))
        twc.InterestList.getInterestList(ilType, updateCache=1)
        if ilType in _ilistSignalMap:
            for fnName in _ilistSignalMap[ilType]:
                _signalRPC(fnName, (val,))

    return


def setTimeZone(timezone):
    twccommon.Log.info('setting timezone to: %s' % timezone)
    #shutil.copyfile('/usr/share/zoneinfo/%s' % timezone, '/etc/localtime')
    return


def installPackage(pkg, instPath):
    _signalRPC('execd.ipackage.install', (pkg, instPath))
    return


def installMediaPack(pack, replace):
    _signalRPC('execd.mediapack.install', (pack, replace))
    return


def getMediaPackVersion(pack):
    version = None
    versionFile = '/media/%s.version' % (pack,)
    if os.path.exists(versionFile):
        try:
            fd = open(versionFile, 'r')
            version = fd.readline()
            version = version[:-1]
            fd.close()
        except:
            twccommon.Log.warning('getMediaPackVersion: Error reading version file: %s.' % (versionFile,))

    else:
        twccommon.Log.info('getMediaPackVersion: Pack %s not installed.' % (pack,))
    return version
    return


def shutdown():
    reboot()
    return


def reboot():
    twccommon.Log.info('Shut down requested! Rebooting...')
    #os.system('shutdown -r now')
    return


def restart():
    twccommon.Log.info('Restart requested! Killing processes...')
    #os.system('killall receiverd')
    return


def loadClock():
    return



if twc.personality == "Perris":
    def loadData(prodType, argData):
        if prodType == 'tag':
            id = 'tag-%s' % argData.id
            duration = argData.duration * 30 + argData.durationFrames
            scheds = "[DynamicSchedule('Tag')]"
            params = twccommon.Data(mediaNum=argData.mediaNum)
            _pmLoad(id, duration, argData.expire, scheds, params)
        elif prodType == 'localAvail':
            id = 'localAvail-%s' % argData.id
            duration = 68
            durationFrames = 0
            duration = duration * 30 + durationFrames
            scheds = "[DynamicSchedule('LocalAvail')]"
            params = twccommon.Data()
            _pmLoad(id, duration, argData.expire, scheds, params)
        else:
            _runPlayCmd(prodType, 'load', argData)
        return
elif twc.personality == "FlatRock":
    def loadData(prodType, argData):
        global _ldlIdList
        if prodType == 'tag':
            id = 'tag-%s' % argData.id
            duration = argData.duration * 30 + argData.durationFrames
            scheds = "[DynamicSchedule('Tag')]"
            params = twccommon.Data(mediaNum=argData.mediaNum)
            _pmLoad(id, duration, argData.expire, scheds, params)
        elif prodType == 'localAvail':
            id = 'localAvail-%s' % argData.id
            duration = 68
            durationFrames = 0
            duration = duration * 30 + durationFrames
            scheds = "[DynamicSchedule('LocalAvail')]"
            params = twccommon.Data()
            _pmLoad(id, duration, argData.expire, scheds, params)
        elif prodType == 'SNUP':
            if len(argData.media1) > 0:
                displayMode = argData.media1
            else:
                displayMode = None
            _ldlIdList.append(argData.id)
            _runPlayCmd('ldl', 'load', argData.id, 1, displayMode)
        elif prodType == 'SNDN':
            pass
        elif prodType == 'local':
            _runPlayCmd(prodType, 'load', argData)
        return


def runData(prodType, argData):
    if prodType == 'tag':
        id = 'tag-%s' % argData.id
        _pmRun(id, argData.time, argData.frame)
    elif prodType == 'localAvail':
        id = 'localAvail-%s' % argData.id
        _pmRun(id, argData.time, argData.frame)
    else:
        _runPlayCmd(prodType, 'run', argData)
    return


def processHeartbeat(**kw):
    v = _getDictVal(kw, 'time')
    if v != None:
        (sec, millisec) = v
        #_setTime(sec, millisec)
    dispMode = _getDictVal(kw, 'displayMode')
    if dispMode != '*':
        _processStateVal(kw, 'displayMode')
    _processStateVal(kw, 'sensorState')
    return


def setTime(sec, millisec):
    return


def setTrafficIncidents(path):
    twccommon.Log.info('Traffic: setTrafficIncidents: path %s.' % (path,))
    _signalRPC('execd.traffic.processIncidents', (path,))
    return


def setTrafficMap(path, hasData):
    if hasData:
        twccommon.Log.info('Traffic: setTrafficMap: path %s.' % path)
    else:
        twccommon.Log.info('Traffic: set Temp Unavail Traffic Map: path %s.' % path)
    return


def changeIrdChannel(channelNumber):
    _signalRPC('execd.altFeed.channelChange', (channelNumber,))
    return


DELAYED_CHANNEL_CHANGE = 0
IMMEDIATE_CHANNEL_CHANGE = 1

def setIrdChannel(channelNumber, switchMethod=DELAYED_CHANNEL_CHANGE):
    if switchMethod == IMMEDIATE_CHANNEL_CHANGE:
        twccommon.Log.info('AltFeed: IMMEDIATE ird channel change requested to channel %s.' % (channelNumber,))
        changeIrdChannel(channelNumber)
    else:
        _signalRPC('execd.altFeed.channelChangeRequest', (channelNumber,))
        twccommon.Log.info('AltFeed: ird channel change requested: Channel %s.' % (channelNumber,))
    return


def system(cmd):
    _signalRPC('execd.system', (cmd,))
    return


def toggleNationalLDL(activate, displayMode=None):
    id = 0
    _runPlayCmd('ldl', 'toggleNationalLDL', id, activate, displayMode)
    return


_ugcRegex = re.compile('[A-Z]{2}[ZC]([0-9]{3}[\\->])*[0-9]{3}')
_getInterestList = twc.InterestList.getInterestList
_ilistSignalMap = {'climId': ['playman.init.setClimIds'], 'county': ['playman.playCmd.bulletin.setCountyInterestList']}

def _setData(key, data, expiration, update):
    dsm.set(key, data, expiration, update)
    ds.commit()
    return

def _rsetData(key, data, expiration, update):
    dsm.rset(key, data, expiration, update)
    ds.rcommit()
    return

def _signalEvent(type, value):
    twc.MiscCorbaInterface.signalEvent(CHANNEL_NAME, type, value)
    return


def _signalRPC(rpcName, args):
    #twc.MiscCorbaInterface.signalEvent(CHANNEL_NAME, rpcName, repr(args))
    fullname = "domesticpy.plugin."+rpcName
    #this is the single unholiest function i have ever written.
    fn = fullname.split(".")[-1]
    di = __import__(".".join(fullname.split(".")[:-1]), fromlist=[fn])
    #print(vars(di))
    di.__dict__[fn](*args)
    return


def _parseUGCStateList(ugc):
    state = ugc[:3]
    ugc = ugc[3:]
    sp = ugc.split('-')
    locs = []
    for loc in sp:
        pos = loc.find('>')
        if pos == -1:
            locs.append('%s%03d' % (state, int(loc)))
        start = int(loc[:pos])
        end = int(loc[pos + 1:])
        for i in range(start, end + 1):
            locs.append('%s%03d' % (state, i))

    return locs
    return


def _getDictVal(dict, key):
    val = None
    try:
        val = dict[key]
    except KeyError:
        pass

    return val
    return


def _processStateVal(kw, valName):
    v = _getDictVal(kw, valName)
    if v == None:
        return
    dsv = dsm.defaultedGet(valName, None)
    if v == dsv:
        return
    _setData(valName, v, 0, 0)
    if valName == 'sensorState':
        toggleNationalLDL(v)
    return


def _pmLoad(id, duration, expire, scheds, params):
    args = (id, duration, expire, scheds, params)
    twccommon.Log.info('signalling load of %s (%s, %s, %s, %s)' % args)
    pcpm.load(*args)
    return


def _pmRun(id, startTime, startFrame):
    args = (id, startTime, startFrame)
    twccommon.Log.info('signalling run of %s (%s, %s)' % args)
    pcpm.run(*args)
    return


def _runPlayCmd(prodType, playCmd, *params):
    twccommon.Log.info('signalling %s of %s %s' % (playCmd, prodType, str(params)))
    print('signalling %s of %s %s' % (playCmd, prodType, str(params)))
    fnName = 'playman.playCmd.%s.%s' % (prodType, playCmd)
    _signalRPC(fnName, params)
    return


