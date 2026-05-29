# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: main.py
# Compiled at: 2007-04-27 10:00:45
import sys, os, os.path, threading, threading, time, traceback, signal, twc.DataStoreInterface, twc.dsmarshal, twc.psp, twc, twccommon.Log, wxscan, wxscan.SunSafetyFactManager, rendereglobals as rg
ds = twc.DataStoreInterface
dsm = twc.dsmarshal
psp = twc.psp
LOOKAHEAD = 8
_orb = None
_config = None
_lock = threading.Lock()

class Command:
    LOAD_CLOCK = 0
    SET_TIME = 1
    LOAD_CLIMATOLOGY_DATA = 2

    def __init__(self, type, **kw):
        self.type = type
        self.__dict__.update(kw)
        return

_cmdQueue = [Command(type=Command.LOAD_CLOCK)]

# class Consumer(twccommon.corba.CosEventComm__POA.PushConsumer):
#     """ CORBA proxy push consumer.  Handle events.
#     """

#     def push(self, args):
#         global _cmdQueue
#         event = args.value()
#         if not isinstance(event, twc.corba.ClientCore.Event):
#             return
#         cmdQueue = []
#         if event.type == 'Load.Clock':
#             twccommon.Log.info('received %s event' % (event.type,))
#             cmdQueue.append(Command(Command.LOAD_CLOCK))
#         elif event.type == 'SevereMode':
#             twccommon.Log.info('received %s event' % (event.type,))
#             cmdQueue.append(Command(Command.LOAD_CLOCK))
#         elif event.type == 'Set.Time':
#             twccommon.Log.info('received %s event' % (event.type,))
#             (t, msec, delta) = event.value.split(' ')
#             cmdQueue.append(Command(Command.SET_TIME, newTime=int(t), delta=int(delta)))
#         if len(cmdQueue) > 0:
#             enterCriticalSection()
#             _cmdQueue.extend(cmdQueue)
#             exitCriticalSection()
#         return

#     def disconnect_push_consumer(self):
#         twccommon.Log.warn('disconnected from event channel')
#         return


def signalHandler(signum, frame):
    twccommon.Log.error('Warning: Process killed. The Clock is now stopped.')
    sys.exit(1)
    return


def enterCriticalSection():
    global _lock
    _lock.acquire()
    return


def exitCriticalSection():
    _lock.release()
    return


def Package(pkgNum):
    key = 'Config.' + dsm.getConfigVersion() + '.Package.%d' % (pkgNum,)
    pkgName = dsm.get(key, cachingEnabled=0)
    twccommon.Log.info('configureable package name lookup: %s -> %s' % (key, pkgName))
    return pkgName
    return


def execClockFile(fname):
    clock = Clock()
    ns = {}
    ns['addCycle'] = clock.addCycle
    ns['Package'] = Package
    execfile(fname, ns, ns)
    ns.clear()
    del ns
    return clock
    return


class Event:

    def __init__(self, name, inst, minutes=None, years=None, months=None, mdays=None, hours=None, wdays=None, ydays=None, duration=60):
        self.minutes = minutes
        self.years = years
        self.months = months
        self.mdays = mdays
        self.hours = hours
        self.wdays = wdays
        self.ydays = ydays
        self.duration = duration
        self.name = name
        self.inst = inst
        return

    def matches(self, time_tuple):
        if self.minutes == None:
            return 0
        if self.years != None and time_tuple[0] not in self.years:
            return 0
        if self.months != None and time_tuple[1] not in self.months:
            return 0
        if self.mdays != None and time_tuple[2] not in self.mdays:
            return 0
        if self.hours != None and time_tuple[3] not in self.hours:
            return 0
        if time_tuple[4] not in self.minutes:
            return 0
        if self.wdays != None and time_tuple[6] not in self.wdays:
            return 0
        if self.ydays != None and time_tuple[7] not in self.ydays:
            return 0
        return 1
        return


class Clock:

    def __init__(self):
        self._event_list = []
        return

    def addCycle(self, cycle, years=None, months=None, mdays=None, hours=None, wdays=None, ydays=None):
        laste = None
        minute = 0
        for s in cycle:
            laste = None
            for p in s:
                if p != None:
                    e = Event(p[0], p[1], (minute,), years, months, mdays, hours, wdays, ydays)
                    laste = e
                    self._event_list.insert(0, e)
                elif laste != None:
                    laste.duration += 60
                minute += 1

        if minute != 60:
            twccommon.Log.error('addCycle expecting 60 minute block of programming and got %d instead.' % minute)
            raise RuntimeError('addCycle expecting 60 minute block')
        return

    def eventAt(self, time_tuple):
        """Calculates the next event.  
        Returns the next package and the number of packages skipped."""
        for e in self._event_list:
            if e.matches(time_tuple):
                return e

        return None
        return

    def findFirstEvent(self, t):
        """Find the first event that can play after specified time.
        The preroll is factored in."""
        global _config
        if len(self._event_list) == 0:
            raise RuntimeError('the clock is empty, fool!')
        time_tuple = time.localtime(t)
        seconds = time_tuple[5]
        if seconds >= 60 - _config.preroll:
            t += 120 - seconds
        else:
            t += 60 - seconds
        time_tuple = time.localtime(t)
        e = self.eventAt(time_tuple)
        loopLimit = 60
        while loopLimit and e == None:
            loopLimit -= 1
            t += 60
            time_tuple = time.localtime(t)
            e = self.eventAt(time_tuple)

        if e == None:
            raise RuntimeError('The clock has NO EVENTS for the next hour!')
        return (e, t - _config.preroll, t)
        return


def sleepUntil(event_time):
    global _orb
    now = time.time()
    while event_time - now > 0.01:
        time.sleep(0.01)
        numCommands = len(_cmdQueue)
        if numCommands > 0:
            return 0
        now = time.time()

    return 1
    return


def getCurrentClockFile():
    try:
        svrMode = dsm.get('SevereMode', cachingEnabled=0)
        configVersion = dsm.getConfigVersion()
        clockFileKey = 'Config.' + configVersion + '.' + _config.clockFileKey
        svrModeClockFileKey = 'Config.' + configVersion + '.' + _config.severeModeClockFileKey
        if not svrMode:
            clockFile = dsm.get(clockFileKey, cachingEnabled=0)
        else:
            clockFile = dsm.get(svrModeClockFileKey, cachingEnabled=0)
    except KeyError:
        twccommon.Log.info('missing data-store key; using default clock')
        clockFile = _config.defaultClockFile

    return  "scmt.clock"#clockFile
    return


def loadNewClock():
    clockFile = _config.workDir + '/' + getCurrentClockFile()
    twccommon.Log.info('loading clock file %s' % clockFile)
    clock = execClockFile(clockFile)
    t = int(time.time())
    (event, event_time, start_time) = clock.findFirstEvent(t)
    cache = [(event, event_time, start_time)]
    t = start_time + event.duration
    for i in range(LOOKAHEAD):
        e = clock.eventAt(time.localtime(t))
        cache.append((e, t - _config.preroll, t))
        t += e.duration

    return (clock, cache, event_time, start_time)
    return


import wxscanpy.plugin.playman.playCmd.pm as pcpm
def presentPackage(sched, startTime, newClock):
    print("clock st", startTime)
    pcpm.load(sched, startTime, newClock)
    #twc.MiscCorbaInterface.signalEvent('SystemEventChannel', 'playman.playCmd.pm.load', repr((sched, startTime, newClock)))
    return


def run():
    global _cmdQueue
    clockChange = 0
    (clock, cache, event_time, start_time) = loadNewClock()
    (newclock, newcache, newevent_time, newstart_time) = (None, None, None, None)
    upNext = list(map((lambda e: (e[0].name, e[0].inst)), cache))
    while 1:
        print("sleepy time")
        sleepCompleted = sleepUntil(event_time)
        print("i wake")
        if not sleepCompleted:
            enterCriticalSection()
            cmdQueue = _cmdQueue
            _cmdQueue = []
            exitCriticalSection()
            for cmd in cmdQueue:
                if cmd.type == Command.LOAD_CLOCK:
                    print("loading le clock")
                    try:
                        (newclock, newcache, newevent_time, newstart_time) = loadNewClock()
                        print("clock success")
                    except Exception as e:
                        newclock = None
                        print('error loading clock file; keeping old clock')

                elif cmd.type == Command.SET_TIME:
                    (e, net, nst) = clock.findFirstEvent(cmd.newTime)
                    if net == event_time:
                        continue
                    elif net < event_time:
                        return
                    elif abs(cmd.newTime - event_time) >= _config.preroll:
                        return
                else:
                    twccommon.Log.error('unknown command type %d; ignoring' % cmd.type)

        if newclock != None:
            if newevent_time == event_time:
                clockChange = 1
                event_time = newevent_time
                clock = newclock
                cache = newcache
                start_time = newstart_time
                newclock = None
                upNext = list(map((lambda e: (e[0].name, e[0].inst)), cache))
        #if not sleepCompleted:
        #    print("skippin")
        #    continue
        sched = list(map((lambda e: (e[0].name, e[0].inst, e[0].duration)), cache))
        cache = cache[1:]
        (dbgPkgName, dbgPkgInst, temp) = sched[0]
        print('building presentation for %s.%d to run at %d' % (dbgPkgName, dbgPkgInst, start_time))
        presentPackage(sched, start_time, clockChange)
        clockChange = 0
        ds.clearCache()
        lastcached = cache[len(cache) - 1]
        st = lastcached[2] + lastcached[0].duration
        nextevent = clock.eventAt(time.localtime(st))
        cache.append((nextevent, st - _config.preroll, st))
        (event_time, start_time) = (cache[0][1], cache[0][2])
        if newclock != None:
            while newevent_time < event_time:
                newcache = newcache[1:]
                lastcached = newcache[len(newcache) - 1]
                st = lastcached[0].duration + lastcached[2]
                newevent = newclock.eventAt(time.localtime(st))
                newcache.append((newevent, st - _config.preroll, st))
                (newevent_time, newstart_time) = (newcache[0][1], newcache[0][2])

    return


def execfile(filename, globa, loca):
    with open(filename, "r", encoding="windows-1252") as f:
        exec(compile(f.read(), filename, 'exec'), globa, loca)

import clockConfig
def main():
    global _config
    global _orb
    twccommon.Log.setIdent('clock')
    try:
        twccommon.Log.info('initializing...')
        #execfile(sys.argv[1])
        _config = clockConfig._values
        #corba crap used to be here
        ds.init()
        ds.enableCaching(1)
        psp.setIncludePath([_config.productDir])
        wxscan.SunSafetyFactManager.init(twc.findRsrc('/sunSafety/sunSafetyFacts', 'data') + '.data')
        pidFileName = _config.pidFileName + '/' + _config.appName + '.pid'
        #wxscan.writePid(pidFileName)
        twccommon.Log.info('running...')
        while 1:
            run()

        ds.uninit()
        return 0
    except Exception as e:
        twccommon.Log.logCurrentException('fatal error; aborting:')
        return -1

    return
import twccommon.embedded
twccommon.embedded.runconfpy(os.path.join(os.path.dirname(__file__), "wxscanpy", "conf", "clock.py"))


if __name__ == '__main__':
    sys.exit(main())
