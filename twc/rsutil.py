# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: rsutil.py
# Compiled at: 2007-01-12 11:17:30
import glob, os, os.path, string, time, twc
from functools import cmp_to_key
from twc import SkyConditionCodes
from twc.SkyConditionCodes import _EnglishFcstSkyConditionTable
from twc.SkyConditionCodes import _EnglishObsSkyConditionTable
from twc.SkyConditionCodes import _SkyConditionInfo
from twc.SkyConditionCodes import _SpanishFcstSkyConditionTable
from twc.SkyConditionCodes import _SpanishObsSkyConditionTable

def secondsToFrames(frames):
    return 30 * frames
    return


def rgbaConvert(r, g, b, a=255.0):
    return (r / 255.0, g / 255.0, b / 255.0, a / 255.0)
    return


def formatDayOfWeek(dow):
    return _week[dow % 7]
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


def getValidImageList(dataPath, productString):
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
            issueTime = int(fileParts[4])
            expirationTime = int(fileParts[5])
        except:
            issueTime = 1
            expirationTime = 1

        if now >= expirationTime:
            continue
        data = (issueTime, filename)
        sortedList.append(data)

    sortedList.sort(key=cmp_to_key(sortByIssueTime))
    return sortedList
    return


def checkImageListForGaps(imageList, imageFrequency, maxGap):
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
        if issueTime < maxAllowedGap:
            print('Time gap found. No images received in last %d seconds!' % gapDuration)
            return []
    return imageList
    return


def formatAirportDelay(delay, fname, numFSize, textFSize, color=rgbaConvert(235, 235, 235, 255)):
    strData = []
    strList = []
    if delay == 999:
        str = 'Closed'
        strData = (str, fname, textFSize, color)
        strList.append(strData)
        return strList
    elif delay == 0:
        str = 'No Delay'
        strData = (str, fname, textFSize, color)
        strList.append(strData)
        return strList
    elif delay < 60:
        str = '%d' % delay
        strData = (str, fname, numFSize, color)
        strList.append(strData)
        str = 'min'
        strData = (str, fname, textFSize, color)
        strList.append(strData)
        return strList
    else:
        hr = delay / 60
        min = delay % 60
        if min == 0:
            str = '%d' % hr
            strData = (str, fname, numFSize, color)
            strList.append(strData)
            str = 'hr'
            strData = (str, fname, textFSize, color)
            strList.append(strData)
        else:
            str = '%d' % hr
            strData = (str, fname, numFSize, color)
            strList.append(strData)
            str = 'hr '
            strData = (str, fname, textFSize, color)
            strList.append(strData)
            str = '%d' % min
            strData = (str, fname, numFSize, color)
            strList.append(strData)
            str = 'min'
            strData = (str, fname, textFSize, color)
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
    ranges = [(0, 2, 'Minimal'), (3, 4, 'Low'), (5, 6, 'Moderate'), (7, 9, 'High'), (10, 10, 'Very High'), (11, 16, 'Extreme')]
    phrase = formatValue(uvIndex, ranges, default)
    if uvIndex > 10:
        uvIndex = '10+'
    return (uvIndex, phrase)
    return


def formatAchesPainsIndex(achesPainsIndex, default=None):
    ranges = [(1, 2, 'Minimal'), (3, 4, 'Low'), (5, 6, 'Moderate'), (7, 8, 'High'), (9, 10, 'Very High')]
    return formatValue(achesPainsIndex, ranges, default)
    return


def formatAirQualityIndex(airQualityIndex, default=None):
    ranges = [(0, 50, 'Good'), (51, 100, 'Moderate'), (101, 150, 'Unhealthy for sensitive groups'), (151, 200, 'Unhealthy'), (201, 500, 'Very Unhealthy')]
    return formatValue(airQualityIndex, ranges, default)
    return


def formatPrimaryPollutant(primaryPollutant):
    pollutant = {'OZONE': 'Ozone', 'PM': 'Coarse Particulates', 'PM2.5': 'Fine Particulates', 'CO': 'Carbon Monoxide', 'NO2': 'Nitrogen Dioxide', 'SO2': 'Sulfur Dioxide'}
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


def isDST(t=time.time()):
    weekdayOffset = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 6: 0}
    (y, m, d, H, M, S, dow, doy, dst) = time.localtime(t)
    beginDST = time.mktime((y, 3, 8, 1, 59, 59, 0, 0, dst))
    (y1, m1, d1, H1, M1, S1, dow1, doy1, dst1) = time.localtime(beginDST)
    beginDST = time.mktime((y1, m1, d1 + weekdayOffset[dow1], 1, 59, 59, 0, 0, dst1))
    endDST = time.mktime((y, 11, 1, 1, 59, 59, 0, 0, dst))
    (y1, m1, d1, H1, M1, S1, dow1, doy1, dst1) = time.localtime(endDST)
    endDST = time.mktime((y1, m1, d1 + weekdayOffset[dow1], 1, 59, 59, 0, 0, dst1))
    if t > beginDST and t < endDST:
        return 1
    else:
        return 0
    return

forceVocalOff = False

def playVocal(utcTimeStamp, offTimes):
    if forceVocalOff:
        return False
    if isDST(utcTimeStamp):
        tzOffset = 4
    else:
        tzOffset = 5
    timeTuple = time.gmtime(utcTimeStamp)
    hour = timeTuple[3]
    easternHour = hour - tzOffset
    if easternHour < 0:
        easternHour += 24
    showVocalLocalReturnCode = 1
    for offTimeTuple in offTimes:
        (startHour, endHour) = offTimeTuple
        if startHour < endHour:
            if startHour <= easternHour <= endHour:
                showVocalLocalReturnCode = 0
        elif startHour == endHour:
            if startHour == easternHour:
                showVocalLocalReturnCode = 0
        elif startHour <= easternHour or easternHour <= endHour:
            showVocalLocalReturnCode = 0

    return showVocalLocalReturnCode
    return


LEFT = 0
RIGHT = 1
CENTER = 2

def justifyGR(length, width, justify=LEFT):
    xOffset = 0
    if justify is RIGHT:
        xOffset = width - length
    elif justify is CENTER:
        xOffset = (width - length) / 2.0
    return xOffset
    return


def paginateText(font, str, width, height):
    res = []
    totStrHeight = 0
    words = str.split(' ')
    if len(words) < 2:
        return [str]
    (s, words, sh) = _getNextLine(font, words, width)
    totStrHeight += sh
    while len(words):
        (tmp, words, sh) = _getNextLine(font, words, width)
        totStrHeight += sh
        if totStrHeight <= height:
            s = s + '\n' + tmp
        else:
            res.append(s)
            s = tmp
            totStrHeight = sh

    res.append(s)
    return res
    return


def _getNextLine(font, words, width):
    str = words[0]
    words = words[1:]
    (sw, sh) = font.stringSize(str)
    while len(words):
        temp = str + ' %s' % (words[0],)
        (sw, sh) = font.stringSize(temp)
        if sw >= width:
            break
        str = temp
        words = words[1:]

    return (str, words, sh)
    return


def animationLoop(page, imageList, repeat=1):
    count = 0
    for grData in imageList:
        gr = grData[0]
        if count > 0:
            gr.setVisibility(0)
        else:
            gr.setVisibility(1)
        es = twc.embedded.renderd.RenderScript.EffectSequencer(gr, repeat)
        for ii in range(len(imageList)):
            duration = imageList[ii][1]
            es.addEffect(twc.embedded.renderd.RenderScript.SetVisibility(None, ii is count), duration)

        page.addItem(gr)
        page.addItem(es)
        count = count + 1

    return


def sequenceOnPage(page, grSet, delay=30, repeat=0):
    count = 0
    for grList in grSet:
        for gr in grList:
            es = twc.embedded.renderd.RenderScript.EffectSequencer(gr, repeat)
            if count > 0:
                gr.setVisibility(0)
            else:
                gr.setVisibility(1)
            for i in range(len(grSet)):
                es.addEffect(twc.embedded.renderd.RenderScript.SetVisibility(None, i is count), delay)

            page.addItem(gr)
            page.addItem(es)

        count = count + 1

    return


def gradientSlider(page, legendW, legendH, minVal, maxVal, value, rgbaVals, scaleIndex=None):
    trueMax = max(minVal, maxVal)
    trueMin = min(minVal, maxVal)
    if value > trueMax:
        value = trueMax
    elif value < trueMin:
        value = trueMin
    slider = twc.embedded.renderd.RenderScript.CompositeRenderable()
    legend = gradientBox(legendW, legendH, rgbaVals)
    slider.addItem(legend)
    if scaleIndex is not None:
        slider.addItem(scaleIndex)
    pointer = twc.embedded.renderd.RenderScript.CompositeRenderable()
    triStartOffset = 3
    tri = twc.embedded.renderd.RenderScript.Polygon()
    triX = 5
    triY = legendH + triStartOffset
    triOffset = 21
    (r, g, b, a) = rgbaConvert(235, 235, 235, 255)
    tri.addVertex(triX - triOffset / 2, triY, r, g, b, a)
    tri.addVertex(triX + triOffset / 2, triY, r, g, b, a)
    tri.addVertex(triX, triY - triOffset, r, g, b, a)
    shadow = twc.embedded.renderd.RenderScript.Polygon()
    (r, g, b, a) = rgbaConvert(10, 10, 10, 153)
    shadow.addVertex(triX - triOffset / 2 + 3, triY - 2, r, g, b, a)
    shadow.addVertex(triX + triOffset / 2 + 3, triY - 2, r, g, b, a)
    shadow.addVertex(triX + 2, triY - triOffset - 3, r, g, b, a)
    pointer.addItem(shadow)
    pointer.addItem(tri)
    slider.addItem(pointer)
    scale = float(legendW - 10)
    val = float(abs(value - minVal))
    dx = scale / 60
    numFrames = val / abs(maxVal - minVal) * 60
    es = twc.embedded.renderd.RenderScript.EffectSequencer(pointer)
    es.addEffect(twc.embedded.renderd.RenderScript.Fader(None, 0, 1, 10), 10)
    es.addEffect(twc.embedded.renderd.RenderScript.NullEffect(None), 10)
    if val > 0:
        es.addEffect(twc.embedded.renderd.RenderScript.Slider(None, dx), numFrames)
    page.addItem(es)
    xpos = dx * numFrames + triStartOffset
    return (slider, xpos)
    return


HORIZONTAL = 0
VERTICAL = 1

def gradientBox(width, height, rgbaValues, orientation=HORIZONTAL):
    numBoxes = len(rgbaValues) - 1
    if orientation == HORIZONTAL:
        w = float(width) / numBoxes
        h = height
    else:
        w = width
        h = float(height) / numBoxes
    cr = twc.embedded.renderd.RenderScript.CompositeRenderable()
    for i in range(numBoxes):
        (r, g, b, a) = rgbaValues[i]
        (r1, g1, b1, a1) = rgbaConvert(r, g, b, a)
        (r, g, b, a) = rgbaValues[i + 1]
        (r2, g2, b2, a2) = rgbaConvert(r, g, b, a)
        box = twc.embedded.renderd.RenderScript.Polygon()
        if orientation == HORIZONTAL:
            box.addVertex(0, 0, r1, g1, b1, a1)
            box.addVertex(0, h, r1, g1, b1, a1)
            box.addVertex(w, h, r2, g2, b2, a2)
            box.addVertex(w, 0, r2, g2, b2, a2)
            box.setPosition(i * w, 0)
        else:
            box.addVertex(0, 0, r1, g1, b1, a1)
            box.addVertex(0, h, r2, g2, b2, a2)
            box.addVertex(w, h, r2, g2, b2, a2)
            box.addVertex(w, 0, r1, g1, b1, a1)
            box.setPosition(0, i * h)
        cr.addItem(box)

    return cr
    return


def getCrawlFaders(w, r, g, b):
    crawlFade = twc.embedded.renderd.RenderScript.CompositeRenderable()
    ltri = twc.embedded.renderd.RenderScript.Polygon()
    ltri.addVertex(0, 0, r, g, b, 1)
    ltri.addVertex(10, 0, r, g, b, 1)
    ltri.addVertex(0, 30, r, g, b, 1)
    lfade = twc.embedded.renderd.RenderScript.Polygon()
    lfade.addVertex(10, 0, r, g, b, 1)
    lfade.addVertex(30, 0, r, g, b, 0)
    lfade.addVertex(20, 30, r, g, b, 0)
    lfade.addVertex(0, 30, r, g, b, 1)
    rtri = twc.embedded.renderd.RenderScript.Polygon()
    rtri.addVertex(w - 10, 30, r, g, b, 1)
    rtri.addVertex(w, 30, r, g, b, 1)
    rtri.addVertex(w, 0, r, g, b, 1)
    rfade = twc.embedded.renderd.RenderScript.Polygon()
    rfade.addVertex(w - 20, 0, r, g, b, 0)
    rfade.addVertex(w, 0, r, g, b, 1)
    rfade.addVertex(w - 10, 30, r, g, b, 1)
    rfade.addVertex(w - 30, 30, r, g, b, 0)
    crawlFade.addItem(ltri)
    crawlFade.addItem(lfade)
    crawlFade.addItem(rfade)
    crawlFade.addItem(rtri)
    return crawlFade
    return


def dataNotAvailable(page, xPos=None, yPos=None, text='Data Not Available'):
    (r, g, b, a) = rgbaConvert(235, 235, 235, 255)
    font = twc.embedded.renderd.RenderScript.TTFont('/rsrc/fonts/Frutiger_Bold_Cond', 34)
    gr = twc.embedded.renderd.RenderScript.Text(font, text)
    gr.setColor(r, g, b, a)
    if xPos is None:
        xPos = (720 - gr.size()[0]) / 2
    if yPos is None:
        yPos = (480 - gr.size()[1]) / 2
    gr.setPosition(xPos, yPos)
    page.addItem(gr)
    return gr
    return


SMALL_ICON = 0
MEDIUM_ICON = 1
LARGE_ICON = 2

def getSpanishIconPath(icon, size=0):
    if size == SMALL_ICON:
        iconPath = '/rsrc/icons_s'
    elif size == MEDIUM_ICON:
        iconPath = '/rsrc/icons_m'
    elif size == LARGE_ICON:
        iconPath = '/rsrc/icons_l'
    if os.path.exists('%s/spanish/%s.mv' % (iconPath, icon)):
        return '%s/spanish/%s' % (iconPath, icon)
    else:
        return '%s/%s' % (iconPath, icon)
    return


def formatObsSkyCondition(skyConditionCode, lang=SkyConditionCodes.english):
    global _EnglishObsSkyConditionTable
    global _SkyConditionInfo
    global _SpanishObsSkyConditionTable
    try:
        if lang == SkyConditionCodes.spanish:
            return _SpanishObsSkyConditionTable[skyConditionCode]
        else:
            return _EnglishObsSkyConditionTable[skyConditionCode]
    except:
        return _SkyConditionInfo('BlankIcon', '')

    return


def formatFcstSkyCondition(skyConditionCode, lang=SkyConditionCodes.english):
    global _EnglishFcstSkyConditionTable
    global _SpanishFcstSkyConditionTable
    try:
        if lang == SkyConditionCodes.spanish:
            return _SpanishFcstSkyConditionTable[skyConditionCode]
        else:
            return _EnglishFcstSkyConditionTable[skyConditionCode]
    except:
        return _SkyConditionInfo('BlankIcon', '')

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