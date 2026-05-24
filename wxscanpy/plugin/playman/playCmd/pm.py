# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: pm.py
# Compiled at: 2007-05-14 11:20:55
import os, stat, sys, time, twc, twc.DataStoreInterface as ds, twc.MiscCorbaInterface, twc.dsmarshal as dsm, twc.playlist, twc.DataEventLog as DataEventLog, twccommon, twccommon.Log as Log, wxscan, twcWx.mapping, wxscan.PageCounter as PageCounter, wxscan.SunSafetyFactManager, wxscan.RunLog, wxscan.CSAudioLog
import rendereglobals as rg
import twccommon.Log

def init(config):
    global _config
    _config = twccommon.Data()
    _config.__dict__.update(config.__dict__)
    fname = twc.findRsrc('/sunSafety/sunSafetyFacts', 'data') + '.data'
    wxscan.SunSafetyFactManager.init(fname)
    wxscan.RunLog.init(_config.runlog)
    wxscan.CSAudioLog.init(_config.csAudioLog)
    vp = dsm.configGet('viewports')
    for (lname, depth, repeat, x, y, w, h, sx, sy, tx, ty) in vp:
        _layerProps[lname] = twc.Data(name=lname, depth=depth, x=x, y=y, w=w, h=h)

    return


def load(playlist, startTime, newClock):
    global _lastPlaylist
    if newClock:
        _lastPlaylist = None
    try:
        _pl._rmOldLocalModules(['%s/lib' % _ROOT])
        (package, packageInst, duration) = playlist[0]
        duration = int(duration)
        print('generating playlist for %s.%s' % (package, packageInst))
        params = wxscan.getPkgAttribs(package, packageInst)
        schedName = _selectSchedule(params)
        _pl.setDefaultParams(params)
        try:
            schedule = twc.playlist.getSchedule(schedName, duration * 30, _pl)
            print('Found legitimate schedule', schedName, schedule)
        except:
            print('error with selected schedule %s for %s.%s' % (schedName, package, packageInst))
            print('attempting fallback playlist for duration %d' % duration)
            if duration >= 120:
                package = 'Core1'
            else:
                package = 'Core2'
            packageInst = 0
            params = wxscan.getPkgAttribs(package, packageInst)
            _pl.setDefaultParams(params)
            schedule = _loadFallback(package, _pl)
            if _lastPlaylist is not None:
                _lastPlaylist[1] = (package, packageInst, duration)
            playlist[0] = (package, packageInst, duration)

        fnames = []
        pkgData = twc.Data()
        logSchedule = []
        Log.info('About to loop')
        si = []
        for (prodType, sched) in schedule.items():
            ppsched = list(map((lambda e: (e.getParams().product, e.getDuration())), sched))
            logSchedule.append((prodType, ppsched))
            print('building render-script for dynamic playlist %s: %s' % (prodType, ppsched))
            si.append(prodType)
            startFrameOffset = int(time.time())*30
            inclpaths = []
            inclpaths.append('%s/%s/incl/' % (_ROOT, prodType))
            inclpaths.append('%s/incl/' % (_ROOT,))
            td = []
            filename = '%s_%s-%s_%s.log' % (_config.datalog, package, packageInst, int(time.time()))
            dl = DataEventLog.DataEventLog(filename, _config.datalogDebug)
            for prod in sched:
                prod.updateParams(lastPlaylist=_lastPlaylist, playlist=playlist, startTime=startTime, startFrameOffset=startFrameOffset, mediaRoot=_config.mediaRoot)
                try:
                    fname = _buildPresFile(prodType, prod, inclpaths)
                    fnames.append(fname)
                    si.append(prodType)
                    startFrameOffset += prod.getDuration()
                    prodData = twc.Data()
                    prodData.params = prod.getParams()
                    prodData.data = prod.getData()
                    prodData.testData = prod.getTestData()
                    setattr(pkgData, prod.getName(), prodData)
                    print("SFO", prod.getName(), startFrameOffset)
                except:
                    Log.logCurrentException('error building %s:%s pres' % (package, prod.getParams().product))

        pkgData.schedule = logSchedule
        dl.writeData(package, pkgData)
        _lastPlaylist = playlist
        for i, fname in enumerate(fnames):
            print('running render-script', fname, si[i])
            try:
                _runRenderScriptFile(fname)
            except Exception as e:
                print('error running pres %s' % (fname,))
                twccommon.Log.logCurrentException()

        twcWx.mapping.refreshAll()
    finally:
        _flush()
    return


_ROOT = '/twc/products/pm'

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
        self._rmOldLocalModules(libpath)
        return

    def loadProduct(self, prodType, prodName, prodInst):
        fullProdName = prodType + '_' + prodName
        params = self.getDefaultParams()
        params = wxscan.getProdAttribs(params.package, params.packageInst, fullProdName, prodInst, params)
        params.prodName = prodName
        params.layerProps = _layerProps[prodType]
        libpaths = ['%s/%s/lib' % (_ROOT, prodType), '%s/lib' % _ROOT]
        prodFile = '%s/%s/%s.prod' % (_ROOT, prodType, prodName)
        tmp = sys.path[:]
        try:
            sys.path = libpaths + sys.path
            return self.loadProductFile(prodFile, params)
        finally:
            sys.path = tmp
        return

    def _rmOldLocalModules(self, libpaths):
        Log.debug('checking %s for old dynamic pm modules, actually nvm' % libpaths)
        clean = []
        # for (mname, mod) in sys.modules.items():
        #     try:
        #         fname = mod.__file__
        #     except AttributeError:
        #         continue

        #     path = os.path.dirname(fname)
        #     if path not in libpaths:
        #         continue
        #     purge = 0
        #     try:
        #         mtime = os.stat(fname)[stat.ST_MTIME]
        #         if self._purgeTime < mtime:
        #             purge = 1
        #     except Exception:
        #         purge = 1

        #     if purge:
        #         Log.info('purging dynamic pm module %s because it is outdated' % mname)
        #         clean.append(mname)

        # for mname in clean:
        #     del sys.modules[mname]

        return

    def flush(self):
        twc.products.ProductLoader.flush(self)
        self._purgeTime = time.time()
        return


def _loadFallback(package, prodLoader):
    if package == 'Core1':
        key = 'Playlist.FallbackCore.A'
    else:
        key = 'Playlist.FallbackCore.B'
    key = 'Config.' + dsm.getConfigVersion() + '.' + key
    psched = dsm.defaultedGet(key)
    schedule = {}
    for (prodType, pList) in psched.playlist:
        prodList = []
        for (prodName, prodInst, duration) in pList:
            prod = prodLoader.loadProduct(prodType, prodName, prodInst)
            prod.loadData()
            prod.getDesiredDuration(duration, duration, duration)
            prod.setDuration(duration * 30)
            prodList.append(prod)

        schedule[prodType] = prodList

    return schedule
    return


def _buildPresFile(prodType, prod, inclpaths, **ns):
    rs = prod.genRenderScript(prodType, inclpaths, **ns)
    (fname, f) = wxscan.tmpFile(_config.tempDir)
    f.write(rs)
    f.close()
    return fname
    return


def _runProduct(fname, layerName, **params):
    prod = twc.products.loadProduct(fname, **params)
    rs = prod.genRenderScript(layerName)
    _runRenderScript(rs)
    return


def _runPres(pres, **kw):
    rs = twc.presToRenderScript(pres, **kw)
    _runRenderScript(rs)
    return


def _runRenderScript(rs):
    (fname, f) = wxscan.tmpFile(_config.tempDir)
    f.write(rs)
    f.close()
    _runRenderScriptFile(fname)
    return


def _runRenderScriptFile(rsfname):
    #twc.MiscCorbaInterface.runRenderScript(rsfname)
    rg.runrsfunction(rsfname)
    return


def _flush():
    _pl.flush()
    ds.clearCache()
    return


def _selectSchedule(params):
    package = params.package
    packageInst = params.packageInst
    suffixes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    if package in ['Core1', 'Core2', 'Core3', 'Core4', 'Core2Spanish', 'Core4Spanish', 'LocalBroadcaster']:
        np = _estWeatherBulletinPages(package, packageInst)
        np = min(np, 2)
        return '%s.%s' % (package, suffixes[np])
    elif package in ['Core5', 'Golf', 'Ski', 'Travel', 'NullPackage']:
        return '%s.%s' % (package, suffixes[0])
    elif package in ['International']:
        flavor = _getPackageFlavor(params, 1, 7, 1)
        return '%s.%s' % (package, suffixes[flavor - 1])
    elif package in ['Traffic']:
        return 'Traffic.A'
    elif package in ['Health']:
        flavor = _getPackageFlavor(params, 1, 4, 1)
        return '%s.%s' % (package, suffixes[flavor - 1])
    elif package in ['Garden']:
        flavor = _getPackageFlavor(params, 1, 2, 1)
        return '%s.%s' % (package, suffixes[flavor - 1])
    elif package in ['Airport']:
        flavor = _getPackageFlavor(params, 1, 3, 1)
        return '%s.%s' % (package, suffixes[flavor - 1])
    elif package in ['BoatAndBeach']:
        flavor = _getPackageFlavor(params, 1, 2, 1)
        return '%s.%s' % (package, suffixes[flavor - 1])
    elif package in ['SevereCore1A', 'SevereCore1B', 'SevereCore2']:
        np = _estWeatherBulletinPages(package, packageInst)
        np = min(np, 1)
        return '%s.%s' % (package, suffixes[np])
    raise RuntimeError('no schedule found for package %s.%s' % (package, packageInst))
    return


def _estWeatherBulletinPages(package, packageInst):
    params = twc.Data()
    params.package = package
    params.packageInst = packageInst
    params.product = 'Local_WeatherBulletin'
    params.productInst = 0
    return PageCounter.estWeatherBulletinPages(params)
    return


def _getPackageFlavor(params, min, max, default=1):
    flavor = getattr(params, 'packageFlavor', default)
    if flavor not in range(min, max + 1):
        print('invalid packageFlavor (%s) for %s.%d; using default flavor' % (flavor, params.package, params.packageInst))
        return default
    return flavor
    return


_pl = _ProdLoader()
_layerProps = {}
_lastPlaylist = None
