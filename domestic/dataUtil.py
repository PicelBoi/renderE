# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: dataUtil.py
# Compiled at: 2007-01-12 11:33:26
import glob, os, os.path, string, time, twc, twccommon, twccommon.Log
from functools import cmp_to_key
Log = twccommon.Log

def apply(func, args, kwargs=None):
    return func(*args) if kwargs is None else func(*args, **kwargs)

def findfirst(s, charset):
    """find first of any char that is in s in charset"""
    index = 0
    for c in s:
        if c in charset:
            return index
        index = index + 1

    return -1
    return


def removeChars(s, charset):
    """remove all characters in charset from s"""
    for c in charset:
        n = string.find(s, c)
        while n != -1:
            s = s[:n] + s[n + 1:]
            n = string.find(s, c)

    return s
    return


def secondsToFrames(frames):
    return 30 * frames
    return


def formatDayOfWeek(dow):
    return _week[dow % 7]
    return


def isPointInsideBox(xyPoint, lowerLeftBBox, upperRightBBox):
    """Determine if the point (x,y) is inside the bounding box
       defined by a lower left corner 'lowerLeftBBox' (llx, lly)
       and an upper right corner 'upperRightBBox' (urx, ury).

       Returns: -1 error answer cannot be determined - bad args?
                 1 point is inside box
                 0 point is not inside box"""
    try:
        (x, y) = xyPoint
        (llx, lly) = lowerLeftBBox
        (urx, ury) = upperRightBBox
    except:
        return -1

    if llx > urx:
        return -1
    if lly > ury:
        return -1
    if llx == urx:
        return -1
    if lly == ury:
        return -1
    if x >= llx and x <= urx and y >= lly and y <= ury:
        return 1
    else:
        return 0
    return


def sortByIssueTime(lhs, rhs):
    """Sort Image Files by issue time.

       Assumes items are in the format:
           (time_t, filename)
    """
    ltime = lhs[0]
    rtime = rhs[0]
    if ltime < rtime:
        return 1
    elif ltime > rtime:
        return -1
    else:
        return 0
    return


def isMapAvailable(configSet, product):
    """Is the map cut for a given map product created and ready to use?"""
    mapAvailable = 1
    TWCPERSDIR = os.environ['TWCPERSDIR']
    mapPath = TWCPERSDIR + '/data/map.cuts/'
    mapFile = ''
    mapFile += mapPath
    mapFile += 'Config.%d.%s' % (configSet, product)
    mapFile += '.map'
    if not os.path.exists(mapFile + '.tif'):
        mapAvailable = 0
    return mapAvailable
    return


def getValidFileList(dataPath='./', prefix=None, suffix=None, startTimeNdx=None, endTimeNdx=None, sortIndex=None, sep='.'):
    """Return a list of matching files.

       Given a list of filenames return the names of the valid images
       and their sort value as a list of tuples: (sortedVal, filename).
       Validation is based on the current system time (compared to numeric
       parts of the filename which represent time_t values) as well as flags
       in the arg list.

       The filenames generally have the following format:
       (NOT all fields are required)

       {dataPath}{prefix}{sep}{start_time_t}{sep}{end_time_t}{sep}{suffix}

       where {prefix} is an optional part of the filename which
       precedes the timestamps

       where {suffix} is an optional part of the filename which follows
       the timestamps

       Set startTimeNdx to the position of the startTime field
       (use a negative number to count from the end) if you want to ignore
       files intended to be used in the future.
       Set endTimeNdx to the position of the endTime field if you want to
       ignore files which are expired.
       Set sortIndex (usually equal to startTimeNdx or endTimeNdx) to cause
       the list to be sorted.
    """
    returnList = []
    imageData = dataPath
    if prefix:
        imageData += prefix + sep
    imageData += '*[0-9]'
    if suffix:
        imageData += sep + suffix
    print("IMAGELIST", imageData)
    imageList = glob.glob(imageData)
    if len(imageList) == 0:
        return returnList
    now = time.time()
    for filename in imageList:
        filebase = os.path.basename(filename)
        fileParts = string.split(filebase, sep)
        if endTimeNdx is not None:
            try:
                endTime = int(fileParts[endTimeNdx])
                if now >= endTime:
                    continue
            except:
                continue

        if startTimeNdx is not None:
            try:
                startTime = int(fileParts[startTimeNdx])
                if now < startTime:
                    continue
            except:
                continue

        if sortIndex:
            try:
                returnList.append((int(fileParts[sortIndex]), filename))
            except:
                continue

        else:
            returnList.append((0, filename))

    if sortIndex and len(returnList):
        returnList.sort(key=cmp_to_key(sortByIssueTime))
    return returnList
    return


def getValidImageList(dataPath, productString, ignoreExpiration=0):
    """Return a list of valid image files sorted by issue time.

       Given a list of image filenames return the names of the valid images
       and their issue times as a list of tuples: (issueTime, filename).

       A valid image is one that has an issue time between now and N seconds
       ago - where N is the expirationTime in seconds. The input imageList must
       have filenames in the following format:

       Config.{ConfigSet}.{Product}.{issue_time_t}.{expiration_time_t}.tif
    """
    sortedList = []
    imageData = dataPath + productString + '.*[0-9].tif'
    imageList = glob.glob(imageData)
    if len(imageList) == 0:
        return sortedList
    now = time.time()
    for filename in imageList:
        filebase = os.path.basename(filename)
        fileParts = string.split(filebase, '.')
        try:
            issueTime = int(fileParts[3])
            expirationTime = int(fileParts[4])
        except:
            issueTime = 1
            expirationTime = 1

        if ignoreExpiration == 0:
            if now >= expirationTime:
                continue
        data = (issueTime, filename)
        sortedList.append(data)

    sortedList.sort(key=cmp_to_key(sortByIssueTime))
    return sortedList
    return


def checkImageListForGaps(product, imageList, imageFrequency, maxGap, ignoreTimeGaps=0, purgeImagesOnGap=1):
    """Given a list of images in chronological order, check for time gaps.

       Checks a list of chronological images for gaps based on the
       expected image frequency. The image list must be in the format
       (issueTime, filename). And the fileinames must have the format:

       Config.{ConfigSet}.{Product}.{time_t}.tif
    """
    if len(imageList) > 0:
        now = time.time()
        file = imageList[0]
        issueTime = file[0]
        gapDuration = maxGap * imageFrequency
        maxAllowedGap = now - gapDuration
        if not ignoreTimeGaps and issueTime < maxAllowedGap:
            Log.warning('Time gap found in %s. No images in last %d seconds! Resetting animation loop!' % (product, gapDuration))
            if purgeImagesOnGap:
                for file in imageList:
                    imageName = file[1]
                    statsName = '%s.data.stats' % imageName[:len(imageName) - 4]
                    os.system('rm %s' % (imageName,))
                    os.system('rm %s' % (statsName,))

            imageList = []
    return imageList
    return


def formatApparentTemp(windChill, heatIndex):
    if heatIndex != None and heatIndex >= 80:
        return ('HEAT INDEX', heatIndex)
    elif windChill != None and windChill <= 40:
        return ('WIND CHILL', windChill)
    else:
        return (None, None)
    return


def formatValue(val, rangeList, default=None):
    for (min, max, displayStr) in rangeList:
        if val >= min and val <= max:
            return displayStr

    if default == None:
        return 'No Report'
    return default
    return


def formatUVIndex(uvIndex, default=None):
    ranges = [(0, 2, 'Low'), (3, 5, 'Moderate'), (6, 7, 'High'), (8, 10, 'Very High'), (11, 16, 'Extreme')]
    phrase = formatValue(uvIndex, ranges, default)
    if uvIndex > 10:
        uvIndex = '10+'
    return (uvIndex, phrase)
    return


def formatAirQualityCategory(val, default=None):
    ranges = [(0, 0, 'GOOD'), (1, 1, 'MODERATE'), (2, 2, 'UNHEALTHY for Sensitive Groups'), (3, 3, 'UNHEALTHY'), (4, 4, 'VERY UNHEALTHY'), (5, 5, 'EXTREME')]
    return formatValue(val, ranges, default)
    return


def formatPrimaryPollutant(primaryPollutant):
    pollutant = {'OZONE': 'Ozone', 'PM10': 'Coarse Particulates', 'PM2.5': 'Fine Particulates', 'CO': 'Carbon Monoxide', 'NO2': 'Nitrogen Dioxide', 'SO2': 'Sulfur Dioxide'}
    return pollutant[string.upper(primaryPollutant)]
    return


def formatTrafficType(trafficType):
    trafficGroup = {'ACC': 'Incident', 'ACC?': 'Incident', 'ACC>S': 'Incident', 'ACCLR': 'Incident', 'ACCS': 'Incident', 'BFIR': 'Incident', 'BFIR?': 'Incident', 'CRFR': 'Incident', 'CRFR?': 'Incident', 'DBUS': 'Incident', 'DBUS?': 'Incident', 'DTRK': 'Incident', 'DTRK?': 'Incident', 'DTT': 'Incident', 'DTT?': 'Incident', 'DVEH': 'Incident', 'DVEH?': 'Incident', 'JTT': 'Incident', 'JTT?': 'Incident', 'MCACC': 'Incident', 'MVACC': 'Incident', 'MVACC?': 'Incident', 'OCAR': 'Incident', 'OCAR?': 'Incident', 'OTRK': 'Incident', 'OTRK?': 'Incident', 'OTT': 'Incident', 'OTT?': 'Incident', 'OVEH': 'Incident', 'OVEH?': 'Incident', 'SPILL': 'Incident', 'SPILL?': 'Incident', 'STT': 'Incident', 'STT?': 'Incident', 'TRKFR': 'Incident', 'TRKFR?': 'Incident', 'TTACC': 'Incident', 'TTFR': 'Incident', 'TTFR?': 'Incident', 'VFR': 'Incident', 'VFR?': 'Incident', 'CONST': 'Construction', 'CONST?': 'Construction'}
    if trafficType in trafficGroup:
        type = trafficGroup[trafficType]
    else:
        type = None
    return type
    return


def formatTrafficImpact(crit):
    impact = (('HIGH IMPACT', '/rsrc/images/highImpactObj'), ('HIGH IMPACT', '/rsrc/images/highImpactObj'), ('MEDIUM IMPACT', '/rsrc/images/medImpactObj'), ('LOW IMPACT', '/rsrc/images/highImpactObj'))
    return impact[crit]
    return


ENGLISH = 0
SPANISH = 1

def formatWindDirection(windDir, lang=ENGLISH, default=None):
    if lang == SPANISH:
        return _windDirectionTableSpanish[windDir]
    else:
        return _windDirectionTable[windDir]
    return


def formatWindText(windSpeed, windDir, lang=ENGLISH):
    windText = ''
    try:
        windDirection = formatWindDirection(windDir, lang)
        if int(windDir) == 0:
            if int(windSpeed) > 0:
                Log.warning('formatWindText error windSpeed = %d while windDir == 0' % (windSpeed,))
            windText = windDirection
        elif int(windSpeed) == 0:
            Log.warning('formatWindText error windSpeed = 0 while windDir = %s' % (windDirection,))
            windText = 'Calm'
        else:
            windText = '%s %d' % (windDirection, windSpeed)
    except:
        Log.warning('formatWindText caught exception windDir = %s windSpeed = %s' % (windDir, windSpeed))

    return windText
    return


def formatPressureTendency(pt, lang=ENGLISH):
    if pt == 1:
        return (1, '/rsrc/images/arrowUp')
    elif pt == 2:
        return (1, '/rsrc/images/arrowDown')
    elif pt == 0 and lang == SPANISH:
        return (0, 'E')
    else:
        return (0, 'S')
    return


_windDirectionTable = {}
_windDirectionTable[0] = 'Calm'
_windDirectionTable[1] = 'N'
_windDirectionTable[2] = 'NNE'
_windDirectionTable[3] = 'NE'
_windDirectionTable[4] = 'ENE'
_windDirectionTable[5] = 'E'
_windDirectionTable[6] = 'ESE'
_windDirectionTable[7] = 'SE'
_windDirectionTable[8] = 'SSE'
_windDirectionTable[9] = 'S'
_windDirectionTable[10] = 'SSW'
_windDirectionTable[11] = 'SW'
_windDirectionTable[12] = 'WSW'
_windDirectionTable[13] = 'W'
_windDirectionTable[14] = 'WNW'
_windDirectionTable[15] = 'NW'
_windDirectionTable[16] = 'NNW'
_windDirectionTable[17] = 'Var'
_windDirectionTableSpanish = {}
_windDirectionTableSpanish[0] = 'Calma'
_windDirectionTableSpanish[1] = 'N'
_windDirectionTableSpanish[2] = 'NNE'
_windDirectionTableSpanish[3] = 'NE'
_windDirectionTableSpanish[4] = 'ENE'
_windDirectionTableSpanish[5] = 'E'
_windDirectionTableSpanish[6] = 'ESE'
_windDirectionTableSpanish[7] = 'SE'
_windDirectionTableSpanish[8] = 'SSE'
_windDirectionTableSpanish[9] = 'S'
_windDirectionTableSpanish[10] = 'SSO'
_windDirectionTableSpanish[11] = 'SO'
_windDirectionTableSpanish[12] = 'OSO'
_windDirectionTableSpanish[13] = 'O'
_windDirectionTableSpanish[14] = 'ONO'
_windDirectionTableSpanish[15] = 'NO'
_windDirectionTableSpanish[16] = 'NNO'
_windDirectionTableSpanish[17] = 'VAR'
_week = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]

def getVocalExtFcstTempRange(temperature, default=None):
    ranges = [
        (-199, -16, 'WELL_BELOW'),
        (-15, -1, 'BELOW'),
        (0, 9, 'SINGLE'),
        (10, 13, 'L10S'),
        (14, 16, 'M10S'),
        (17, 19, 'H10S'),
        (20, 23, 'L20S'),
        (24, 26, 'M20S'),
        (27, 29, 'H20S'),
        (30, 33, 'L30S'),
        (34, 36, 'M30S'),
        (37, 39, 'H30S'),
        (40, 43, 'L40S'),
        (44, 46, 'M40S'),
        (47, 49, 'H40S'),
        (50, 53, 'L50S'),
        (54, 56, 'M50S'),
        (57, 59, 'H50S'),
        (60, 63, 'L60S'),
        (64, 66, 'M60S'),
        (67, 69, 'H60S'),
        (70, 73, 'L70S'),
        (74, 76, 'M70S'),
        (77, 79, 'H70S'),
        (80, 83, 'L80S'),
        (84, 86, 'M80S'),
        (87, 89, 'H80S'),
        (90, 93, 'L90S'),
        (94, 96, 'M90S'),
        (97, 99, 'H90S'),
        (100, 103, 'L100S'),
        (104, 106, 'M100S'),
        (107, 109, 'H100S'),
        (110, 113, 'L110S'),
        (114, 116, 'M110S'),
        (117, 119, 'H110S'),
        (120, 123, 'L120S'),
        (124, 129, '120S'),
        (130, 139, '130S')
    ]
    return formatValue(temperature, ranges, default)
    return


def formatHighTempDesc(temperature, default=None):
    ranges = [(-199, 69, 'mild'), (70, 84, 'warm'), (85, 199, 'hot')]
    return formatValue(temperature, ranges, default)
    return


def formatLowTempDesc(temperature, default=None):
    ranges = [(-199, 39, 'cold'), (40, 69, 'cool'), (70, 199, 'mild')]
    return formatValue(temperature, ranges, default)
    return

def formatSevereWxQualifier(severeWxQualCode):
    severeWxQualifier = {'Q9005': 'Potential for up to 3 inches of snow', 'Q9010': 'Potential for up to 6 inches of snow', 'Q9015': 'Potential for 6-12 inches of snow', 'Q9020': 'Potential for a foot or more of snow', 'Q9025': 'Potential for significant snowfall', 'Q9030': 'Potential for blizzard conditions', 'Q9205': 'Potential for some icing', 'Q9210': 'Potential for significant icing', 'Q9350': 'Strong Santa Ana winds possible', 'Q9405': 'Potential for heavy rainfall', 'Q9410': 'Potential for flooding rains', 'Q9605': 'Potential for severe thunderstorms', 'Q9610': 'Severe thunderstorms expected', 'Q9800': 'Watching the tropics', 'Q9805': 'Tropical storm conditions possible', 'Q9810': 'Tropical storm conditions likely', 'Q9815': 'Hurricane conditions possible', 'Q9820': 'Hurricane conditions likely', 'Q9825': 'Major hurricane conditions possible', 'Q9830': 'Major hurricane conditions likely'}
    try:
        return severeWxQualifier[severeWxQualCode]
    except:
        return None

    return

def formatSnowAccum(snowAccumCode):
    snowAccum = {'A9005': 'up to 3 inches of snow', 'A9010': 'up to 6 inches of snow', 'A9015': '6-12 inches of snow', 'A9020': 'a foot or more of snow', 'A9025': 'a significant snowfall', 'A9205': 'some icing', 'A9210': 'significant icing'}
    try:
        return snowAccum[snowAccumCode]
    except:
        return None

    return




import twccommon.PluginManager
TWCPERSDIR = os.environ['TWCPERSDIR']
plugInGroupingRoot = TWCPERSDIR + '/plugin/misc/buckets'
_pmSkyGrouping = twccommon.PluginManager.PluginManager(plugInGroupingRoot, 'buckets')

def getSkyCondGrouping(skyCond, locale):
    plugin = _pmSkyGrouping.retrievePlugin(locale)
    grouping = plugin.getSkyCondGrouping(skyCond)
    try:
        return apply(_makeSCG, grouping)
    except:
        return None

    return


def getObsSkyCondGrouping(skyCond):
    return getSkyCondGrouping(skyCond, 'Observation')
    return


def getFcstSkyCondGrouping(skyCond):
    return getSkyCondGrouping(skyCond, 'Forecast')
    return


def _makeSCG(wr, sr, ws, ss, i, w, c, pc, cl, t, f, sv):
    return twccommon.Data(widespreadRain=wr, scatteredRain=sr, widespreadSnow=ws, scatteredSnow=ss, ice=i, windy=w, cloudy=c, partlyCloudy=pc, clear=cl, thunder=t, fog=f, severe=sv)
    return
