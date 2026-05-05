# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: PromoMessageMapping.py
# Compiled at: 2011-07-22 13:54:05
import types, twc, twcWx.xmlUtil as xmlUtil, twcWx.mapping as mapping, os, nethandler

class PromoMessageMappingHandler(xmlUtil.LookupSubHandler):

    def __init__(self, container):
        self._elements = [('promoMessage', str, xmlUtil.REQUIRED)]
        xmlUtil.LookupSubHandler.__init__(self, container)
        self._key = 0
        return

    def startrecord(self, attrs):
        data = self._parseAttributes(attrs, self._elements)
        if data != None:
            key = self._key
            data = twc.DefaultedData(data)
            self._dataDict[key] = data
            self._key = self._key + 1
        return

import rendereglobals as rg
filePath = rg.newjoin(os.environ["RENDEREMEDIA"], '/mappings/promoMessage/')

class PromoMessageMapping(mapping.Map):

    def __init__(self, refresh=0):
        mapping.Map.__init__(self, refresh)
        return

    def getList(self, data):
        lmap = self._getMap(data)
        result = None
        if lmap is not None:
            keys = list(lmap.keys())
            keys.sort()
            result = list(map(lmap.get, keys))
        return result
        return

    def _load(self, data):
        path = filePath + data + '.xml'
        if not os.path.exists(path):
            path = nethandler.requestNetAssetExt(filePath+data, "xml")
        try:
            map = xmlUtil.parseXML(path, PromoMessageMappingHandler)
            if map:
                return (map, path)
            else:
                return None
        except IOError:
            return None

        return

