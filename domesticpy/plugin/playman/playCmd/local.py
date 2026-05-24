# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: local.py
# Compiled at: 2007-01-12 11:33:37
import domestic, domestic.wxdata, domestic.BulletinInfo as BulletinInfo, os, copy, time, glob, twc.EventLog as EventLog, twccommon, twccommon.Log as Log, twccommon.PluginManager, twc.dsmarshal as dsm, twc.MiscCorbaInterface
import domesticpy.plugin.playman.playCmd.pm as pcpm
import rendereglobals as rg
import tscard
from functools import cmp_to_key
CHANNEL_NAME = 'SystemEventChannel'
TAG_DELAY = 50

def init(config):
    global _config
    global _params
    _config = twccommon.Data()
    _config.__dict__.update(config.__dict__)
    _config.root = '/usr/twc/domestic/products/pm/local'
    _config.shareDir = '%s/share' % (_config.root,)
    _config.defaultPlaylistGroup = 'DefaultUS'
    _params = twccommon.Data()
    _params.root = _config.root
    _params.tempDir = rg.newjoin(os.environ["RENDEREROOT"], "temp", "local")
    os.makedirs(_params.tempDir, exist_ok=True)
    return

def load(argData):
    id = argData.id
    pres = _params.clone()
    pres.update(argData)
    pres.expireTime = time.time() + pres.expire / 30
    _presentations[id] = pres
    pres.startTime = time.time()
    pres.mediaNum = argData.logoId
    if twc.personality == "FlatRock":
        pres.duration = argData.duration * 30 + argData.durationFrames
    pres.channelChangeRequest = 0
    pres.suppressLocal = 0
    pres.alternateFeedActive = 0
    irdChannel = dsm.defaultedConfigGet('irdChannelChangeRequest')
    if _channelChangeNeeded(irdChannel):
        pres.channelChangeRequest = 1
        pres.irdChannel = irdChannel
        Log.info('AltFeed: IRD channel change requested. Channel will change to %s during this local.' % (irdChannel,))
    if pres.vbid != '000':
        pres.alternateFeedActive = 1
    interestList = dsm.defaultedConfigGet('interestlist.vbid')
    if interestList == None:
        interestList = []
    if pres.vbid in interestList:
        pres.suppressLocal = 1
        Log.info('AltFeed: Upcoming local will be suppressed to view an alternate feed. VBID = %s' % (pres.vbid,))
    if pres.channelChangeRequest == 1 and pres.suppressLocal == 1:
        pres.suppressLocal = 0
        Log.warning('AltFeed: IRD channel change request NOT received in time. Rendering a normal local with channel change.')
    pres.defaultGroup = _config.defaultPlaylistGroup
    pres.group = dsm.defaultedConfigGet('PlaylistOverride', pres.defaultGroup)
    
    if twc.personality == "Perris":
        try:
            (pres.duration, pres.version, pres.squeezeBack) = _flavorMap[pres.flavor]
            pres.override = 0
        except Exception:
            pres.override = 1
            pres.duration = argData.duration
            pres.version = 0
            pres.squeezeBack = 0
    elif twc.personality == "FlatRock":
        try:
            flavorMap = dsm.defaultedConfigGet('FlavorMap')
            for (key, value) in flavorMap:
                if pres.flavor == key:
                    (pres.version, pres.squeezeBack) = value
                    break

            pres.override = 0
        except Exception:
            pres.override = 1
            pres.duration = argData.duration * 30 + argData.durationFrames
            pres.version = 0
            pres.squeezeBack = 0

    pres.durationSeconds = (pres.duration // 30)
    pres.hasLdl = not pres.squeezeBack
    print('has ldl')
    if pres.hasLdl:
        (pres.ldlBulletins, pres.ldlWarningMode, pres.activeWarnings) = _activeBulletins()
        pres.nationalLdl = 0
        pres.lasCrawlText = _getLasCrawlText()
        print('LAS CRAWL TEXT')
    pres.bkgAudioFilename = None
    if not tscard.SDI_URL:
        pres.bkgAudioFilename = _getBkgAudioFilename()
    #if pres.channelChangeRequest == 1 or pres.alternateFeedActive == 1:
    #    pres.bkgAudioFilename = _getBkgAudioFilename()
    scheds = _selectSchedule(pres)
    if scheds != None:
        _load(id, pres.duration, pres.expire, scheds, pres)
    return


def run(argData):
    id = argData.id
    pres = _presentations[id]
    del _presentations[id]
    rtime = getattr(argData, 'time', 0)
    frame = getattr(argData, 'frame', 0)
    pres.startTime = rtime
    pres.startFrame = frame
    _run(id, pres.startTime, pres.startFrame, pres)
    _cull()
    if pres.channelChangeRequest == 1:
        domestic.wxdata.changeIrdChannel(pres.irdChannel)
    return


_presentations = {}
_starId = dsm.defaultedConfigGet('starId', None)
_ldlState = None
_schedOverrideTmpl = "[\n    DynamicSchedule('%(flavor)s'),\n    StaticSchedule('%(flavor)s'),\n]"
_schedLdlOnlyTmpl = "[\n    DynamicSchedule('Ldl.ldl1'),\n    StaticSchedule('FallbackLdl%(durationSeconds)s'),\n]"
_schedGroupOverrideTmpl = "[\n    DynamicSchedule('%(group)s.%(durationSeconds)s.%(version)s'),\n    DynamicSchedule('%(defaultGroup)s.%(durationSeconds)s.%(version)s'),\n    CompositeSchedule([\n        StaticSchedule('Fallback%(durationSeconds)s'),\n        StaticSchedule('FallbackLdl%(durationSeconds)s'),\n    ]),\n    StaticSchedule('Fallback%(durationSeconds)s'),\n]"
_schedGroupDefaultTmpl = "[\n    DynamicSchedule('%(defaultGroup)s.%(durationSeconds)s.%(version)s'),\n    CompositeSchedule([\n        StaticSchedule('Fallback%(durationSeconds)s'),\n        StaticSchedule('FallbackLdl%(durationSeconds)s'),\n    ]),\n    StaticSchedule('Fallback%(durationSeconds)s'),\n]"
_schedNoFallbackTmpl = "[\n    DynamicSchedule('%(defaultGroup)s.%(durationSeconds)s.%(version)s'),\n]"
_schedNoFallbackGroupOverrideTmpl = "[\n    DynamicSchedule('%(group)s.%(durationSeconds)s.%(version)s'),\n    DynamicSchedule('%(defaultGroup)s.%(durationSeconds)s.%(version)s'),\n]"
_flavorMap = {'S': (57 * 30 + 20, 0, 1), 'D': (60 * 30, 0, 0), 'E': (60 * 30, 1, 0), 'K': (90 * 30, 0, 0), 'O': (90 * 30, 1, 0), 'N': (120 * 30, 0, 0), 'L': (120 * 30, 1, 0), 'M': (120 * 30, 2, 0), 'T': (140 * 30, 0, 0)}

forcelascrawl = True

def _getLasCrawlText():
    print('get lascrawl')
    global _ldlState
    params = dsm.defaultedConfigGet('Ldl_LASCrawl')
    if params == None or params.serialNum == None or params.crawls == None:
        print('NO crawls valid at this time')
        return None
    if _ldlState == None or _ldlState.serialNum != params.serialNum:
        times = [0] * len(params.crawls)
        _ldlState = twccommon.Data(serialNum=params.serialNum, lastUsedTimes=times)
    i = 0
    now = int(time.time())
    validList = []
    for crawl in params.crawls:
        try:
            (startTime, endTime, displayTimes, text) = crawl
            if (now >= startTime and now <= endTime) or forcelascrawl:
                h = time.localtime(now)[3]
                for (sdh, edh) in displayTimes:
                    if sdh <= edh:
                        match = (h in range(sdh, edh + 1))
                    else:
                        match = (h not in range(edh + 1, sdh))
                    if match:
                        validList.append((i, _ldlState.lastUsedTimes[i], text))

        except:
            print('There is an error in the configuration                 for crawl number %d' % (i + 1))
            continue

        i += 1

    if len(validList) == 0:
        print('NO crawls valid at this time')
        print('Reason: validList')
        return None
    print('crawls valid at this time: %s' % (map((lambda e: e[0]), validList),))
    validList.sort(key=cmp_to_key(lambda a, b: twccommon.compare(a[1], b[1])))
    (i, lut, text) = validList[0]
    text = text
    print('crawl %d selected because it is least recently viewed' % (i,))
    _ldlState.lastUsedTimes[i] = now
    return text
    return

import math
import random
def _getBkgAudioFilename():
    files = glob.glob(rg.newjoin(os.environ["RENDEREROOT"], 'bgm', '*'))
    print(files)
    files.sort()
    numFiles = len(files)
    if numFiles == 0:
        return None
    else:
        return random.choice(files)
        (y, m, d, H, M, S, dw, jd, dst) = time.gmtime()
        ndx = ((m + 5) / 10 + H + dw) % numFiles
        return files[math.floor(ndx)]
    return


def _activeBulletins():
    counties = dsm.defaultedConfigGet('interestlist.county')
    if counties is not None:
        bulletins = BulletinInfo.loadActiveBulletins(counties)
    else:
        bulletins = {}
    activeWarnings = 0
    for (key, val) in bulletins.copy().items():
        if val.category == BulletinInfo.CAT_WARNING:
            activeWarnings = 1
        if val.ldl == 0:
            del bulletins[key]

    hurricaneStatement = dsm.defaultedGet('hurricaneStatement')
    ldlWarningMode = 0
    if len(bulletins) > 0:
        ldlWarningMode = 1
    elif hurricaneStatement != None:
        ldlWarningMode = 1
    return [bulletins, ldlWarningMode, activeWarnings]
    return


def _channelChangeNeeded(channel):
    if channel == None:
        return 0
    lastRequestedChannel = dsm.defaultedConfigGet('irdLastRequestedChannel')
    if channel == lastRequestedChannel:
        return 0
    irdSlave = dsm.defaultedConfigGet('irdSlave')
    if irdSlave == None or irdSlave == '0':
        return 1
    return


def _cull():
    culled = []
    now = time.time()
    for (key, val) in _presentations.items():
        if now >= val.expireTime:
            culled.append(key)

    for key in culled:
        Log.info('removing expired presentation %s' % key)
        del _presentations[key]

    return


def _selectSchedule(pres):
    scheds = None
    if pres.override:
        scheds = _schedOverrideTmpl % pres.__dict__
    elif pres.suppressLocal:
        Log.info('AltFeed: Suppressing local %s / alternate feed %d frames' % (pres.flavor, pres.duration))
        if pres.hasLdl:
            scheds = _schedLdlOnlyTmpl % pres.__dict__
    elif pres.squeezeBack:
        if pres.group == pres.defaultGroup:
            scheds = _schedNoFallbackTmpl % pres.__dict__
        else:
            scheds = _schedNoFallbackGroupOverrideTmpl % pres.__dict__
    elif pres.group == pres.defaultGroup:
        scheds = _schedGroupDefaultTmpl % pres.__dict__
    else:
        scheds = _schedGroupOverrideTmpl % pres.__dict__
    return scheds
    return


def _load(id, duration, expire, scheds, params):
    #_signalRPC('playman.playCmd.pm.load', (id, duration, expire, scheds, params))
    pcpm.load(id, duration, expire, scheds, params)
    return


def _run(id, startTime, startFrame, params=None):
    #_signalRPC('playman.playCmd.pm.run', (id, startTime, startFrame, params))
    pcpm.run(id, startTime, startFrame, params)
    return


def _signalRPC(rpcName, args):
    return

