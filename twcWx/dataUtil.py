# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: dataUtil.py
# Compiled at: 2005-12-01 07:18:53
import twccommon, twcWx.SkyCondMapping as sky, twcWx.TextFcstMapping as txt, twcWx.IncidentTypeMapping as inc, twcWx.BackgroundMusicMapping as bkgMusic, twcWx.PromoMessageMapping as promoMsg, twcWx.WelcomeMessageMapping as welcomeMsg , twcWx.HolidayThemeMapping as holidayTheme
incidentTypeMap = inc.IncidentTypeMapping(1)

def getIncidentType(typeID, mappingFile, default=None):
    result = incidentTypeMap.get(typeID, mappingFile)
    if result == None:
        if default == None:
            result = twccommon.Data(group='', description='')
        else:
            result = default
    return result
    return


skyCondMap = sky.SkyCondMapping(1)

def formatSkyCondition(iconCode, locale='default', default=None):
    result = skyCondMap.get(iconCode, locale)
    if result == None:
        if default == None:
            result = twccommon.Data(iconFile='BlankIcon', textModifier='')
        else:
            result = default
    return result
    return


def skyConditionHasPrecip(iconCode):
    data = skyCondMap.get(iconCode, 'Observation')
    if data.precipitation == None:
        return 0
    return data.precipitation
    return


def getSkyCondGroup(iconCode):
    data = skyCondMap.get(iconCode, 'ExtendedForecast')
    if data.group == None:
        return 0
    return data.group
    return


textFcstMap = txt.TextFcstMapping(1)

def getTextMapping(code, mappingFile, default=None):
    result = textFcstMap.get(code, mappingFile)
    if result == None:
        if default == None:
            result = twccommon.Data(text='')
        else:
            result = default
    return result
    return


bkgMusicMap = bkgMusic.BackgroundMusicMapping(1)

def getBackgroundMusicList(mappingFile):
    result = bkgMusicMap.getList(mappingFile)
    return result
    return


promoMsgMap = promoMsg.PromoMessageMapping(1)

def getPromoMessageList(mappingFile):
    result = promoMsgMap.getList(mappingFile)
    return result
    return


def getPromoMessageAt(mappingFile, index):
    list = promoMsgMap.getList(mappingFile)
    try:
        result = promoMsgMap[index]
        return result
    except:
        return promoMsgMap[0]

    return

welcomeMsgMap = welcomeMsg.WelcomeMessageMapping(1)

def getWelcomeMessageList(mappingFile):
    result = welcomeMsgMap.getList(mappingFile)
    return result
    return


def getWelcomeMessageAt(mappingFile, index):
    list = welcomeMsgMap.getList(mappingFile)
    try:
        result = promoMsgMap[index]
        return result
    except:
        return promoMsgMap[0]

    return

holidayThemeMap = holidayTheme.HolidayThemeMapping(1)

def getHolidayThemeList(mappingFile):
    result = holidayThemeMap.getList(mappingFile)
    return result
    return


def getHolidayTheme(date, mappingFile):
    list = holidayThemeMap.getList(mappingFile)
    holiday = None
    for h in list:
        if date == h.date:
            holiday = h.holiday
            break
    return holiday
    

def validateAttr(obj, attrs):
    for attr in attrs:
        if obj.__dict__.has_key(attr) == 0:
            return None

    return obj
    return
