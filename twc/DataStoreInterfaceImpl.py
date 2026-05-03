# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: DataStoreInterfaceImpl.py
# Compiled at: 2007-01-12 11:17:29
"""
"""
import os
import rendereglobals as rg
import json
import time

def confchange(text):
    return text.replace("Config.0", "Config.1")

debug = True
class InterfaceImpl:

    def __init__(self):
        print("INTERFACE IMPL CREATED")
        pass
        

    def get(self, keys, cachingEnabled=None, session=0):
        (rc, values, notfound) = self.internalGet(keys, cachingEnabled, session)
        return (rc, values)
        return

    def getAll(self, keys, cachingEnabled=None, session=0):
        (rc, values, notfound) = self.internalGet(keys, cachingEnabled, session)
        values.update(notfound)
        return (rc, values)

    def internalGet(self, keys, cachingEnabled=None, session=0):
        """Internal get implementation for get/getAll to use"""
        notfound = {}
        rc = 1
        result = {}
        
        for key in keys:
            if confchange(key) in rg.sessiondata[session]:
                if (float(rg.sessiondata[session][confchange(key)][1]) < time.time()) and (float(rg.sessiondata[session][confchange(key)][1]) != 0):
                    notfound[confchange(key)] = None
                    del rg.sessiondata[session][confchange(key)]
                    continue
                res = rg.sessiondata[session][confchange(key)]
                result[confchange(key)] = res[0]
            elif confchange(key) in rg.datastore:
                if (float(rg.datastore[confchange(key)][1]) < time.time()) and (float(rg.datastore[confchange(key)][1]) != 0):
                    notfound[confchange(key)] = None
                    self.remove(key, session)
                    #self.commit()
                    continue
                res = rg.datastore[confchange(key)]
                result[confchange(key)] = res[0]
            else:
                notfound[confchange(key)] = None

        return (rc, result, notfound)

    def set(self, entries, session=0):
        rc = 1
        
        for (key, data, expir) in entries:
            rg.sessiondelete[session].discard(confchange(key))
            rg.sessiondata[session][confchange(key)] = (data, expir)

        return rc

    def remove(self, keys, session=0):
        rc = 1
        for key in keys:
            if key in rg.sessiondata:
                del rg.sessiondata[session][confchange(key)]
                rg.sessiondelete[session].add(confchange(key))

        return rc
        return

    def commit(self, session=0):
        rc = 1
        
        for key in rg.sessiondata[session]:
            rg.datastore[key] = rg.sessiondata[session][key]
        rg.sessiondata[session] = {}
        rg.sessiondelete[session] = set()
        
        datas = json.dumps(rg.datastore, indent=4)
        
        try:
            with open(rg.newjoin(os.environ["RENDEREROOT"], "ds.json"), "w") as f:
                f.write(datas)
        except:
            rc = 0

        return rc
        return

    def abort(self, session=0):
        rc = 1
        rg.sessiondata[session] = {}
        rg.sessiondelete[session] = set()

        return rc
        return

    def enableCaching(self, cachingEnabled=1):
        self._cachingEnabled = cachingEnabled
        return

    def clearCache(self):
        self._cache = {}
        self._invalid = []
        return

    def _get(self, keys):
        """Perform a straight DataStoreSession.get, i.e. ignore local cache."""

        return self.get(keys)
        return
