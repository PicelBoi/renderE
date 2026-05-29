# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: renderUtil.py
# Compiled at: 2007-01-12 11:17:28
import glob, os, os.path, string, time, twc
from . import RenderControl, RenderScript

def rgbaConvert(r, g, b, a=255.0):
    return (r / 255.0, g / 255.0, b / 255.0, a / 255.0)
    return

SHIFT_BEVEL_BOX = False
bevelshift = None #keep this if you don't want to change the default color
#bevelshift = (0, 0, 0)
#format: (hue, saturation, value)
#ranges: 0-360, 0-100, 0-100
#these numbers are added to the normal values (hue will wrap around, others are clamped)

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


def paginateText(font, str, width, height, delimiter=' '):
    res = []
    totStrHeight = 0
    words = str.split(delimiter)
    if len(words) < 2:
        return [str]
    sh = font.leading()
    (s, words) = _getNextLine(font, words, width, delimiter)
    totStrHeight += sh
    while len(words):
        (tmp, words) = _getNextLine(font, words, width, delimiter)
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


def paginateIndentedText(font, fontColor, str, width, height, indentList, delimiter=None, includeDelimiter=0):
    strList = []
    pageList = []
    totStrHeight = 0
    offset = 0
    indent = 0
    i = 0
    delOffset = 0
    (r, g, b, a) = fontColor
    crList = []
    if delimiter is not None:
        delOffset = includeDelimiter * len(delimiter)
    (indent, offset) = _getIndentInfo(indentList, i)
    i += 1
    words = str.split(' ')
    sh = font.leading()
    if len(words) < 2:
        cr = RenderScript.CompositeRenderable()
        gr = RenderScript.Text(font, str)
        gr.setPosition(offset, height - sh)
        gr.setColor(r, g, b, a)
        cr.addItem(gr)
        crList.append(cr)
        return crList
    cr = RenderScript.CompositeRenderable()
    (s, words) = _getNextLine(font, words, width - indent, ' ')
    totStrHeight += sh
    strList.append(s)
    while len(words):
        (indent, offset) = _getIndentInfo(indentList, i)
        (tmp, words) = _getNextLine(font, words, width - indent, ' ')
        totStrHeight += sh
        if totStrHeight >= height:
            foundDelimiter = 0
            if delimiter is not None:
                j = len(strList) - 1
                while j > 0:
                    index = strList[j].rfind(delimiter)
                    if index != -1:
                        lineFrag = strList[j][index + delOffset:]
                        strList[j] = strList[j][:index + delOffset]
                        lineFragWords = []
                        k = len(strList) - 1
                        while k > j:
                            lineFragWords = strList[k].split(' ') + lineFragWords
                            del strList[k]
                            k = len(strList) - 1

                        lineFragWords = lineFrag.split(' ') + lineFragWords
                        words = lineFragWords + tmp.split(' ') + words
                        foundDelimiter = 1
                        break
                    else:
                        j -= 1

                if not foundDelimiter:
                    words = _reassembleTextList(tmp, words)
            else:
                words = _reassembleTextList(tmp, words)
            pageList.append(strList)
            strList = []
            i = 0
            (indent, offset) = _getIndentInfo(indentList, i)
            (tmp, words) = _getNextLine(font, words, width - indent, ' ')
            totStrHeight = sh
        strList.append(tmp)
        i += 1

    if len(strList):
        pageList.append(strList)
        strList = []
    for page in pageList:
        cr = RenderScript.CompositeRenderable()
        ypos = height - sh
        i = 0
        for line in page:
            (indent, offset) = _getIndentInfo(indentList, i)
            gr = RenderScript.Text(font, line)
            gr.setPosition(offset, ypos)
            gr.setColor(r, g, b, a)
            cr.addItem(gr)
            ypos -= sh
            i += 1

        crList.append(cr)

    return crList
    return


def _getNextLine(font, words, width, delimiter):
    str = words[0]
    words = words[1:]
    (sw, sh) = font.stringSize(str)
    while len(words):
        temp = str + '%s%s' % (delimiter, words[0])
        (sw, sh) = font.stringSize(temp)
        if sw >= width:
            break
        str = temp
        words = words[1:]

    return (str, words)
    return


def _getIndentInfo(indentList, index):
    if index < len(indentList):
        (indent, side) = indentList[index]
        if not side:
            offset = indent
        else:
            offset = 0
    else:
        indent = 0
        offset = 0
    return (indent, offset)
    return


def _reassembleTextList(str, wordList):
    tmpWords = str.split(' ')
    words = tmpWords + wordList
    return words
    return


def animationLoop(page, imageList, repeat=1, loopLimit=0):
    count = 0
    for grData in imageList:
        gr = grData[0]
        if count > 0:
            gr.setVisibility(0)
        else:
            gr.setVisibility(1)
        es = RenderScript.EffectSequencer(gr, repeat, loopLimit)
        for ii in range(len(imageList)):
            duration = imageList[ii][1]
            es.addEffect(RenderScript.SetVisibility(None, ii is count), duration)

        page.addItem(gr)
        page.addItem(es)
        count = count + 1

    return


def sequenceOnPage(page, grSet, delay=30, repeat=0):
    count = 0
    for grList in grSet:
        for gr in grList:
            es = RenderScript.EffectSequencer(gr, repeat)
            if count > 0:
                gr.setVisibility(0)
            else:
                gr.setVisibility(1)
            for i in range(len(grSet)):
                es.addEffect(RenderScript.SetVisibility(None, i is count), delay)

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
    slider = RenderScript.CompositeRenderable()
    legend = gradientBox(legendW, legendH, rgbaVals)
    slider.addItem(legend)
    if scaleIndex is not None:
        slider.addItem(scaleIndex)
    pointer = RenderScript.CompositeRenderable()
    triStartOffset = 3
    tri = RenderScript.Polygon()
    triX = 5
    triY = legendH + triStartOffset
    triOffset = 21
    (r, g, b, a) = rgbaConvert(235, 235, 235, 255)
    tri.addVertex(triX - triOffset / 2, triY, r, g, b, a)
    tri.addVertex(triX + triOffset / 2, triY, r, g, b, a)
    tri.addVertex(triX, triY - triOffset, r, g, b, a)
    shadow = RenderScript.Polygon()
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
    es = RenderScript.EffectSequencer(pointer)
    es.addEffect(RenderScript.Fader(None, 0, 1, 10), 10)
    es.addEffect(RenderScript.NullEffect(None), 10)
    if val > 0:
        es.addEffect(RenderScript.Slider(None, dx), numFrames)
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
    cr = RenderScript.CompositeRenderable()
    for i in range(numBoxes):
        (r, g, b, a) = rgbaValues[i]
        (r1, g1, b1, a1) = rgbaConvert(r, g, b, a)
        (r, g, b, a) = rgbaValues[i + 1]
        (r2, g2, b2, a2) = rgbaConvert(r, g, b, a)
        box = RenderScript.Polygon()
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
    crawlFade = RenderScript.CompositeRenderable()
    ltri = RenderScript.Polygon()
    ltri.addVertex(0, 0, r, g, b, 1)
    ltri.addVertex(10, 0, r, g, b, 1)
    ltri.addVertex(0, 30, r, g, b, 1)
    lfade = RenderScript.Polygon()
    lfade.addVertex(10, 0, r, g, b, 1)
    lfade.addVertex(30, 0, r, g, b, 0)
    lfade.addVertex(20, 30, r, g, b, 0)
    lfade.addVertex(0, 30, r, g, b, 1)
    rtri = RenderScript.Polygon()
    rtri.addVertex(w - 10, 30, r, g, b, 1)
    rtri.addVertex(w, 30, r, g, b, 1)
    rtri.addVertex(w, 0, r, g, b, 1)
    rfade = RenderScript.Polygon()
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


TRANS_BLUE = 0
RED = 1
YELLOW = 2
GREEN = 3

def clamp(n, lower, upper):
    return max(min(n, upper), lower)

def shiftGradient(grad, hue, sat, val):
    import colorsys as cs
    new = []
    for col in grad:
        a = col[3]
        h, s, v = cs.rgb_to_hsv(*[c/255 for c in col[:3]])
        h += (hue/360)
        h %= 1
        s = clamp((s+sat/100), 0, 1)
        v = clamp((v+val/100), 0, 1)
        r, g, b = cs.hsv_to_rgb(h, s, v)
        new.append((r*255, g*255, b*255, a))
    return new

modern = (twc.personality == "Texarkana")
def getBevelBox(w, h, color=None, debug=False, shift=bevelshift):
    bevelWidth = 3
    if color is None or len(color) != 5:
        color = [[(113, 143, 178, 255), (59, 98, 148, 255)], [(24, 51, 92, 255), (15, 34, 67, 255)], [(39, 79, 133, 255), (61, 100, 150, 255)], [(14, 32, 65, 255), (27, 57, 107, 255)], [(20, 51, 141, 153), (64, 91, 153, 153)]]
    tombstone = RenderScript.CompositeRenderable(debug)
    topEdge = RenderScript.Polygon()
    bottomEdge = RenderScript.Polygon()
    leftEdge = RenderScript.Polygon()
    rightEdge = RenderScript.Polygon()
    centerBox1 = RenderScript.Polygon()
    if not modern:
        centerBox2 = RenderScript.Polygon()
    
    colorTop = [(113, 143, 178, 255), (59, 98, 148, 255)]
    colorBottom = [(24, 51, 92, 255), (15, 34, 67, 255)]
    colorLeft = [(39, 79, 133, 255), (61, 100, 150, 255)]
    colorRight = [(14, 32, 65, 255), (27, 57, 107, 255)]
    colorBox = [(20, 51, 141, 153), (64, 91, 153, 153)]
    
    if modern:
        c1 = (80, 139, 200, 255)
        c2 = (80, 139, 200, 0)
        
        c5 = (82, 121, 161, 255)
        c6 = (82, 121, 161, 0)
        
        c3 = (36, 72, 120, 140)
        c4 = (25, 50, 100, 140)
        colorBox = [c3, c4]
        colorRight = [c1, c2, c5, c6]
        colorLeft = [c1, c2, c5, c6]
        colorTop = [c1, c2, c5, c6]
        colorBottom = [c1, c2, c5, c6]
        bevelWidth = 6
    
    if shift:
        colorTop = shiftGradient(colorTop, *shift)
        colorBottom = shiftGradient(colorBottom, *shift)
        colorLeft = shiftGradient(colorLeft, *shift)
        colorRight = shiftGradient(colorRight, *shift)
        colorBox = shiftGradient(colorBox, *shift)
    
    if not modern:
        (r, g, b, a) = colorTop[0]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        topEdge.addVertex(bevelWidth, 0, r, g, b, a)
        topEdge.addVertex(0, bevelWidth, r, g, b, a)
        (r, g, b, a) = colorTop[1]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        topEdge.addVertex(w, bevelWidth, r, g, b, a)
        topEdge.addVertex(w - bevelWidth, 0, r, g, b, a)
        topEdge.setPosition(0, h - bevelWidth)
        
        (r, g, b, a) = colorBottom[0]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        bottomEdge.addVertex(0, 0, r, g, b, a)
        bottomEdge.addVertex(bevelWidth, bevelWidth, r, g, b, a)
        (r, g, b, a) = colorBottom[1]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        bottomEdge.addVertex(w - bevelWidth, bevelWidth, r, g, b, a)
        bottomEdge.addVertex(w, 0, r, g, b, a)
        
        (r, g, b, a) = colorLeft[0]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        leftEdge.addVertex(0, 0, r, g, b, a)
        leftEdge.addVertex(bevelWidth, bevelWidth, r, g, b, a)
        (r, g, b, a) = colorLeft[1]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        leftEdge.addVertex(bevelWidth, h - bevelWidth, r, g, b, a)
        leftEdge.addVertex(0, h, r, g, b, a)
        
        (r, g, b, a) = colorRight[0]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        rightEdge.addVertex(0, bevelWidth, r, g, b, a)
        rightEdge.addVertex(bevelWidth, 0, r, g, b, a)
        (r, g, b, a) = colorRight[1]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        rightEdge.addVertex(bevelWidth, h, r, g, b, a)
        rightEdge.addVertex(0, h - bevelWidth, r, g, b, a)
        rightEdge.setPosition(w - bevelWidth, 0)

        
        tombstone.addItem(topEdge)
        tombstone.addItem(bottomEdge)
        tombstone.addItem(leftEdge)
        tombstone.addItem(rightEdge)
    
        (r, g, b, a) = colorBox[0]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        centerBox1.addVertex(0, 0, r, g, b, a)
        centerBox1.addVertex(w - bevelWidth * 2, 0, r, g, b, a)
        (r, g, b, a) = colorBox[1]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        centerBox1.addVertex(w - bevelWidth * 2, h / 2 - bevelWidth, r, g, b, a)
        centerBox1.addVertex(0, h / 2 - bevelWidth, r, g, b, a)
        centerBox1.setPosition(bevelWidth, bevelWidth)
        
        
        (r, g, b, a) = colorBox[1]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        centerBox2.addVertex(0, 0, r, g, b, a)
        centerBox2.addVertex(w - bevelWidth * 2, 0, r, g, b, a)
        (r, g, b, a) = colorBox[0]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        centerBox2.addVertex(w - bevelWidth * 2, h / 2 - bevelWidth, r, g, b, a)
        centerBox2.addVertex(0, h / 2 - bevelWidth, r, g, b, a)
        centerBox2.setPosition(bevelWidth, h / 2)
    
        tombstone.addItem(centerBox1)
        tombstone.addItem(centerBox2)
    else:
        (r1, g1, b1, a1) = colorLeft[0] #
        (r2, g2, b2, a2) = colorLeft[1]
        (r3, g3, b3, a3) = colorLeft[2] #
        (r4, g4, b4, a4) = colorLeft[3]
        
        
        (r1, g1, b1, a1) = rgbaConvert(r1, g1, b1, a1)
        (r2, g2, b2, a2) = rgbaConvert(r2, g2, b2, a2)
        (r3, g3, b3, a3) = rgbaConvert(r3, g3, b3, a3)
        (r4, g4, b4, a4) = rgbaConvert(r4, g4, b4, a4)
        
        (r, g, b, a) = colorBox[1]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        centerBox1.addVertex(0, 0, r, g, b, a)
        centerBox1.addVertex(w, 0, r, g, b, a)
        (r, g, b, a) = colorBox[0]
        (r, g, b, a) = rgbaConvert(r, g, b, a)
        centerBox1.addVertex(w, h, r, g, b, a)
        centerBox1.addVertex(0, h, r, g, b, a)
        centerBox1.setPosition(0, 0)
        tombstone.addItem(centerBox1)
        
        inset = 1
        topEdge.setPosition(0, h - bevelWidth)
        topEdge.addVertex(inset, bevelWidth - inset, r1, g1, b1, a1)
        topEdge.addVertex(0, bevelWidth, r1, g1, b1, a1)
        topEdge.addVertex(w, bevelWidth, r1, g1, b1, a1)
        topEdge.addVertex(w - inset, bevelWidth - inset, r1, g1, b1, a1)
        topEdge.addVertex(w - bevelWidth, 0, r2, g2, b2, a2)
        topEdge.addVertex(bevelWidth, 0, r2, g2, b2, a2)
        
        bottomEdge.addVertex(w - inset, inset, r3, g3, b3, a3)
        bottomEdge.addVertex(w, 0, r3, g3, b3, a3)
        bottomEdge.addVertex(0, 0, r3, g3, b3, a3)
        bottomEdge.addVertex(inset, inset, r3, g3, b3, a3)
        bottomEdge.addVertex(bevelWidth, bevelWidth, r4, g4, b4, a4)
        bottomEdge.addVertex(w - bevelWidth, bevelWidth, r4, g4, b4, a4)

        
        leftEdge.addVertex(inset, h - inset, r1, g1, b1, a1)
        leftEdge.addVertex(0, h, r1, g1, b1, a1)
        leftEdge.addVertex(0, 0, r3, g3, b3, a3)
        leftEdge.addVertex(inset, inset, r3, g3, b3, a3)
        leftEdge.addVertex(bevelWidth, bevelWidth, r4, g4, b4, a4)
        leftEdge.addVertex(bevelWidth, h - bevelWidth, r2, g2, b2, a2)
        
        rightEdge.addVertex(bevelWidth - inset, inset, r3, g3, b3, a3)
        rightEdge.addVertex(bevelWidth, 0, r3, g3, b3, a3)
        rightEdge.addVertex(bevelWidth, h, r1, g1, b1, a1)
        rightEdge.addVertex(bevelWidth - inset, h - inset, r1, g1, b1, a1)
        rightEdge.addVertex(0, h - bevelWidth, r2, g2, b2, a2)
        rightEdge.addVertex(0, bevelWidth, r4, g4, b4, a4)
        rightEdge.setPosition(w - bevelWidth, 0)

        
        tombstone.addItem(topEdge)
        tombstone.addItem(bottomEdge)
        tombstone.addItem(leftEdge)
        tombstone.addItem(rightEdge)
    
    return tombstone
    return


def fadeInOut(p, gr, totalDuration, fadeInDuration=5, fadeOutDuration=5):
    fade = RenderScript.EffectSequencer(gr)
    if fadeInDuration:
        fade.addEffect(RenderScript.Fader(None, 0, 1, fadeInDuration), fadeInDuration)
    if totalDuration > fadeInDuration + fadeOutDuration:
        fade.addEffect(RenderScript.NullEffect(None), totalDuration - fadeInDuration - fadeOutDuration)
    if fadeOutDuration:
        fade.addEffect(RenderScript.Fader(None, 1, 0, fadeOutDuration), fadeOutDuration)
    #print(fade.effects)
    p.addItem(fade)
    return

def slideInOut(p, gr, totalDuration, fadeInDuration=5, fadeOutDuration=5, moveDistance=720, delay=0):
    fade = RenderScript.EffectSequencer(gr)
    if delay:
        fade.addEffect(RenderScript.NullEffect(None), delay)
    if fadeInDuration:
        fade.addEffect(RenderScript.Slider(None, moveDistance/fadeInDuration, 0), fadeInDuration)
    if totalDuration > fadeInDuration + fadeOutDuration:
        fade.addEffect(RenderScript.NullEffect(None), totalDuration - fadeInDuration - fadeOutDuration - delay)
    if fadeOutDuration:
        fade.addEffect(RenderScript.Slider(None, -moveDistance/fadeOutDuration, 0), fadeOutDuration)
    #print(fade.effects)
    p.addItem(fade)
    return

