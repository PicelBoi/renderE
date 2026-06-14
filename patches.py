import string
import time
import nethandler
import os
import rendereglobals as rg
import loadtools
from pathlib import PurePath
import builtins
import types

def newrange(*args):
    if len(args) == 1:
        return builtins.range(int(args[0]))
    if len(args) == 2:
        return builtins.range(int(args[0]), int(args[1]))
    if len(args) == 3:
        return builtins.range(int(args[0]), int(args[1]), int(args[2]))
string.__dict__["letters"] = string.ascii_letters
string.__dict__["find"] = (lambda s, f : s.find(f))
string.__dict__["upper"] = (lambda s : str(s).upper())
string.__dict__["lower"] = (lambda s : str(s).lower())
def rfix(s, o, n, count=-1):
    return s.replace(o, n, count)

def sfix(s, sep, maxsplit=-1):
    return s.split(sep, maxsplit)
string.__dict__["replace"] = rfix
string.__dict__["split"] = sfix
def fixifsub(val):
    if val is None:
        return -1
    if isinstance(val, types.FunctionType):
        return val
    return val
builtins.__dict__["ehuehuehue_i_added_a_function"] = fixifsub #this is the new winner of "most ridiculous python thing i have ever done"
oldtime = time.struct_time
builtins.__dict__["xrange"] = range

def untab(stuff):
    return stuff.replace("    \t", "        ").replace("\t", "        ")

def unprint(stuff):
    stuff = untab(stuff)
    lines = stuff.split("\n")
    finallines = []
    for l in lines:
        if l.strip().startswith("print"):
            continue
        finallines.append(l)
    return "\n".join(finallines)

from functools import reduce

oldmktime = time.mktime
def newmktime(struc):
    if type(struc) == list:
        return oldmktime(tuple([int(a) for a in struc]))
    return oldmktime(tuple([int(e) for e in struc]))
time.mktime = newmktime

def apply(func, args, kwargs=None):
    return func(*args) if kwargs is None else func(*args, **kwargs)

def newaccess(path, mode):
    if not os.path.exists(path):
        newpath = nethandler.requestNetAssetExt(path)
        if newpath:
            return True
        else:
            return False
    else:
        return os.access(path, mode)

import traceback as tb
def newstat(path):
    try:
        ptest = rg.newjoin(os.path.dirname(os.path.abspath(__file__)), "net")
        if path.startswith(ptest):
            return os.stat(path)
        if not os.access(path, os.R_OK):
            newpath = nethandler.requestNetAssetExt(path)
            if newpath:
                return os.stat(newpath)
            else:
                return os.stat(path)
        else:
            return os.stat(path)
    except:
        tb.print_exc()
        print(path)

def filterfixer9000(fun, it):
    return list(filter(fun, it))

def newexists(path):
    if path.startswith("/twc/data/map.cuts"):
        return os.path.exists(path.replace("/twc/data/map.cuts", rg.newjoin(os.environ["TWCPERSDIR"], "data", "map.cuts")))
    if not os.path.exists(path):
        newpath = nethandler.requestNetAssetExt(path)
        return bool(newpath)
    else:
        return True

def newisfile(path):
    if path.startswith("/twc/data/map.cuts"):
        return os.path.isfile(path.replace("/twc/data/map.cuts", rg.newjoin(os.environ["TWCPERSDIR"], "data", "map.cuts")))
    if not os.path.exists(path):
        newpath = nethandler.requestNetAssetExt(path)
        return os.path.isfile(newpath)
    else:
        return os.path.isfile(path)

def newstrftime(format, struc_time):
    return time.strftime(format.replace("%l", str(int(time.strftime("%I", struc_time))).rjust(2)), struc_time)

rg.newaccess = newaccess
rg.newstat = newstat
rg.newexists = newexists

builtins.__dict__["newstrftime"] = newstrftime

iid = 0

def revmap(*args):
    return list(map(*args))

def runrs(filename):
    global iid
    crs = loadtools.compilers(filename)
    print(type(crs))
    ns = {"apply": apply, "newaccess": newaccess, "newexists": newexists, "newstat": newstat, "newjoin": rg.newjoin, "range": newrange, "map": revmap, "newisfile": newisfile, "newstrftime": newstrftime}
    try:
        exec(crs.replace("os.stat", "newstat").replace("os.access", "newaccess").replace("os.path.exists", "newexists").replace("os.path.join", "newjoin").replace("os.path.isfile", "newisfile").replace("time.strftime", "newstrftime"), ns, ns)
    except Exception as e:
        tb.print_exc()
        with open(f"rscrash{iid}.txt", "w") as f:
            f.write(crs)
        iid += 1
        raise e

def runrsc(filename):
    dat = "global layerProps\n"
    with open(os.path.normpath(filename), "r") as f:
        dat += f.read()
    ns = {"apply": apply, "newaccess": newaccess, "newexists": newexists, "newstat": newstat, "reduce": reduce, "newjoin": rg.newjoin, "time": time, "newisfile": newisfile, "newstrftime": newstrftime}
    ns.update()
    fixed = unprint(dat).replace("os.stat", "newstat").replace("os.access", "newaccess").replace("os.path.exists", "newexists").replace("os.path.join", "newjoin".replace("os.path.isfile", "newisfile").replace("time.strftime", "newstrftime"))
    
    try:
        exec(compile(fixed, filename, "exec"), ns, ns)
    except Exception as e:
        print("CRASH RSC")
        with open("crash_rsc.txt", "w") as f:
            f.write(fixed)
        with open("crash_rsc_e.txt", "w") as f:
            f.write(tb.format_exc())
        raise e

rg.runrsfunction = runrs
rg.runrscfunction = runrsc

def yes_i_am_real_struct_time(seq=None, tm_year=0, tm_mon=0, tm_mday=0, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=0, tm_yday=0, tm_isdst=0):
    if seq:
        return oldtime(seq)
    return oldtime((tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))
time.__dict__["struct_time"] = yes_i_am_real_struct_time