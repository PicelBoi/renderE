# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: bulletin.py
# Compiled at: 2007-01-12 11:33:37
import domestic, domestic.dataUtil, domestic.BulletinInfo, os, time, twc.dsmarshal, twc.DataStoreInterface, twccommon, twccommon.Log
from functools import cmp_to_key
ds = twc.DataStoreInterface
dsm = twc.dsmarshal
BulletinInfo = domestic.BulletinInfo
Log = twccommon.Log
BULLETIN_LAYER_ID = 'BullLayer'
DSKEY_CRAWL_ACTIVE = 'bulletin.active'
DSKEY_ILIST_COUNTY = 'interestlist.county'
_rotationSize = 3
_idleCnt = 0
_interestlist = None
_lastRotation = None
_rotation = None
_crawlActive = 0
_firstLoad = 1

def init(config):
    global _config
    global _interestlist
    global _params
    _config = twccommon.Data()
    _config.__dict__.update(config.__dict__)
    Log.info('initializing bulletin plugin')
    _params = twccommon.Data()
    active = dsm.defaultedGet(DSKEY_CRAWL_ACTIVE, 1)
    if active:
        _activate(1)
    setCountyInterestList(_interestlist)
    return


def idle():
    global _idleCnt
    if _idleCnt == 10:
        _idleCnt = 0
        now = int(time.time())
        changed = 0
        bc = _bulletins.copy() #prevent issues caused by expiring
        for bulletin in bc.values():
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


def getPlaylistName():
    playlistName = 'Bulletin.bulletin1'
    playlistOverride = dsm.defaultedConfigGet('BulletinPlaylistOverride')
    if playlistOverride:
        playlistName = 'Bulletin.%s' % playlistOverride
    return playlistName
    return

import domesticpy.plugin.playman.playCmd.pm as pm
def load():
    global _crawlActive
    global _firstLoad
    id = BULLETIN_LAYER_ID
    bulletinCrawl = []
    for bulletin in _params.bulletins:
        crawlInfo = twccommon.Data()
        crawlInfo.pil = bulletin.pil
        crawlInfo.pilExt = bulletin.pilExt
        crawlInfo.headline = bulletin.headline
        crawlInfo.text = bulletin.text
        crawlInfo.color = bulletin.color
        crawlInfo.beeps = bulletin.beeps
        bulletinCrawl.append(crawlInfo)

    params = twccommon.Data()
    params.bulletinCrawl = bulletinCrawl
    params.immediateReplacement = _params.immediateReplacement
    if twc.personality == "Watt":
        params.changeType = _params.changeType
    params.activate = _crawlActive
    params.firstLoad = _firstLoad
    params.bulletinActive = 0
    if len(bulletinCrawl) > 0:
        params.bulletinActive = 1
    now = int(time.time())
    expire = 0
    for bulletin in _params.bulletins:
        if bulletin.dispExpiration > expire:
            expire = bulletin.dispExpiration

    duration = expire - now
    if duration < 0:
        duration = 1
    durationFrames = duration * 30
    pmDuration = durationFrames
    pmExpire = now + duration
    schedules = "[DynamicSchedule('%s')]" % (getPlaylistName(),)
    pm.load(id, pmDuration, pmExpire, schedules, params)
    pm.run(id, 0, 0)
    _firstLoad = 0
    return


def run(activate):
    activate = int(activate)
    if activate == _crawlActive:
        if activate:
            Log.info('bulletin layer already activated')
        else:
            Log.info('bulletin layer already deactivated')
        return
    id = BULLETIN_LAYER_ID
    pmDuration = 31
    pmExpire = int(time.time()) + pmDuration
    params = twccommon.Data()
    params.activate = activate
    params.firstLoad = _firstLoad
    params.immediateReplacement = 1
    params.bulletinCrawl = []
    schedules = "[DynamicSchedule('%s')]" % (getPlaylistName(),)
    pm.load(id, pmDuration, pmExpire, schedules, params)
    pm.run(id, 0, 0)
    _activate(activate)
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


def _compareCrawlGroupBulletin(l, r):
    if l.priority > r.priority:
        return -1
    if l.priority < r.priority:
        return 1
    if l.expiration > r.expiration:
        return -1
    if l.expiration < r.expiration:
        return 1
    return 0
    return


def _selectBulletinRotation(bulletins, windowSize):
    if not bulletins:
        return []
    data = _split(bulletins.values(), (lambda e: e.category))
    categories = list(data.keys())
    categories.sort()
    categories.reverse()
    bull = data[categories[0]]
    bull = _squashCrawlGroups(bull)
    bull.sort(key=cmp_to_key(_compareBulletin))
    return _debigulate(bull, windowSize)
    return


def _squashCrawlGroups(rotation):
    res = []
    data = _split(rotation, (lambda e: e.crawlGroup))
    for (key, blist) in data.items():
        if key == None:
            res += blist
        else:
            blist.sort(key=cmp_to_key(_compareCrawlGroupBulletin))
            res.append(blist[0])

    return res
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
    if len(rotation) == 0:
        str += ' no active bulletins|'
    Log.info(str)
    return


def _setMode(rotation):
    return


def _updatePresentation(lastRotation, rotation):
    immediate = 1
    try:
        _params.immediateReplacement = immediate
    except NameError:
        return
    if twc.personality == "Watt":
        if lastRotation:
            _params.changeType = 'update'
        else:
            _params.changeType = 'create'
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
        primaryCounty = 'BOGUS1'
        if len(_interestlist):
            primaryCounty = _interestlist[0]
        bulletin = BulletinInfo.loadBulletin(primaryCounty, county, group)
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


def _activate(activate):
    global _crawlActive
    _crawlActive = activate
    key = DSKEY_CRAWL_ACTIVE
    dsm.set(key, _crawlActive, 0)
    ds.commit()
    return

