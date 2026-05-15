# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: backgroundMusic.py
# Compiled at: 2007-05-14 11:20:55
import os, os.path, time, glob, stat, twc, twccommon, twccommon.Log as Log, wxscan.Properties, wxscan, twc.dsmarshal as dsm, twc.DataStoreInterface as ds, twc.MiscCorbaInterface, twcWx.dataUtil as dataUtil, rendereglobals as rg

def init(config):
    global _config
    global _params
    Log.info('backgroundMusic plugin init started')
    _config = twccommon.Data()
    _config.__dict__.update(config.__dict__)
    _params = twc.Data()
    _params.musicDir = '/usr/twc/domestic/products/ext/music'
    _params.tempDir = '%s/musicDir' % (_config.tempDir,)
    _params.layerName = wxscan.Properties.MUSIC_LAYER_NAME
    Log.info('backgroundMusic plugin init ended')
    Log.info('_params.musicDir: %s' % _params.musicDir)
    Log.info('_params.tempDir: %s' % _params.tempDir)
    return


def getNextValidSong(bmDir, bmIdx, bmList):
    origIdx = bmIdx
    firstPass = 1
    bmListEnd = len(bmList) - 1
    if bmIdx >= bmListEnd or bmIdx == -1:
        idx = origIdx = 0
    else:
        idx = bmIdx + 1
    song = bmDir + bmList[idx].musicFile
    while os.path.exists(song) == 0:
        Log.error("BackgroundMusic: song: %s doesn't exist!" % song)
        if idx == bmListEnd:
            idx = 0
        else:
            idx = idx + 1
        if idx == origIdx and not firstPass:
            Log.error('Iterated over entire list one time and none of the songs exists.')
            return (None, -1)
        if firstPass:
            firstPass = 0
        song = bmDir + bmList[idx].musicFile

    Log.info('BackgroundMusic: next song: %s, pos %d' % (song, idx))
    return (song, idx)
    return


def load():
    defaultList = 1
    fname = None
    atime = 0
    musicMediaDir = 'bgm/'
    try:
        bkgMusicList = dataUtil.getBackgroundMusicList('BackgroundMusic')
    except KeyError:
        bkgMusicList = None

    if bkgMusicList != None:
        try:
            currentIdx = dsm.get('Config.' + dsm.getConfigVersion() + '.currentBackgroundSongIdx')
        except KeyError:
            currentIdx = -1
        else:
            if len(bkgMusicList) == 0:
                Log.info('backgroundMusicList is empty!')
            else:
                (fname, currentIdx) = getNextValidSong(musicMediaDir, currentIdx, bkgMusicList)
            if fname == None:
                Log.info('Defaulting to globbing directory for songs.')
            else:
                defaultList = 0
            dsm.set('Config.' + dsm.getConfigVersion() + '.currentBackgroundSongIdx', currentIdx, 0)
            ds.commit()
    if defaultList:
        Log.info('Globbing directory for background music files')
        files = glob.glob(musicMediaDir + '*.mp3')
        if len(files) == 0:
            Log.critical('Missing audio files in %s. NO AUDIO PACKAGE?? ' % musicMediaDir)
            fname = None
        else:
            atimes = map((lambda e: (e, os.stat(e)[stat.ST_ATIME])), files)
            atimes.sort((lambda a, b: twccommon.compare(a[1], b[1])))
            (fname, atime) = atimes[0]
            fname = fname.split('/')
            fname = fname[len(fname) - 1]
            fname = musicMediaDir + fname
    _params.fname = fname
    try:
        Log.info('Calling wxscan.buildPresentationScript()')
        dstName = wxscan.buildPresentationScript(_params.musicDir, _config.tempDir, 'Misc', 0, 'BackgroundMusic', 0, _params)
        Log.info('Running BackgroundMusic render script')
        rg.runrsfunction(dstName)
    except Exception as e:
        Log.error('Unable to call BackgroundMusic.rs render script')
        raise

    return

