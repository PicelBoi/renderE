# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: ldl.py
# Compiled at: 2007-01-12 11:33:37
import domestic, time, twccommon, twccommon.Log, twc.MiscCorbaInterface, twc.dsmarshal
from domestic import BulletinInfo
dsm = twc.dsmarshal

_activate = 0
def init(config):
    global _activate
    global _config
    _displayMode = None
    _activate = dsm.defaultedGet('sensorState')
    if _activate is not None:
        _activate = int(_activate)
    else:
        _activate = 0
    _config = twccommon.Data()
    _config.duration = 5400
    _config.expiration = 300
    if twc.personality == "Perris":
        _config.playlistId = 'NationalLDL'
        _config.defaultPlaylistName = 'Ldl.nationalDefaultUp'
        _config.downPlaylistName = 'Ldl.nationalDown'
    elif twc.personality == "FlatRock":
        _config.defaultPlaylistName = 'NationalLdl.nationalLdlUp'
        _config.downPlaylistName = 'NationalLdl.nationalDown'
    _config.__dict__.update(config.__dict__)
    return


def _ldlBulletins():
    counties = dsm.defaultedConfigGet('interestlist.county')
    if counties is not None:
        bulletins = BulletinInfo.loadActiveBulletins(counties)
    else:
        bulletins = {}
    for (key, val) in bulletins.copy().items():
        if val.ldl == 0:
            del bulletins[key]

    return bulletins
    return

if twc.personality == "Perris":
    def _getPlaylistName(ldlWarningMode):
        _dispMode = {'A': (twc.Data(playlistName='Ldl.nationalDefaultUp')), 'B': (twc.Data(playlistName='Ldl.nationalLongformUp'))}
        dispMode = dsm.defaultedGet('displayMode')
        if dispMode in _dispMode:
            playListName = _dispMode[dispMode].playlistName
        else:
            playListName = _config.defaultPlaylistName
        if playListName == 'Ldl.nationalDefaultUp':
            (y, m, d, H, M, S, dow, jd, dst) = time.localtime()
            if H >= 5 and H < 10:
                if ldlWarningMode == 0:
                    playListName = 'Ldl.nationalMorningUp'
                else:
                    playListName = 'Ldl.nationalMorningSevereUp'
        twccommon.Log.info('Playlist.%s chosen' % playListName)
        playlistOverride = dsm.defaultedConfigGet('LdlPlaylistOverride')
        if playlistOverride == 'nationalDbsUp':
            playListName = 'Ldl.%s' % playlistOverride
            _config.duration = 13800
        return playListName
        return
elif twc.personality == "FlatRock":
    def _getPlaylistName(displayMode=None):
        global _displayMode
        (y, m, d, H, M, S, dow, jd, dst) = time.localtime()
        now = H * 100 + M
        if displayMode is None:
            _displayMode = dsm.defaultedGet('displayMode')
        else:
            _displayMode = displayMode
        if _displayMode == 'A':
            playlistSchedule = dsm.defaultedGet('Config.%s.Playlist.NationalLdl.scheduleA' % dsm.getConfigVersion())
        elif _displayMode == 'B':
            playlistSchedule = dsm.defaultedGet('Config.%s.Playlist.NationalLdl.scheduleB' % dsm.getConfigVersion())
        else:
            twccommon.Log.warning('Unknown displayMode=%s' % displayMode)
            playlistSchedule = None
        if playlistSchedule == None:
            twccommon.Log.error('Unable to choose LDL playlist. No LDL Playlists are configured!')
            return None
        try:
            for (st, et, plName) in playlistSchedule[dow]:
                start = st[0] * 100 + st[1]
                end = et[0] * 100 + et[1]
                if start <= now and end >= now:
                    twccommon.Log.info('LDL playlist Playlist.%s chosen' % plName)
                    return plName

        except Exception as e:
            twccommon.Log.error('Unable choose LDL playlist for day %d time %d:%d' % (dow, H, M))

        return None

import domesticpy.plugin.playman.playCmd.pm as pcpm
if twc.personality == "Perris":
    def load(playlistId, playlistName, duration, bulletins):
        tmpLdlWarningMode = _getLdlWarningMode(bulletins)
        eventValue = (playlistId, duration, _config.expiration, "[DynamicSchedule('%s')]" % playlistName, twccommon.Data(ldlBulletins=bulletins, ldlWarningMode=tmpLdlWarningMode, nationalLdl=1))
        #twc.MiscCorbaInterface.signalEvent('SystemEventChannel', 'playman.playCmd.pm.load', eventValue)
        pcpm.load(*eventValue)
        return
elif twc.personality == "FlatRock":
    def load(playlistId, activate, displayMode):
        global _activate
        global _displayMode
        _activate = activate
        _displayMode = displayMode
        bulletins = _ldlBulletins()
        ldlWarningMode = _getLdlWarningMode(bulletins)
        if activate == 0:
            playlistName = _config.downPlaylistName
            duration = 1
        else:
            playlistName = _getPlaylistName(displayMode)
            if playlistName == None:
                return 0
            duration = _config.duration
        tmpLdlWarningMode = _getLdlWarningMode(bulletins)
        eventValue = repr((playlistId, duration, _config.expiration, "[DynamicSchedule('%s')]" % playlistName, twccommon.Data(ldlBulletins=bulletins, ldlWarningMode=tmpLdlWarningMode, nationalLdl=1, displayMode=displayMode)))
        pcpm.load(*eventValue)
        return 1
        return

if twc.personality == "Perris":
    def toggleNationalLDL(id, activate, time=0, frame=0):
        print("i am the")
        global _activate
        if _activate not in vars():
            _activate = 0
        id = int(id)
        time = int(time)
        frame = int(frame)
        activate = int(activate)
        if _activate == 0 and activate == 0:
            return
        _activate = activate
        bulletins = _ldlBulletins()
        ldlWarningMode = _getLdlWarningMode(bulletins)
        if activate == 0:
            load(_config.playlistId, _config.downPlaylistName, 1, bulletins)
            return
        playlistName = _getPlaylistName(ldlWarningMode)
        load(_config.playlistId, playlistName, _config.duration, bulletins)
        eventValue = (_config.playlistId, time, frame, twccommon.Data(nationalLdl=1))
        #twc.MiscCorbaInterface.signalEvent('SystemEventChannel', 'playman.playCmd.pm.run', eventValue)
        print("i am the national ldl")
        pcpm.run(*eventValue)
        return
elif twc.personality == "FlatRock":
    def run(playlistId, time, frame):
        eventValue = repr((playlistId, time, frame, twccommon.Data(nationalLdl=1, displayMode=_displayMode)))
        pcpm.run(*eventValue)
        return
    
    def toggleNationalLDL(id, activate, displayMode=None, time=0, frame=0):
        time = int(time)
        frame = int(frame)
        activate = int(activate)
        if load(id, activate, displayMode) and activate == 1:
            run(id, time, frame)
        return


def _getLdlWarningMode(bulletins):
    hurricaneStatement = dsm.defaultedGet('hurricaneStatement')
    ldlWarningMode = 0
    if len(bulletins) > 0:
        ldlWarningMode = 1
    elif hurricaneStatement != None:
        ldlWarningMode = 1
    return ldlWarningMode
    return

