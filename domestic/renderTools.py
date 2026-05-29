# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: renderTools.py
# Compiled at: 2007-01-12 11:33:26
from twc.embedded.renderd.renderUtil import rgbaConvert
from twc.embedded.renderd.RenderScript import Box
from twc.embedded.renderd.RenderScript import CompositeRenderable
from twc.embedded.renderd.RenderScript import EffectSequencer
from twc.embedded.renderd.RenderScript import Polygon
from twc.embedded.renderd.RenderScript import Fader
from twc.embedded.renderd.RenderScript import Slider
from twc.embedded.renderd.RenderScript import NullEffect
from twc.embedded.renderd.RenderScript import SetVisibility
from twc.embedded.renderd.RenderScript import SetPosition
from twc.embedded.renderd.RenderScript import Text
from twc.embedded.renderd.RenderScript import TTFont
from twc.embedded.renderd.RenderScript import TIFF_Image
from twc.embedded.renderd.RenderScript import Clipper
import twc
from functools import reduce

def apply(func, args, kwargs=None):
    return func(*args) if kwargs is None else func(*args, **kwargs)

def sequenceOnPage(page, grSet, delayList, repeat=0):
    pageCount = len(grSet)
    count = 0
    delay = 1
    totFrames = reduce((lambda a, b: a + b), delayList)
    for grList in grSet:
        for gr in grList:
            es = EffectSequencer(gr, repeat=repeat)
            if count == 0:
                es.addEffect(SetVisibility(None, 1), delayList[count] - 5)
                es.addEffect(Fader(None, 1, 0, 5), 5)
                es.addEffect(SetVisibility(None, 0), 1)
                es.addEffect(Fader(None, 0, 1, 1), 1)
                es.addEffect(NullEffect(None), totFrames - delayList[count] + 3)
            elif count == pageCount - 1:
                es.addEffect(SetVisibility(None, 0), delay)
                es.addEffect(Fader(None, 1, 0, 1), 1)
                es.addEffect(SetVisibility(None, 1), 1)
                es.addEffect(Fader(None, 0, 1, 5), 5)
                es.addEffect(NullEffect(None), totFrames - delay + 7)
            else:
                es.addEffect(SetVisibility(None, 0), delay)
                es.addEffect(Fader(None, 1, 0, 1), 1)
                es.addEffect(SetVisibility(None, 1), 1)
                es.addEffect(Fader(None, 0, 1, 5), 5)
                es.addEffect(NullEffect(None), delayList[count] - 12)
                es.addEffect(Fader(None, 1, 0, 5), 5)
                es.addEffect(SetVisibility(None, 0), 1)
                es.addEffect(Fader(None, 0, 1, 1), 1)
                es.addEffect(NullEffect(None), totFrames - delayList[count] + delay + 2)
            page.addItem(gr)
            page.addItem(es)

        delay = delayList[count] + delay
        count = count + 1

    return


def dataNotAvailable(page, xPos=None, yPos=None, text='Data Not Available', noDataBar=0, fadeDuration=5, displayDuration=0, rgba=None):
    print("DNA", f"_{twc.personality}_")
    if twc.personalityCode == 3:
        print("FlatrockDNA")
        if rgba:
            (r, g, b, a) = rgbaConvert(*rgba)
        else:
            (r, g, b, a) = rgbaConvert(25, 25, 25, 255)
        font = TTFont('/rsrc/fonts/Interstate-Bold', 30, t=30, shadow=0)
        gr = Text(font, text)
        gr.setColor(r, g, b, a)
        if xPos is None:
            xPos = (720 - gr.size()[0]) / 2
        if yPos is None:
            yPos = (480 - gr.size()[1]) / 2
        gr.setPosition(xPos, yPos)
        renderObj = gr
        if noDataBar:
            cr = CompositeRenderable()
            bb = Box()
            bb.setSize(720, 31)
            bb.setPosition(0, yPos - 6)
            (r, g, b, a) = rgbaConvert(20, 20, 20, 255)
            bb.setColor(r, g, b, a)
            cr.addItem(bb)
            cr.addItem(gr)
            renderObj = cr
        if displayDuration > 0:
            page.addItem(renderObj)
            totalDelay = 2 * fadeDuration + 20
            dur = displayDuration - totalDelay
            ef = EffectSequencer(renderObj)
            ef.addEffect(SetVisibility(None, 0), 1)
            ef.addEffect(Fader(None, 1, 0, 1), 1)
            ef.addEffect(SetVisibility(None, 1), 1)
            ef.addEffect(NullEffect(None), 7)
            ef.addEffect(Fader(None, 0, 1, fadeDuration), fadeDuration)
            ef.addEffect(NullEffect(None), dur)
            ef.addEffect(Fader(None, 1, 0, fadeDuration), fadeDuration)
            page.addItem(ef)
        return renderObj
    elif twc.personalityCode < 3:
        (r, g, b, a) = rgbaConvert(212, 212, 50, 255)
        font = TTFont('/rsrc/fonts/Interstate-Bold', 30, t=30)
        gr = Text(font, text)
        gr.setColor(r, g, b, a)
        print(gr.size())
        if xPos is None:
            xPos = (720 - gr.size()[0]) / 2
        if yPos is None:
            yPos = (480 - gr.size()[1]) / 2
        gr.setPosition(xPos, yPos)
        renderObj = gr
        if noDataBar:
            cr = CompositeRenderable()
            bb = Box()
            bb.setSize(720, 31)
            bb.setPosition(0, yPos - 6)
            (r, g, b, a) = rgbaConvert(20, 20, 20, 255)
            bb.setColor(r, g, b, a)
            cr.addItem(bb)
            cr.addItem(gr)
            renderObj = cr
        if displayDuration > 0:
            page.addItem(renderObj)
            totalDelay = 2 * fadeDuration + 20
            dur = displayDuration - totalDelay
            ef = EffectSequencer(renderObj)
            ef.addEffect(SetVisibility(None, 0), 1)
            ef.addEffect(Fader(None, 1, 0, 1), 1)
            ef.addEffect(SetVisibility(None, 1), 1)
            ef.addEffect(NullEffect(None), 7)
            ef.addEffect(Fader(None, 0, 1, fadeDuration), fadeDuration)
            ef.addEffect(NullEffect(None), dur)
            ef.addEffect(Fader(None, 1, 0, fadeDuration), fadeDuration)
            page.addItem(ef)
        return renderObj

modern = (twc.personality == "Texarkana")

def createTitleBarModern(string1, string2):
    vBevSize = 3
    hBevSize = 3
    padV = 14
    padH = 12
    bg1X = vBevSize - 3
    bg1Y = hBevSize
    bg1W = 0
    tr1X = bg1X + padH
    tr1Y = bg1Y + padV
    titleFont1 = TTFont('/rsrc/fonts/Interstate-Bold', 36, 0)
    titleFont2 = TTFont('/rsrc/fonts/Interstate-Bold', 30 + 6, 0)
    crTitleTxt = CompositeRenderable()
    crTitleTxt2 = CompositeRenderable()
    crTitleBev = CompositeRenderable()
    crTitleBev2 = CompositeRenderable()
    
    bgSide = 10
    bgSide2 = 8
    bgInset = 3
    bg1H = 50
    #bg2H = 40
    bg2H = 50
    bg2O = 10
    
    bg2V = 5
    bg2TV = 2
    
    bg2V = 0
    bg2TV = 0
    
    if string1:
        tr1 = Text(titleFont1, string1)
        tr1w, tr1h = tr1.size()
        if string2:
            tr2 = Text(titleFont2, string2)
            tr2w, tr2h = tr2.size()
            pp = Polygon()
            (r, g, b, a) = rgbaConvert(20, 20, 20, 255)
            pp.addVertex(bgSide, 0, r, g, b, a)
            pp.addVertex(0, bgSide, r, g, b, a)
            pp.addVertex(0, bg2H, r, g, b, a)
            pp.addVertex(tr2w+padH*2-bgSide+bg2O, bg2H, r, g, b, a)
            pp.addVertex(tr2w+padH*2+bg2O, bg2H-bgSide, r, g, b, a)
            pp.addVertex(tr2w+padH*2+bg2O, 0, r, g, b, a)
            pp.setPosition(bg1X+tr1w, bg1Y+bg2V)

            crTitleBev2.addItem(pp)
            
            pp = Polygon()
            (r, g, b, a) = rgbaConvert(235, 235, 235, 255)
            (r2, g2, b2, a2) = rgbaConvert(235, 235, 235, 127)
            pp.addVertex(bgSide2, 0, r2, g2, b2, a2)
            pp.addVertex(0, bgSide2, r2, g2, b2, a2)
            pp.addVertex(0, bg2H-bgInset*2, r, g, b, a)
            pp.addVertex(tr2w+padH*2-bgSide2-bgInset*2+bg2O, bg2H-bgInset*2, r, g, b, a)
            pp.addVertex(tr2w+padH*2-bgInset*2+bg2O, bg2H-bgSide2-bgInset*2, r, g, b, a)
            pp.addVertex(tr2w+padH*2-bgInset*2+bg2O, 0, r2, g2, b2, a2)
            pp.setPosition(bg1X+bgInset+tr1w, bg1Y+bgInset+bg2V)
            
            crTitleBev2.addItem(pp)
            
            tr2.setPosition(tr1X+tr1w+bgInset+bg2O, tr1Y+bg2TV)
            (r, g, b, a) = rgbaConvert(20, 20, 20, 255)
            tr2.setColor(r, g, b, a)
            crTitleTxt2.addItem(tr2)
        pp = Polygon()
        (r, g, b, a) = rgbaConvert(80, 139, 200, 255)
        (r2, g2, b2, a2) = rgbaConvert(82, 121, 161, 255)
        pp.addVertex(bgSide, 0, r2, g2, b2, a2)
        pp.addVertex(0, bgSide, r2, g2, b2, a2)
        pp.addVertex(0, bg1H, r, g, b, a)
        pp.addVertex(tr1w+padH*2, bg1H, r, g, b, a)
        pp.addVertex(tr1w+padH*2, 0, r2, g2, b2, a2)
        pp.setPosition(bg1X, bg1Y)

        crTitleBev.addItem(pp)
        
        pp = Polygon()
        (r, g, b, a) = rgbaConvert(20, 20, 20, 255)
        (r2, g2, b2, a2) = rgbaConvert(20, 20, 20, 192)
        pp.addVertex(bgSide2, 0, r2, g2, b2, a2)
        pp.addVertex(0, bgSide2, r2, g2, b2, a2)
        pp.addVertex(0, bg1H-bgInset*2, r, g, b, a)
        pp.addVertex(tr1w+padH*2-bgInset*2, bg1H-bgInset*2, r, g, b, a)
        pp.addVertex(tr1w+padH*2-bgInset*2, 0, r2, g2, b2, a2)
        pp.setPosition(bg1X+bgInset, bg1Y+bgInset)
        
        crTitleBev.addItem(pp)
        
        tr1.setPosition(tr1X, tr1Y)
        (r, g, b, a) = rgbaConvert(235, 235, 235, 255)
        tr1.setColor(r, g, b, a)
        crTitleTxt.addItem(tr1)
    return (crTitleBev, crTitleBev2, crTitleTxt, crTitleTxt2)

def createTitleBar(string1, string2, s1BkgColor, s2BkgColor, s1TxtColor, s2TxtColor, s1ShdColor, s2ShdColor):
    if modern:
        return createTitleBarModern(string1, string2)
    (R, G, B, A) = s1ShdColor
    (r, g, b, a) = rgbaConvert(R, G, B, A)
    titleFont1 = TTFont('/rsrc/fonts/Interstate-Bold', 36, t=20, sr=r, sb=b, sg=g, sa=a)
    (R, G, B, A) = s2ShdColor
    (r, g, b, a) = rgbaConvert(R, G, B, A)
    titleFont2 = TTFont('/rsrc/fonts/Interstate-Bold', 36, t=20, sr=r, sb=b, sg=g, sa=a)
    vBevSize = 3
    hBevSize = 3
    padV = 8
    padH = 8
    bg1X = vBevSize
    bg1Y = hBevSize
    bg1W = 0
    tr1X = bg1X + padH
    tr1Y = bg1Y + padV
    tr1W = 0
    if string1:
        bg1W = titleFont1.stringWidth(string1) + 20
    if string2:
        bg2W = 564
        bg2X = bg1X + bg1W
        bg2Y = hBevSize
        tr2X = bg2X + 3
        tr2Y = hBevSize + padV
    crTitleTxt = CompositeRenderable()
    crTitleBev = CompositeRenderable()
    (r, g, b, a) = rgbaConvert(255, 255, 255, 0)
    V1 = (0, hBevSize + 52, r, b, g, a)
    V5 = (520, 0, r, g, b, a)
    V6 = (520, hBevSize, r, g, b, a)
    V10 = (vBevSize, hBevSize + 52, r, b, g, a)
    (r, g, b, a) = rgbaConvert(221, 221, 221, int(255 * 0.62))
    V2 = (0, hBevSize + 12, r, b, g, a)
    V4 = (260, 0, r, g, b, a)
    V7 = (260, hBevSize, r, g, b, a)
    V9 = (vBevSize, hBevSize + 12, r, b, g, a)
    (r, g, b, a) = rgbaConvert(212, 212, 212, int(255 * 0.8))
    V3 = (0, 0, r, g, b, a)
    V8 = (vBevSize, hBevSize, r, g, b, a)
    pp = Polygon()
    apply(pp.addVertex, V1)
    apply(pp.addVertex, V2)
    apply(pp.addVertex, V3)
    apply(pp.addVertex, V8)
    apply(pp.addVertex, V9)
    apply(pp.addVertex, V10)
    crTitleBev.addItem(pp)
    pp = Polygon()
    apply(pp.addVertex, V3)
    apply(pp.addVertex, V4)
    apply(pp.addVertex, V5)
    apply(pp.addVertex, V6)
    apply(pp.addVertex, V7)
    apply(pp.addVertex, V8)
    crTitleBev.addItem(pp)
    if string1:
        (R, G, B, A) = s1BkgColor
        if string2:
            (r, g, b, a) = rgbaConvert(R, G, B, A)
            V1 = (bg1X, bg1Y, r, g, b, a)
            V2 = (bg1X + bg1W, bg1Y, r, g, b, a)
            (r, g, b, a) = rgbaConvert(R, G, B, 0)
            V7 = (bg1X, bg1Y + 60, r, g, b, a)
            V8 = (bg1X + bg1W, bg1Y + 60, r, g, b, a)
            pp = Polygon()
            apply(pp.addVertex, V1)
            apply(pp.addVertex, V2)
            apply(pp.addVertex, V8)
            apply(pp.addVertex, V7)
            crTitleTxt.addItem(pp)
        else:
            (r, g, b, a) = rgbaConvert(R, G, B, A)
            V1 = (bg1X, bg1Y, r, g, b, a)
            (r, g, b, a) = rgbaConvert(R, G, B, A * 0.63)
            V2 = (bg1X + 255, bg1Y, r, g, b, a)
            V4 = (bg1X, bg1Y + 46, r, g, b, a)
            (r, g, b, a) = rgbaConvert(R, G, B, A * 0.25)
            V5 = (bg1X + 255, bg1Y + 46, r, g, b, a)
            (r, g, b, a) = rgbaConvert(R, G, B, A * 0.03)
            V3 = (bg1X + 520, bg1Y, r, g, b, a)
            V7 = (bg1X, bg1Y + 72, r, g, b, a)
            (r, g, b, a) = rgbaConvert(R, G, B, A * 0.025)
            V6 = (bg1X + 520, bg1Y + 46, r, g, b, a)
            V8 = (bg1X + 115, bg1Y + 72, r, g, b, a)
            (r, g, b, a) = rgbaConvert(R, G, B, 0)
            V9 = (bg1X + 520, bg1Y + 72, r, g, b, a)
            pp = Polygon()
            apply(pp.addVertex, V1)
            apply(pp.addVertex, V2)
            apply(pp.addVertex, V5)
            apply(pp.addVertex, V4)
            crTitleTxt.addItem(pp)
            pp = Polygon()
            apply(pp.addVertex, V2)
            apply(pp.addVertex, V3)
            apply(pp.addVertex, V6)
            apply(pp.addVertex, V5)
            crTitleTxt.addItem(pp)
            pp = Polygon()
            apply(pp.addVertex, V4)
            apply(pp.addVertex, V5)
            apply(pp.addVertex, V8)
            apply(pp.addVertex, V7)
            crTitleTxt.addItem(pp)
            pp = Polygon()
            apply(pp.addVertex, V5)
            apply(pp.addVertex, V6)
            apply(pp.addVertex, V9)
            apply(pp.addVertex, V8)
            crTitleTxt.addItem(pp)
        tr1 = Text(titleFont1, string1)
        tr1.setPosition(tr1X, tr1Y)
        (R, G, B, A) = s1TxtColor
        (r, g, b, a) = rgbaConvert(R, G, B, A)
        tr1.setColor(r, g, b, a)
        crTitleTxt.addItem(tr1)
    if string2:
        (R, G, B, A) = s2BkgColor
        (r, g, b, a) = rgbaConvert(R, G, B, A)
        V1 = (bg2X, bg2Y, r, g, b, a)
        (r, g, b, a) = rgbaConvert(R, G, B, A * 0.54)
        V2 = (bg2X + 425, bg2Y, r, g, b, a)
        V4 = (bg2X, bg2Y + 46, r, g, b, a)
        (r, g, b, a) = rgbaConvert(R, G, B, A * 0.32)
        V5 = (bg2X + 425, bg2Y + 46, r, g, b, a)
        (r, g, b, a) = rgbaConvert(R, G, B, 0)
        V3 = (bg2X + 515, bg2Y, r, g, b, a)
        V6 = (bg2X + 515, bg2Y + 46, r, g, b, a)
        V7 = (bg2X, bg2Y + 77, r, g, b, a)
        V8 = (bg2X + 425, bg2Y + 77, r, g, b, a)
        V9 = (bg2X + 515, bg2Y + 77, r, g, b, a)
        pp = Polygon()
        apply(pp.addVertex, V1)
        apply(pp.addVertex, V2)
        apply(pp.addVertex, V5)
        apply(pp.addVertex, V4)
        crTitleTxt.addItem(pp)
        pp = Polygon()
        apply(pp.addVertex, V2)
        apply(pp.addVertex, V3)
        apply(pp.addVertex, V6)
        apply(pp.addVertex, V5)
        crTitleTxt.addItem(pp)
        pp = Polygon()
        apply(pp.addVertex, V4)
        apply(pp.addVertex, V5)
        apply(pp.addVertex, V8)
        apply(pp.addVertex, V7)
        crTitleTxt.addItem(pp)
        pp = Polygon()
        apply(pp.addVertex, V5)
        apply(pp.addVertex, V6)
        apply(pp.addVertex, V9)
        apply(pp.addVertex, V8)
        crTitleTxt.addItem(pp)
        tr2 = Text(titleFont2, string2)
        tr2.setPosition(tr2X, tr2Y)
        (R, G, B, A) = s2TxtColor
        (r, g, b, a) = rgbaConvert(R, G, B, A)
        tr2.setColor(r, g, b, a)
        crTitleTxt.addItem(tr2)
    return (crTitleBev, crTitleTxt)
    return

def createSDRefreshTitleBar(titleString, txtColor, background=None):
    (R, G, B, A) = txtColor
    (r, g, b, a) = rgbaConvert(R, G, B, A)
    crTitleTxt = CompositeRenderable()
    if background:
        bkgdFile = twc.findRsrc('/backgrounds/%s' % background, 'tif', 0)
        bkgdImage = TIFF_Image(bkgdFile)
        crTitleTxt.addItem(bkgdImage)
        bkgdImage.setPosition(0, 0)
    titleFont = TTFont('/rsrc/fonts/Interstate-Bold', 36, t=20, sr=r, sb=b, sg=g, sa=a, shadow=0)
    trTextTitle = Text(titleFont, titleString)
    trTextTitle.setColor(r, g, b, a)
    tr1X = tr1Y = 0
    crTitleTxt.addItem(trTextTitle)
    trTextTitle.setPosition(11, 11)
    return crTitleTxt
    return

def drawMapBanner(page):
    """Draw black map banner."""
    pp = Polygon()
    (r, g, b, a) = rgbaConvert(20, 20, 20, 255)
    pp.addVertex(52, 384, r, g, b, a)
    pp.addVertex(52, 405, r, g, b, a)
    pp.addVertex(245, 405, r, g, b, a)
    pp.addVertex(245, 384, r, g, b, a)
    page.addItem(pp)
    pp = Polygon()
    (r, g, b, a) = rgbaConvert(20, 20, 20, 179)
    pp.addVertex(245, 384, r, g, b, a)
    pp.addVertex(245, 405, r, g, b, a)
    pp.addVertex(500, 405, r, g, b, a)
    pp.addVertex(494, 384, r, g, b, a)
    page.addItem(pp)
    return


def drawValidTimeSlider(page, lastImageDuration, imageDuration, imageCount, timeScale, timeScaleOffset, loopLimit):
    """Draw timeBarSlider for all animated map products."""
    (xPos, yPos) = (444, 384)
    color = (147, 96, 193, 255)
    slider = CompositeRenderable()
    (r, g, b, a) = rgbaConvert(color[0], color[1], color[2], color[3])
    pp = Polygon()
    pp.addVertex(xPos, yPos, r, g, b, a * 0.2)
    pp.addVertex(xPos + 20, yPos, r, g, b, a * 0.8)
    pp.addVertex(xPos + 50, yPos, r, g, b, a)
    pp.addVertex(xPos + 56, yPos + 21, r, g, b, a)
    pp.addVertex(xPos + 20, yPos + 21, r, g, b, a * 0.8)
    pp.addVertex(xPos, yPos + 21, r, g, b, a * 0.2)
    slider.addItem(pp)
    page.addItem(slider)
    seq = EffectSequencer(slider, 1, loopLimit)
    seq.addEffect(SetPosition(None, -155, 0), 1)
    distance = 155.0
    time = (imageCount - 1) * imageDuration
    speed = distance / time
    seq.addEffect(Slider(None, speed), time)
    page.addItem(seq)
    seq.addEffect(NullEffect(), lastImageDuration - 1)
    legendStartPos = 306
    f = TTFont('/rsrc/fonts/Interstate-BlackItalic', 20)
    for ii in range(len(timeScale)):
        t = Text(f, timeScale[ii])
        legendStartPos += timeScaleOffset[ii]
        t.setPosition(legendStartPos, 388)
        (r, g, b, a) = rgbaConvert(212, 212, 212, 255)
        t.setColor(r, g, b, a)
        page.addItem(t)

    return


def ldlWatchSlide(p, grList, duration):
    for gr in grList:
        es = EffectSequencer(gr)
        es.addEffect(NullEffect(None), 5)
        es.addEffect(Slider(None, 6, 0), 5)
        es.addEffect(NullEffect(None), duration - 10)
        p.addItem(es)

    return

def slide(p, gr, time, dur, dest):
    
    sx, sy = gr.position()
    es = EffectSequencer(gr)
    es.addEffect(NullEffect(None), int(time))
    es.addEffect(Slider(None, (dest[0]-sx)/dur, (dest[1]-sy)/dur), int(dur))
    p.addItem(gr)

def clipObj(p, gr, left=0, right=720, top=720, bottom=0):
    c = Clipper(gr)
    c.clip(Clipper.CP_LEFT, left, 0)
    c.clip(Clipper.CP_RIGHT, right, 0)
    c.clip(Clipper.CP_TOP, top, 0)
    c.clip(Clipper.CP_BOTTOM, bottom, 0)

def createBox(p, pos, size, color):
    gr = Box()
    gr.setSize(*size)
    gr.setPosition(*pos)
    r,g,b,a = color
    gr.setColor(r,g,b,a)
    return gr

def createText(p, text, font, color, pos):
    t = Text(font, text)
    r,g,b,a = color
    t.setColor(r,g,b,a)
    t.setPosition(*pos)
    return t