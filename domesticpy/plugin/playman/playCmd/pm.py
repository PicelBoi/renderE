# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: pm.py
# Compiled at: 2007-01-12 11:33:37
import domestic, os, stat, sys, time, twc, twc.DataStoreInterface as ds, twc.dsmarshal as dsm, twc.playlist, twc.products, twc.DataEventLog as DataEventLog, twcWx.mapping, twccommon, twccommon.Log as Log, twccommon.PluginManager as PluginManager
from functools import reduce
import rendereglobals as rg

tempdir = rg.newjoin(os.environ["RENDEREROOT"], "temp")

def init(config):
    global _config
    global _pluginMgr
    global _runlog
    _config = twccommon.Data()
    _config.__dict__.update(config.__dict__)
    _pluginMgr = PluginManager.PluginManager(config.playlistPluginRoot)
    _runlog = twc.EventLog.EventLog(rg.newjoin(tempdir, "runlog"), 3600)
    return


def load(id, duration, expire, schedules, params, runlogEvents=None):
    try:
        if twc.personality == "FlatRock":
            fname = '%s/playlistload' % tempdir
            open(fname, 'w').close()
        if duration == 0:
            Log.error('request to load presentation %s with 0 duration ignored' % id)
            return
        #_pl._rmOldLocalModules(['%s/lib' % _ROOT])
        if runlogEvents == None:
            runlogEvents = []
        argData = twccommon.Data(id=id, duration=duration, expire=expire, schedules=schedules, params=params, expireTime=time.time() + expire / 30, runlogEvents=runlogEvents)
        _presentations[id] = argData
        Log.info('attempting to build presentation (id=%s, schedule=%s)...' % (id, schedules))
        schedLoaders = eval(schedules)
        presentations = _buildBestSchedPresentations(argData, schedLoaders)
        if presentations == None:
            Log.error("couldn't generate a presentation")
            return
        elif twc.personality == "FlatRock":
            fname = '%s/playlistgenerate' % tempdir
            open(fname, 'w').close()
        argData.presentations = presentations
        rsFiles = []
        for vpPres in argData.presentations:
            rsFiles.append(vpPres.fname)

        _runRenderScriptFiles(rsFiles)
    finally:
        _flush()
    return


def run(id, startTime, startFrame, params=None):
    argData = _presentations[id]
    del _presentations[id]
    argData.startTime = startTime
    argData.startFrame = startFrame
    rsFiles = []
    for vpPres in argData.presentations:
        try:
            if params != None:
                pparams = params.clone()
            else:
                pparams = twccommon.Data()
            pparams.startTime = startTime
            pparams.startFrame = startFrame
            pparams.update(vpPres)
            (rsfname, searchPath) = _findFile(vpPres.prodType, 'Run.rs')
            vpPres.runScript = rsfname
            vpPres.runInclPath = list(map((lambda e: '%s/incl' % e), searchPath))
            fname = _buildRenderScriptFile(rsfname, vpPres.runInclPath, params=pparams, runlogEvents=argData.runlogEvents)
            rsFiles.append(fname)
        except Exception:
            Log.logCurrentException('error building presentation')

    try:
        _runRenderScriptFiles(rsFiles)
        if twc.personality == "FlatRock":
            fname = '%s/playlistrun' % tempdir
            open(fname, 'w').close()
    except Exception:
        Log.logCurrentException('error running presentation')

    # if twc.personality == "FlatRock":
    #     if hasattr(pparams, 'sidChannel'):
    #         irdChannelSidTable = dsm.defaultedConfigGet('irdChannelSidTable.%s' % pparams.sidChannel)
    #         if irdChannelSidTable == None:
    #             irdChannelSidTable = dsm.defaultedConfigGet('irdChannelSidTable.default')
    #             if irdChannelSidTable == None:
    #                 irdChannelSidTable = ('100', 9001, 'OA')
    #         (irdChan, sid, sidSum) = irdChannelSidTable
    #         _runUpdateSID(sid, sidSum)
    _buildTestLog(argData)
    _buildRunLog(argData)
    _refreshMedia()
    _cull()
    return


class ScheduleLoader:

    def __repr__(self):
        return self.__str__()
        return

    def getSchedule(self, duration):
        return


class CompositeSchedule(ScheduleLoader):

    def __init__(self, loaders):
        self._loaders = loaders
        return

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, list(map((lambda e: str(e)), self._loaders)))
        return

    def details(self):
        return str(map((lambda e: e.details()), self.__loaders))
        return

    def getSchedule(self, duration):
        schedule = {}
        for sl in self._loaders:
            schedule.update(sl.getSchedule(duration))

        return schedule
        return


class SingleSchedule(ScheduleLoader):

    def __init__(self, schedName):
        self.scheduleName = schedName
        return

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.scheduleName)
        return


class StaticSchedule(SingleSchedule):

    def getSchedule(self, duration):
        mod = _pluginMgr.retrievePlugin(self.scheduleName)
        tmp = mod.getSchedule(duration)
        schedule = {}
        for (prodType, tmppl) in tmp.items():
            playlist = []
            for (prodName, durs) in tmppl:
                prod = _pl.loadProduct(prodType, prodName, 0)
                prod.loadData()
                if len(durs) == 1:
                    dur = durs[0]
                    prod.getDesiredDuration(dur, dur, dur)
                    prod.setDuration(dur)
                else:
                    i = 1
                    fdurs = []
                    for e in durs:
                        fdurs.append((i, e, e, e))

                    prod.getDesiredPageDurations(fdurs)
                    prod.setPageDurations(durs)
                    prod.setDuration(reduce((lambda a, b: a + b), durs, 0))
                playlist.append(prod)

            schedule[prodType] = playlist

        return schedule
        return


class DynamicSchedule(SingleSchedule):

    def getSchedule(self, duration):
        params = _pl.getDefaultParams()
        Log.info('Schedule Name: %s' % self.scheduleName)
        playlistParams = dsm.defaultedConfigGet(self.scheduleName)
        if playlistParams == None:
            Log.warning("couldn't find config entry %s" % self.scheduleName)
        else:
            params = twccommon.mergeStructs([params, playlistParams])
            _pl.setDefaultParams(params)
        return twc.playlist.getSchedule(self.scheduleName, duration, _pl)
        return


class _ProdLoader(twc.products.ProductLoader):

    def __init__(self):
        twc.products.ProductLoader.__init__(self)
        self._purgeTime = -1
        self._params = None
        return

    def setDefaultParams(self, params):
        self._params = params
        return

    def getDefaultParams(self):
        d = twc.Data()
        d.__dict__.update(self._params.__dict__)
        return d
        return

    def startProdType(self, prodType):
        libpath = ['%s/%s/lib' % (_ROOT, prodType)]
        #self._rmOldLocalModules(libpath)
        return

    def loadProduct(self, prodType, prodName, prodInst):
        print('loading product %s_%s...' % (prodType, prodName))
        params = self.getDefaultParams()
        pparams = getAttribs('%s_%s' % (prodType, prodName), params)
        params = twccommon.mergeStructs([params, pparams])
        (prodFile, searchPath) = _findFile(prodType, '%s.prod' % prodName)
        libPath = list(map((lambda e: '%s/lib' % e), searchPath))
        inclPath = list(map((lambda e: '%s/incl' % e), searchPath))
        params.prodFile = prodFile
        params.searchPath = searchPath
        params.inclPath = inclPath
        params.libPath = libPath
        params.prodType = prodType
        params.prodName = prodName
        params.prodInst = prodInst
        params.product = '%s_%s' % (prodType, prodName)
        tmp = sys.path[:]
        try:
            print(libPath, sys.path)
            sys.path = list(libPath) + sys.path
            try:
                return self.loadProductFile(prodFile, params)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print("ERROR OCCURRED IN PROD", prodFile)
                raise e
        finally:
            sys.path = tmp
        return

    def _rmOldLocalModules(self, libpaths):
        Log.debug('checking %s for old dynamic pm modules' % libpaths)
        clean = []
        for (mname, mod) in sys.modules.items():
            try:
                fname = mod.__file__
            except AttributeError:
                continue

            path = os.path.dirname(fname)
            if path not in libpaths:
                continue
            purge = 0
            try:
                mtime = os.stat(fname)[stat.ST_MTIME]
                if self._purgeTime < mtime:
                    purge = 1
            except Exception:
                purge = 1

            if purge:
                Log.info('purging dynamic pm module %s because it is outdated' % mname)
                clean.append(mname)

        for mname in clean:
            del sys.modules[mname]

        return

    def flush(self):
        twc.products.ProductLoader.flush(self)
        self._purgeTime = time.time()
        return


if twc.personality == "Perris":
    def getAttribs(product, params=None):
        cfgVersion = int(dsm.getConfigVersion())
        kl = ['Config', 'Config.%d' % cfgVersion, 'Config.%d.%s' % (cfgVersion, product), 'Config.%d.Override' % cfgVersion]
        fullParams = twc.getAttribList(kl)
        if params:
            fullParams = twccommon.mergeStructs([params, fullParams])
        return fullParams
        return
elif twc.personality == "FlatRock":
    def getAttribs(product, prodInst, params=None):
        cfgVersion = int(dsm.getConfigVersion())
        #kl = ['Config', 'Config.%d' % cfgVersion, 'Config.%d.%s' % (cfgVersion, product), 'Config.%d.%s.%d' % (cfgVersion, product, prodInst), 'Config.%d.Override' % cfgVersion]
        kl = ['Config', 'Config.%d' % cfgVersion, 'Config.%d.%s' % (cfgVersion, product), 'Config.%d.Override' % cfgVersion]
        fullParams = twc.getAttribList(kl)
        if params:
            fullParams = twccommon.mergeStructs([params, fullParams])
        return fullParams
        return

import nethandler
def _findFile(prodType, fname):
    paths = ['%s/%s' % (_ROOT, prodType), _ROOT]
    paths2 = ['%s/%s' % (_NETROOT, prodType), _NETROOT]
    paths3 = ['%s/%s' % (_NETROOT, prodType), _NETROOT]
    print("FINDFILE PATHS")
    print(paths)
    print(paths2)
    print(paths3)
    pathsSearched = paths
    while len(paths) > 0:
        fullname = paths[0] + '/%s' % fname
        if os.path.exists(fullname):
            return (fullname, paths)
        paths = paths[1:]
    while len(paths2) > 0:
        fullname = paths2[0] + '/%s' % fname
        nt = nethandler.requestNetAssetExt(fullname, check=True)
        if nt:
            return (nt, paths2)
        fullname = paths2[0] + '/%s' % fname
        nt = nethandler.requestNetAssetExt(fullname)
        if nt:
            return (nt, paths3)
        paths2 = paths2[1:]

    raise Exception("couldn't locate file %s in %s" % (fname, pathsSearched))
    return


def _findInPath(path, fname):
    for p in path:
        fullname = '%s/%s' % (p, fname)
        if os.path.exists(fullname):
            return fname

    return None
    return


def _readFile(fname):
    f = open(fname, "r")
    try:
        return f.read()
    finally:
        f.close()
    return


def _dsmget(key):
    val = None
    try:
        val = dsm.defaultedGet(key)
    except Exception:
        pass

    return val
    return


def _buildBestSchedPresentations(argData, schedLoaders):
    presentations = []
    for schedLoader in schedLoaders:
        try:
            Log.info('building schedule %s...' % schedLoader)
            params = argData.params.clone()
            _pl.setDefaultParams(params)
            schedule = schedLoader.getSchedule(argData.duration)
            if twc.personality == "FlatRock":
                for (prodType, playlist) in schedule.items():
                    print("Setting Playlist Schedule", prodType, playlist)
                    prodLabels = []
                    for prod in playlist:
                        labels = prod.getLabel()
                        print("ProdLabel", labels)
                        for labelData in labels:
                            if labelData.label == '*':
                                continue

                        prodLabels.append(labels)

                    key = '%s.playlistSchedule' % prodType
                    Log.info('Setting playlist schedule for %s' % key)
                    dsm.set(key, prodLabels, 0)
                    ds.commit()
            
            return _buildSchedPresentations(argData, schedule)
        except Exception:
            Log.logCurrentException('error building schedule %s:' % schedLoader)

    return None
    return


def _buildSchedPresentations(argData, schedule):
    vpPresentations = []
    Log.info('schedule contains the following playlists %s' % schedule.keys())
    for (prodType, playlist) in schedule.items():
        Log.info('building playlist for viewport %s...' % prodType)
        vpPresentations.append(_buildViewportPresentation(argData, prodType, playlist))

    return vpPresentations
    return


def _buildViewportPresentation(argData, prodType, playlist):
    vpPres = twccommon.Data()
    vpPres.prodType = prodType
    vpPres.prodPresentations = []
    vpPres.layerProps = dsm.configGet('viewport.%s' % prodType)
    print("LPROPS", vpPres.layerProps, 'viewport.%s' % prodType)
    vpPres.layerProps.name = '%s_%s' % (prodType, argData.id)
    vpPres.layerProps.expire = argData.expire
    if twc.personality == "Perris":
        vpPres.prodSchedule = list(map((lambda e: (e.getName(), e.getDuration())), playlist))
    elif twc.personality == "FlatRock":
        vpPres.prodSchedule = list(map((lambda e: (e.getName(), e.getDuration(), e.getProdInstance())), playlist))
    startTime = 0
    startFrameOffset = 0
    prodCount = 0
    for prod in playlist:
        Log.info('building presentation for product %s (duration=%s)...' % (prod.getName(), prod.getDuration()))
        prod.updateParams(startTime=startTime, startFrameOffset=startFrameOffset, prodType=prodType, layerProps=vpPres.layerProps, prodSchedule=vpPres.prodSchedule, prodCount=prodCount)
        pres = _buildProductPresentation(argData, vpPres, prod)
        startFrameOffset += pres.prod.getDuration()
        prodCount += 1
        vpPres.prodPresentations.append(pres)

    params = argData.params.clone()
    params.preroll = _config.preroll
    params.layerProps = vpPres.layerProps
    params.prodSchedule = list(map((lambda e: (e.fname, e.prod.getDuration())), vpPres.prodPresentations))
    runlogEvents = []
    (rsfname, searchPath) = _findFile(vpPres.prodType, 'Load.rs')
    vpPres.loadScript = rsfname
    vpPres.loadInclPath = list(map((lambda e: '%s/incl' % e), searchPath))
    vpPres.fname = _buildRenderScriptFile(rsfname, vpPres.loadInclPath, vpPres.layerProps.name, params=params, runlogEvents=runlogEvents)
    argData.runlogEvents.extend(runlogEvents)
    return vpPres
    return


def _buildProductPresentation(argData, vpPres, prod):
    pres = twccommon.Data()
    pres.prod = prod
    runlogEvents = []
    pres.fname = _buildPresFile(vpPres.prodType, prod, prod.getParams().inclPath, runlogEvents=runlogEvents)
    argData.runlogEvents.extend(runlogEvents)
    Log.info('generated render script for %s (%s)' % (prod.getName(), pres.fname))
    return pres
    return


def _buildPresFile(prodType, prod, inclpaths, **ns):
    (fname, f) = domestic.tmpFile(tempdir, prod.getName(), 'rsc')
    prod.updateParams(fname=fname)
    rs = prod.genRenderScript(prodType, inclpaths, **ns)
    try:
        f.write(rs)
    except Exception as e:
        print("Error writing pres file! Dumped using forced utf-8")
        with open("rs_write_dump.txt", "w", encoding="utf-8") as f:
            f.write(rs)
        raise e
    finally:
        f.close()
    return fname
    return


def _buildRenderScriptFile(rsfname, inclPath, dst=None, **kw):
    rs = _readFile(rsfname)
    rsc = twc.psp.evalRenderScript(rs, kw, inclPath)
    if dst != None:
        fname = '%s/%s.rsc' % (tempdir, dst)
        f = open(fname, 'w')
    else:
        (fname, f) = domestic.tmpFile(tempdir, '', 'rsc')
    f.write(rsc)
    f.close()
    return fname
    return


def _runRenderScriptFiles(rsFileList):
    hdr = 'from twc.embedded.renderd import RenderControl\n'
    (loaderFile, f) = domestic.tmpFile(tempdir, '', 'ldr')
    f.write(hdr)
    for rs in rsFileList:
        f.write('RenderControl.loadPresentation("')
        f.write(rs)
        f.write('")\n')

    f.close()
    Log.info('running render script files %s' % loaderFile)
    _runRenderScriptFile(loaderFile)
    return

import rendereglobals as rg
def _runRenderScriptFile(rsfname):
    #twc.MiscCorbaInterface.runRenderScript(rsfname)
    rg.runrsfunction(rsfname)
    return


def _flush():
    _pl.flush()
    ds.clearCache()
    return


def _buildTestLog(argData):
    adt = argData.clone()
    del adt.presentations
    for vpPres in argData.presentations:
        vdt = vpPres.clone()
        setattr(adt, vpPres.prodType, vdt)
        del vdt.prodPresentations
        for pres in vpPres.prodPresentations:
            pdt = pres.clone()
            del pdt.prod
            setattr(vdt, pres.prod.getShortName(), pdt)
            setattr(pdt, 'params', pres.prod.getParams())
            setattr(pdt, 'data', pres.prod.getData())
            setattr(pdt, 'testData', pres.prod.getTestData())

    fname = '%s/%s.xml' % (_LOG_ROOT, adt.id)
    dl = DataEventLog.DataEventLog(fname, 1)
    dl.writeData('presentation', adt)
    return


def _buildRunLog(argData):
    for (k, v) in argData.runlogEvents:
        _runlog.writeData(k, v)

    return


def _refreshMedia():
    twcWx.mapping.refreshAll()
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


_ROOT = rg.newjoin(os.environ["RENDEREDOMESTIC"], "products", "pm")
_NETROOT = '/usr/twc/domestic/products/pm'
_LOG_ROOT = rg.newjoin(os.environ["RENDEREROOT"], "temp", "logs")
os.makedirs(_LOG_ROOT, exist_ok=True)
_pl = _ProdLoader()
_pluginMgr = None
_presentations = {}
_runlog = None
