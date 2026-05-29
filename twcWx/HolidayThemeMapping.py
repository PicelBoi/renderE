import types, twc, twcWx.xmlUtil as xmlUtil, twcWx.mapping as mapping, os, nethandler

class HolidayThemeMappingHandler(xmlUtil.LookupSubHandler):

    def __init__(self, container):
        self._elements = [('date', str, xmlUtil.REQUIRED), ('holiday', str, xmlUtil.REQUIRED), ('R', int, xmlUtil.REQUIRED), ('G', int, xmlUtil.REQUIRED), ('B', int, xmlUtil.REQUIRED)]
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
filePath = rg.newjoin('/media/mappings/holidayThemes/')
print(filePath)

class HolidayThemeMapping(mapping.Map):

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
            map = xmlUtil.parseXML(path, HolidayThemeMappingHandler)
            if map:
                return (map, path)
            else:
                return None
        except IOError:
            return None

        return

