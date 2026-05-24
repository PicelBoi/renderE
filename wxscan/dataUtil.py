# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: dataUtil.py
# Compiled at: 2007-04-27 10:00:47
import glob, os, os.path, string, time, twc, twccommon, twccommon.Log

def findfirst(s, charset):
    """find first of any char that is in s in charset"""
    index = 0
    for c in s:
        if c in charset:
            return index
        index = index + 1

    return -1
    return


def secondsToFrames(frames):
    return 30 * frames
    return


def formatDayOfWeek(dow):
    return _week[dow % 7]
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
       Validation is based on the current system time (compared to numeric parts of the filename which
          represent time_t values) as well as flags in the arg list.

       The filenames generally have the following format: (NOT all fields are required)
          {dataPath}{prefix}{sep}{start_time_t}{sep}{end_time_t}{sep}{suffix}
          where {prefix} is an optional part of the filename which precedes the timestamps
          where {suffix} is an optional part of the filename which follows the timestamps

       Set startTimeNdx to the position of the startTime field (use a negative number to count from the end)
          if you want to ignore files intended to be used in the future.
       Set endTimeNdx to the position of the endTime field if you want to ignore files which are expired.
       Set sortIndex (usually equal to startTimeNdx or endTimeNdx) to cause the list to be sorted.
    """
    returnList = []
    imageData = dataPath
    if prefix:
        imageData += prefix + sep
    imageData += '*[0-9]'
    if suffix:
        imageData += sep + suffix
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
        returnList.sort(sortByIssueTime)
    return returnList
    return


def getValidImageList(dataPath, productString, ignoreExpiration=0):
    """Return a list of valid image files sorted by issue time.

       Given a list of image filenames return the names of the valid images
       and their issue times as a list of tuples: (issueTime, filename).

       A valid image is one that has an issue time between now and N seconds
       ago - where N is the expirationTime in seconds. The input imageList must
       have filenames in the following format:

       {Pkg}.{PkgInst}.{Prod}.{ProdInst}.{issue_time_t}.{expiration_time_t}.tif
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
            issueTime = int(fileParts[6])
            expirationTime = int(fileParts[7])
        except:
            issueTime = 1
            expirationTime = 1

        if ignoreExpiration == 0:
            if now >= expirationTime:
                continue
        data = (issueTime, filename)
        sortedList.append(data)

    sortedList.sort(sortByIssueTime)
    return sortedList
    return


def getValidMovie(dataPath, region, ignoreExpiration=0):
    """Return the latest(highest expiration time_t) movie that 
       matches and has not expired.

       The movies have filenames in the following format:

       {issue_time_t}.{expiration_time_t}.{region}.mpg
    """
    movieData = dataPath + '/*.' + region + '.mpg'
    movieList = glob.glob(movieData)
    if len(movieList) == 0:
        return None
    now = time.time()
    sortedList = []
    for filename in movieList:
        filebase = os.path.basename(filename)
        fileParts = string.split(filebase, '.')
        try:
            expirationTime = int(fileParts[1])
        except:
            expirationTime = 1

        if ignoreExpiration == 0:
            if now >= expirationTime:
                continue
        data = (expirationTime, filename)
        sortedList.append(data)

    if len(sortedList) == 0:
        return None
    sortedList.sort(sortByIssueTime)
    (expTime, movie) = sortedList[0]
    return movie[:-4]
    return


def checkImageListForGaps(product, imageList, imageFrequency, maxGap, ignoreTimeGaps=0, purgeImagesOnGap=1):
    """Given a list of images in chronological order, check for time gaps.

       Checks a list of chronological images for gaps based on the
       expected image frequency. The image list must be in the format
       (issueTime, filename). And the fileinames must have the format:

       {Pkg}.{PkgInst}.{Prod}.{ProdInst}.{time_t}.tif
    """
    if len(imageList) > 0:
        now = time.time()
        file = imageList[0]
        issueTime = file[0]
        gapDuration = maxGap * imageFrequency
        maxAllowedGap = now - gapDuration
        if not ignoreTimeGaps and issueTime < maxAllowedGap:
            twccommon.Log.warning('Time gap found in %s. No images in last %d seconds! Resetting animation loop!' % (product, gapDuration))
            if purgeImagesOnGap:
                for file in imageList:
                    imageName = file[1]
                    statsName = '%s.data.stats' % imageName[:len(imageName) - 4]
                    os.system('rm %s' % (imageName,))
                    os.system('rm %s' % (statsName,))

                imageList = []
    return imageList
    return


def formatAirportDelay(delay, numFont, textFont, color=(0.92, 0.92, 0.92, 1)):
    strData = []
    strList = []
    if delay == 999:
        str = 'Closed'
        strData = (str, textFont, color)
        strList.append(strData)
        return strList
    elif delay == 0:
        str = 'No Delay'
        strData = (str, textFont, color)
        strList.append(strData)
        return strList
    elif delay < 60:
        str = '%d' % delay
        strData = (str, numFont, color)
        strList.append(strData)
        str = ' min'
        strData = (str, textFont, color)
        strList.append(strData)
        return strList
    else:
        hr = delay / 60
        min = delay % 60
        if min == 0:
            str = '%d' % hr
            strData = (str, numFont, color)
            strList.append(strData)
            str = ' hr'
            strData = (str, textFont, color)
            strList.append(strData)
        else:
            str = '%d' % hr
            strData = (str, numFont, color)
            strList.append(strData)
            str = ' hr'
            strData = (str, textFont, color)
            strList.append(strData)
            str = ' %d' % min
            strData = (str, numFont, color)
            strList.append(strData)
            str = ' min'
            strData = (str, textFont, color)
            strList.append(strData)
        return strList
    return


def formatApparentTemp(windChill, heatIndex):
    if heatIndex != None and heatIndex >= 80:
        return (2, 'Heat Index', heatIndex)
    elif windChill != None and windChill <= 40:
        return (1, 'Wind Chill', windChill)
    else:
        return (0, '', 0)
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


def formatAchesPainsIndex(achesPainsIndex, default=None):
    ranges = [(1, 2, 'Minimal'), (3, 4, 'Low'), (5, 6, 'Moderate'), (7, 8, 'High'), (9, 10, 'Very High')]
    return formatValue(achesPainsIndex, ranges, default)
    return


def formatAirQualityCategory(val, default=None):
    ranges = [(0, 0, 'Good'), (1, 1, 'Moderate'), (2, 2, 'Unhealthy for sensitive groups'), (3, 3, 'Unhealthy'), (4, 4, 'Very Unhealthy'), (5, 5, 'Extreme')]
    return formatValue(val, ranges, default)
    return


def formatPrimaryPollutant(primaryPollutant):
    pollutant = {'OZONE': 'Ozone', 'PM10': 'Coarse Particulates', 'PM2.5': 'Fine Particulates', 'CO': 'Carbon Monoxide', 'NO2': 'Nitrogen Dioxide', 'SO2': 'Sulfur Dioxide'}
    return pollutant[string.upper(primaryPollutant)]
    return


def formatPollenIndex(pollenIndex, default=None):
    ranges = [(0, 0, 'None'), (1, 1, 'Low'), (2, 2, 'Moderate'), (3, 3, 'High'), (4, 4, 'Very High')]
    return formatValue(pollenIndex, ranges, default)
    return


def formatRespiratoryIndex(respiratoryIndex, default=None):
    ranges = [(1, 2, 'Very Poor'), (3, 4, 'Poor'), (5, 6, 'Fair'), (7, 8, 'Good'), (9, 10, 'Very Good')]
    return formatValue(respiratoryIndex, ranges, default)
    return


def formatTreeSpecies(treeCode):
    treeTypes = {'A': 'Alder', 'B': 'Aspen', 'D': 'Cedar', 'E': 'Cottonwood', 'F': 'Cypress', 'G': 'Dogwood', 'H': 'Elm', 'I': 'Fir', 'J': 'Juniper', 'K': 'Maple', 'L': 'Oak', 'M': 'Olive', 'O': 'Pine', 'Q': 'Poplar', 'R': 'Redwood', 'S': 'Sweetgum', 'T': 'Sycamore', 'U': 'Plum', 'V': 'Mulberry', 'W': 'Beech', 'X': 'Pecan', 'Z': 'Unknown', 'AA': 'Ash', 'BB': 'Birch', 'HH': 'Hickory', 'WW': 'Willow'}
    return treeTypes[treeCode]
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
        if windSpeed == 0 and lang == ENGLISH:
            windText = 'Calm'
        elif windSpeed == 0 and lang == SPANISH:
            windText = 'Calma'
        else:
            windText = '%s %d' % (windDirection, windSpeed)
    except:
        pass

    return windText
    return


def formatPressureTendency(pt, lang=ENGLISH):
    if pt == 1:
        return (1, '/rsrc/images/up_arrow')
    elif pt == 2:
        return (1, '/rsrc/images/down_arrow')
    elif pt == 0 and lang == SPANISH:
        return (0, 'E')
    else:
        return (0, 'S')
    return


def formatTrafficType(trafficType):
    trafficGroup = {'ACC': 'Incident', 'ACC?': 'Incident', 'ACC>S': 'Incident', 'ACCLR': 'Incident', 'ACCS': 'Incident', 'BFIR': 'Incident', 'BFIR?': 'Incident', 'CRFR': 'Incident', 'CRFR?': 'Incident', 'DBUS': 'Incident', 'DBUS?': 'Incident', 'DTRK': 'Incident', 'DTRK?': 'Incident', 'DTT': 'Incident', 'DTT?': 'Incident', 'DVEH': 'Incident', 'DVEH?': 'Incident', 'JTT': 'Incident', 'JTT?': 'Incident', 'MCACC': 'Incident', 'MVACC': 'Incident', 'MVACC?': 'Incident', 'OCAR': 'Incident', 'OCAR?': 'Incident', 'OTRK': 'Incident', 'OTRK?': 'Incident', 'OTT': 'Incident', 'OTT?': 'Incident', 'OVEH': 'Incident', 'OVEH?': 'Incident', 'SPILL': 'Incident', 'SPILL?': 'Incident', 'STT': 'Incident', 'STT?': 'Incident', 'TRKFR': 'Incident', 'TRKFR?': 'Incident', 'TTACC': 'Incident', 'TTFR': 'Incident', 'TTFR?': 'Incident', 'VFR': 'Incident', 'VFR?': 'Incident', 'CONST': 'Construction', 'CONST?': 'Construction'}
    if trafficGroup.has_key(trafficType):
        type = trafficGroup[trafficType]
    else:
        type = None
    return type
    return


def formatTrafficImpact(crit):
    impact = (('HIGH IMPACT', '/rsrc/images/highImpactObj'), ('HIGH IMPACT', '/rsrc/images/highImpactObj'), ('MEDIUM IMPACT', '/rsrc/images/medImpactObj'), ('LOW IMPACT', '/rsrc/images/highImpactObj'))
    return impact[crit]
    return


_windDirectionTable = {}
_windDirectionTable[0] = 'Light'
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
_windDirectionTable[17] = 'Variable'
_windDirectionTableSpanish = {}
_windDirectionTableSpanish[0] = 'Light'
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
_windDirectionTableSpanish[17] = 'Variable'
_week = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]
