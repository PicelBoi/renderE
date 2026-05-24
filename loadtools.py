import os
import nethandler
import twc.psp
import twc.dsmarshal
import twccommon
import functools
import rsfix
import patches

def compilers(rs, unp = True):
    ns = {"params": twccommon.Data()}
    path = None
    if os.path.exists(rs):
        path = rs
    elif nethandler.requestNetAssetExt(rs):
        path = nethandler.requestNetAssetExt(rs)
    if not path:
        raise ValueError("rs file not found!")
    with open(path, "r") as f:
        data = f.read()
    if unp:
        data = patches.unprint(data)
    rseval : str = twc.psp.evalRenderScript(data, ns)
    #replace audiosequencer things
    rseval = rsfix.fix(rseval)
    return rseval

def fixsort(code: str) -> str:
    #replaces the son of the devil (python 2 styled sorting)
    finalcode = ""
    working = code[:]
    while True:
        fn = working.find(".sort(")
        if fn == -1:
            finalcode += working
            break
        finalcode += working[:fn+6]
        close = working.find(")", fn)
        if close == -1:
            raise ValueError("prod file is broken")
        cmp = working[fn+6:close]
        if cmp != "":
            finalcode += f"key=functools.cmp_to_key({cmp})"
        working = working[close:]
    return finalcode.replace("Exception, e", "Exception as e")