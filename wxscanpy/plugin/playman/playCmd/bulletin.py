# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: bulletin.py
# Compiled at: 2007-05-14 11:20:55
import wxscan, wxscan.dataUtil, wxscan.BulletinInfo as BulletinInfo, os, time, twc.dsmarshal as dsm, twc.DataStoreInterface as ds, twccommon, twccommon.Log as Log, twc.MiscCorbaInterface, wxscan.RunLog, rendereglobals as rg

DSKEY_ILIST_COUNTY = 'interestlist.county'
KEY_SVRMODE = 'SevereMode'
KEY_SVRMODE_PILS = 'Config.' + dsm.getConfigVersion() + '.severeMode.pilList'
CHANNEL_NAME = 'SystemEventChannel'
_rotationSize = 3
_idleCnt = 0
_interestlist = None
_lastRotation = None
_rotation = None
_lastSvrMode = None

def init(config):
    global _config
    global _interestlist
    global _params
    _config = twccommon.Data()
    _config.__dict__.update(config.__dict__)
    _params = twc.Data()
    _params.bulletinDir = '/usr/twc/domestic/products/ext/bulletin'
    _params.layerName = 'Bulletin'
    _params.layerDepth = 90
    _params.tempDir = 'temp/ext/bulletin'
    _params.shareDir = ['%s' % (_params.bulletinDir,)]
    wxscan.RunLog.init(_config.runlog)
    setCountyInterestList(_interestlist)
    return


def idle():
    global _idleCnt
    if _idleCnt >= 10:
        _idleCnt = 0
        now = time.time()
        changed = 0
        for bulletin in _bulletins.values():
            if now >= bulletin.dispExpiration:
                changed += 1
                Log.info('bulletin expired %s-%s-%s' % (bulletin.pil, bulletin.pilExt, bulletin.county))
                _delBulletin(_bulletins, bulletin.county, bulletin.group)

        if changed > 0:
            _updateBulletinRotation()
    _idleCnt += 1
    return


def setCountyInterestList(il):
    global _bulletins
    global _interestlist
    (_interestlist, _bulletins) = _processNewInterestList(il)
    _updateBulletinRotation()
    return


def set(county, group):
    setList([(county, group)])
    return


def setList(l):
    for (county, group) in l:
        _addBulletin(_interestlist, _bulletins, county, group)

    _updateBulletinRotation()
    return


def cancel(county, group):
    cancelList([(county, group)])
    return


def cancelList(l):
    for (county, group) in l:
        _delBulletin(_bulletins, county, int(group))

    _updateBulletinRotation()
    return


def load():
    dstName = wxscan.buildPresentationScript(_params.bulletinDir, _config.tempDir, 'Misc', 0, 'SevereWeatherCrawl', 0, _params)
    rg.runrsfunction(dstName)
    return


def _processNewInterestList(interestlist=None):
    now = int(time.time())
    try:
        if interestlist == None:
            Log.info('loading bulletin interest list...')
            interestlist = dsm.configGet(DSKEY_ILIST_COUNTY)
        Log.info('searching for already active bulletins...')
        bulletins = BulletinInfo.loadActiveBulletins(interestlist)
        bulls = {}
        try:
            while 1:
                (key, bulletin) = bulletins.popitem()
                if now < bulletin.dispExpiration:
                    Log.info('found active bulletin @ start: %s.%s' % (bulletin.county, bulletin.group))
                    _initBulletin(bulletin)
                    bulls[key] = bulletin

        except:
            pass

        return (interestlist, bulls)
    except KeyError:
        Log.warning('no interest list set for bulletins; none will be displayed')
        return ([], {})

    return


def _split(list, selector):
    data = {}
    for e in list:
        key = selector(e)
        try:
            data[key].append(e)
        except KeyError:
            data[key] = [e]

    return data
    return


def _compareBulletin(l, r):
    if l.primary > r.primary:
        return -1
    if l.primary < r.primary:
        return 1
    if l.priority > r.priority:
        return -1
    if l.priority < r.priority:
        return 1
    if l.issueTime > r.issueTime:
        return -1
    if l.issueTime < r.issueTime:
        return 1
    if l.lastDisplayTime < r.lastDisplayTime:
        return 1
    if l.lastDisplayTime > r.lastDisplayTime:
        return -1
    if l.displaySequence < r.displaySequence:
        return 1
    if l.displaySequence > r.displaySequence:
        return -1
    return 0
    return


def _selectBulletinRotation(bulletins, windowSize):
    if not bulletins:
        return []
    data = _split(bulletins.values(), (lambda e: e.category))
    categories = data.keys()
    categories.sort()
    categories.reverse()
    bull = data[categories[0]]
    bull.sort(_compareBulletin)
    return _debigulate(bull, windowSize)
    return


def _debigulate(rotation, windowSize):
    """Make it where the is no gap in the rotation
    bigger than windowSize that contains only secondary
    counties.
    """
    i = 0
    for i in range(len(rotation)):
        if not rotation[i].primary:
            break

    primaryList = rotation[:i]
    secondaryList = rotation[i:]
    np = len(primaryList)
    ns = len(secondaryList)
    if np == 0:
        return secondaryList
    if ns == 0:
        return primaryList
    if np >= windowSize:
        return primaryList
    res = []
    cnt = windowSize - np
    while len(secondaryList):
        res.extend(primaryList)
        res.extend(secondaryList[:cnt])
        secondaryList = secondaryList[cnt:]

    return res
    return


def _logRotation(rotation, rotationChanged):
    str = 'bulletin rotation'
    if not rotationChanged:
        str = 'unchanged ' + str
    for e in rotation:
        qatext = getattr(e, 'qatext', None)
        str += '|%s-%s-%s' % (e.pil, e.pilExt, e.county)
        if qatext != None:
            str += '-%s' % (qatext,)

    str += '|'
    Log.info(str)
    return


def _setMode(rotation):
    global _lastSvrMode
    spl = dsm.defaultedGet(KEY_SVRMODE_PILS)
    svrMode = len(list(filter((lambda e: e.pil in spl), rotation)))
    if svrMode != _lastSvrMode:
        _lastSvrMode = svrMode
        dsm.set(KEY_SVRMODE, svrMode, 0)
        ds.commit()
        #twc.MiscCorbaInterface.signalEvent(CHANNEL_NAME, KEY_SVRMODE, str(svrMode))
    return


def _updatePresentation(lastRotation, rotation):
    immediate = 1
    _params.immediateReplacement = immediate
    now = time.time()
    _params.bulletins = []
    i = 1
    for e in rotation:
        e.lastDisplayTime = now
        e.displaySequence = i
        i += 1
        _params.bulletins.append(e)

    load()
    return


def _initBulletin(bulletin):
    bulletin.lastDisplayTime = 0
    bulletin.displaySequence = 0
    return


def _addBulletin(interestlist, bulletins, county, group):
    try:
        bulletin = BulletinInfo.loadBulletin(_interestlist[0], county, group)
        _initBulletin(bulletin)
        bulletins[(county, group)] = bulletin
    except BulletinInfo.InvalidBulletin as e:
        Log.warning('invalid bulletin for %s.%d: %s' % (county, group, e))
    except KeyError:
        Log.warning('got a bulletin event for %s.%d; but could not properly load it' % (county, group))
    except IndexError:
        Log.error('BUG - bulletin set but no interest list; contact a developer')

    return


def _delBulletin(bulletins, county, group):
    try:
        del bulletins[(county, group)]
    except KeyError:
        Log.warning('got a bulletin cancellation for a bulletin that is not active: %s.%d' % (county, group))

    return


def _updateBulletinRotation():
    global _lastRotation
    global _rotation
    _rotation = _selectBulletinRotation(_bulletins, _rotationSize)
    rotationChanged = _rotation != _lastRotation
    if rotationChanged:
        _logRotation(_rotation, rotationChanged)
        _setMode(_rotation)
        _updatePresentation(_lastRotation, _rotation)
        _lastRotation = _rotation
    return

