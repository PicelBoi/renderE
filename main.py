import rendereglobals as rg
import loadtools
import math
from PIL import Image
from io import BytesIO
from twc.embedded.renderd.RenderScript import *
import twc.embedded.renderd.RenderControl as RenderControl
import twc.embedded.renderd.renderUtil as renderUtil
import domestic.renderTools as renderTools
import twc
import twccommon.embedded
import socket
import os
import sys
import threading as th
import time
import random

import builtins
builtins.__dict__["renderElog"] = print #for testing purposes only

import domesticpy.plugin.playman.playCmd.local as pmlc
import domesticpy.plugin.playman.playCmd.pm as pm
import domesticpy.plugin.playman.playCmd.ldl as pmldl
import domestic.wxdata
import json
import traceback as tb
from datetime import datetime
import patches
import twc.dsmarshal as dsm
import pickle

import tscard

DEBUG = False

vidtex = None

sdi = False
if len(sys.argv) > 1:
    sdi = True
    tscard.SDI_URL = sys.argv[1]
    print(f"Set SDI URL to {sys.argv[1]}")

fov = 25
screensize = (720, 480)
zzz = 1
rl = rg.rl

#rl.set_config_flags(rl.ConfigFlags.FLAG_WINDOW_UNDECORATED | rl.ConfigFlags.FLAG_WINDOW_TRANSPARENT)
rl.set_config_flags(rl.ConfigFlags.FLAG_WINDOW_UNDECORATED)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("localhost", 7245))

# im = rl.load_image(os.path.join(os.environ["RENDEREROOT"], "icon.png"))
# im2 = rl.load_image(os.path.join(os.environ["RENDEREROOT"], "icon.png"))
# rl.image_resize(im2, 128, 128)
# im3 = rl.load_image(os.path.join(os.environ["RENDEREROOT"], "icon.png"))
# rl.image_resize(im3, 64, 64)
# im4 = rl.load_image(os.path.join(os.environ["RENDEREROOT"], "icon.png"))
# rl.image_resize(im4, 32, 32)
# rl.set_window_icons((im, im2, im3, im4), 4)

def loadtif(filename): 
    im = Image.open(filename)
    arr = BytesIO()
    im.save(arr, format="PNG")
    arr = arr.getvalue()
    im2 = rl.load_image_from_memory('.png', arr, len(arr))
    return (rl.load_texture_from_image(im2), im2.width, im2.height)

names = ["RenderE" for _ in range(47)] + ["ReReRenderD", "RemixD", "RenderD"]
windbg = ""

splashes = [
    "Functioning not guaranteed",
    "From Wikipedia, the free encyclopedia",
    "I'm Southbridge Cable Network, and I approve this message",
    "Brought to you by SpecifiCable Communications",
    "Trusted. Reliable. Accurate.",
    "It could be better with your help!",
    "The original IntelliStrons I",
    "No more ancient hardware now.",
    "I don't want your SVG remakes.",
    "100% Original Recipe!",
    "Thunderstorm card not guaranteed.",
    "The programmer has a nap. Holdout! Programmer!",
    "The letter R has the correct vertical size",
    "specificable.lewolfyt.cc",
    "Weather. News. Freedom. SpecifiCable.",
    "I hope your computer is decent!",
    "We call it the CPU fryer 9000.",
    "bash: fortune: command not found",
    "We're gonna take it into overtime",
    "3D was definitely drunk while working on the i1",
    "Remember that greed is one of the seven deadly sins.",
    "Let's put this show together.",
    "The IntelliStar for the common man, woman, or otherwise stated.",
    "We do TWC preservation, the right way.™",
    "Weather coverage you can count on.",
    "Prepare your computer! It's gonna get ugly.",
    "Now you can be the MSO everyone needs.",
    "There is no such thing as the RenderD window.",
    "Run that funky forecast, white boy!",
    "Azmo, brick, biatch, and now.. this. Hello!",
    "Holla Holla get $",
    "R.I.P. NRi1. You will be missed.",
    "The only simulator to have allegedly won three purple hearts!",
    "If the graphics are broken, blow into it and try again."
]

fortune = random.choice(splashes)
rl.init_window(screensize[0], screensize[1], f"{random.choice(names)} - {fortune}")

camera = rl.Camera3D(
    rl.Vector3(0, 0, 0),
    rl.Vector3(0, 0, -10),
    rl.Vector3(0, 1, 0),
    fov,
    rl.CameraProjection.CAMERA_PERSPECTIVE
)

planem = rl.gen_mesh_plane(1, 1, 1, 1)

rl.set_target_fps(30)

def frustum_size_at_z(z, fov_y_deg, aspect_ratio):
    fov_y = math.radians(fov_y_deg)
    height = z * math.tan(fov_y / 2)
    width = height * aspect_ratio
    return width, height

zzz = rg.zzz

xxx, yyy = frustum_size_at_z(zzz, fov, screensize[0]/screensize[1])
print(xxx, yyy)
# xxx = 2.6
# yyy = 1.72

plane = rl.load_model_from_mesh(planem)

defaulttex = plane.materials[0].maps.texture

rl.rl_disable_backface_culling()

ee = 0

def jsontodata(jsond):
    dt = twccommon.Data()
    dt.__dict__ = json.loads(jsond)
    return dt

runrs = patches.runrs
runrsc = patches.runrsc

def sockethandle():
    sock.listen()
    while True:
        conn, addr = sock.accept()
        while True:
            print("waiting time!")
            breaking = False
            expecting = int.from_bytes(conn.recv(4), "big")
            data = bytearray()
            while True:
                cdata = conn.recv(1024) #i'll have to figure out larger data chunks not-today
                if not cdata:
                    breaking = True
                    break
                expecting -= len(cdata)
                data.extend(cdata)
                if expecting == 0:
                    break
            if breaking:
                break
            
            if data.split(b" ")[0].decode() == "rset":
                args = data.split(b" ")
                buf = BytesIO(b" ".join(args[4:]))
                val = pickle.Unpickler(buf).load()
                res = dsm.set(args[1].decode(), val, float(args[2]), int(args[3]), session=1)
                conn.send(res.encode())
                conn.shutdown(socket.SHUT_WR)
                print(f"remotely set {args[1].decode()} to {val}")
                continue
            elif data.split(b" ")[0].decode() == "rget":
                args = data.split(b" ")
                buf = BytesIO()
                dat = dsm.get(args[1].decode(), session=1)
                pickle.Pickler(buf).dump(dat)
                conn.send(buf.getvalue())
                conn.shutdown(socket.SHUT_WR)
                print("remotely got")
                continue
            elif data.split(b" ")[0].decode() == "rcommit":
                dsm.ds.commit(1)
                continue
            
            data = data.decode().strip()
            args = data.split(" ")
            if args[0] == "runrs":
                runrs(args[1])
            elif args[0] == "runrsc":
                try:
                    runrsc(args[1])
                except:
                    tb.print_exc()
            elif args[0] == "jsonload":
                prodType = args[1]
                dat = jsontodata(" ".join(args[2:]))
                try:
                    domestic.wxdata.loadData(prodType, dat)
                except:
                    tb.print_exc()
            elif args[0] == "jsonrun":
                prodType = args[1]
                dat = jsontodata(" ".join(args[2:]))
                try:
                    domestic.wxdata.runData(prodType, dat)
                except:
                    tb.print_exc()
            elif args[0] == "togglenat":
                print("togglenat")
                dat = json.loads(" ".join(args[1:]))
                try:
                    domestic.wxdata.toggleNationalLDL(*dat)
                except:
                    tb.print_exc()
            elif args[0] == "activatel":
                RenderControl.activateLayer(args[1], 0)
            elif args[0] == "deactivatel":
                RenderControl.deactivateLayer(args[1], 0)
            elif args[0] == "createtest":
                RenderControl.destroyNamedLayer("Foreground", 0)
                producttest()
            else:
                print(args)
        conn.close()

tth = th.Thread(target=sockethandle, daemon=True)
tth.start()

prodloader = pm._ProdLoader()

def fsplash():
    l = Layer()
    p = Page()
    l.addPage(p)

    gr = Box()
    gr.setSize(720,480)
    r,g,b,a = renderUtil.rgbaConvert(235,235,235)
    gr.setColor(r,g,b,a)
    p.addItem(gr)

    quad2 = TIFF_Image("/rsrc/images/renderELogo")
    quad2.setSize(360, 240)
    quad2.setPosition(180, 120)

    Rotate(quad2, .9, xr=1)
    Rotate(quad2, .8, yr=1)
    Rotate(quad2, .7, zr=1)

    gr = Box()
    gr.setSize(720, 110)
    r, g, b, a = renderUtil.rgbaConvert(20, 20, 20)
    gr.setColor(r, g, b, a)
    p.addItem(gr)

    # gr = TIFF_Image()
    # gr.setSize(720, 110)
    # r, g, b, a = renderUtil.rgbaConvert(20, 20, 20)
    # gr.setColor(r, g, b, a)
    # p.addItem(gr)

    p.addItem(quad2)

    f = TTFont("/rsrc/fonts/Frutiger_Bold", 16, shadow = 0)
    r,g,b,a = renderUtil.rgbaConvert(255, 212,  14)
    gr = Text(f, 'headend Id: 322737')
    gr.setPosition(70,92)
    gr.setColor(r,g,b,a)
    p.addItem(gr)
    gr = Text(f, 'serial number: N/A')
    gr.setPosition(70,76)
    gr.setColor(r,g,b,a)
    p.addItem(gr)
    gr = Text(f, 'location name: Minneapolis')
    gr.setPosition(70,60)
    gr.setColor(r,g,b,a)
    p.addItem(gr)
    gr = Text(f, 'affiliate name: XFINITY TV')
    gr.setPosition(70,44)
    gr.setColor(r,g,b,a)
    p.addItem(gr)
    
    cr = CompositeRenderable()

    filename = "/rsrc/logos/twcLogo"
    gr = TIFF_Image(filename)
    gr.setPosition(600, 62)
    #p.addItem(gr)
    cr.addItem(gr)
    filename = "/rsrc/logos/wxScanLogo"
    gr = TIFF_Image(filename)
    gr.setPosition(490, 44)
    #p.addItem(gr)
    cr.addItem(gr)
    
    p.addItem(cr)

    #name, layer, time, frameOffset, depth, repeat, x, y, w, h, sx, sy, tx, ty, activated
    rg.layers.append(["Foreground", l, 0, 0, 10, 0, 0, 0, 720, 480, 1, 1, 0, 0, False])

def ebucolorbars():
    RenderControl.createNamedLayer("Video", 25, 0, 0, 0, 0)
    l = Layer()
    p = Page()
    l.addPage(p)
    im = JPEG_Image(rg.newjoin(os.environ["RENDEREROOT"], "ebu"))
    im.setSize(720, 480)
    im.setPosition(0, 0)
    p.addItem(im)
    RenderControl.appendLayer("Video", l)
    RenderControl.activateLayer("Video")

#ebucolorbars()

def producttest():
    l = Layer()
    p = Page()
    l.addPage(p)
    pduration = 150
    
    bkg1 = twc.findRsrc("/backgrounds/%s" % ("domestic"), "tif", 1)
    print(bkg1)
    background = TIFF_Image(bkg1)
    background.setTransitionable(0)
    background.setSize(720, 480)
    p.addItem(background)
    
    print("loadedbg")


    def center(areaStart, areaWidth, elemWidth):
        return areaStart + areaWidth/2 - elemWidth/2

    ru = renderUtil   # abbreviation
    
    title = ("test", "product")
    dur = pduration

    titleX = 52
    titleY = 479 - 74
    
    def resolveOverrides(name, defaultVal):
        return defaultVal

    text1Color       = resolveOverrides('text1Color', (212, 212, 212, 255))
    text2Color       = resolveOverrides('text2Color', (20, 20, 20, 255))
    text1ShadowColor = resolveOverrides('text1ShadowColor', (20, 20, 20, 255))
    text2ShadowColor = resolveOverrides('text2ShadowColor', (212, 212, 212, 255))
    text1BkgColor    = resolveOverrides('text1BkgColor', (0, 0, 0, 0))
    text2BkgColor    = resolveOverrides('text2BkgColor', (212, 212, 212, 255))
    fadeIn           = resolveOverrides('titleFadeInDuration', 5)
    fadeOut          = resolveOverrides('titleFadeOutDuration', 5)


    #Create the title bar elements
    crBev, crTxt = renderTools.createTitleBar(
        title[0],              title[1],
        text1BkgColor,    text2BkgColor,
        text1Color,       text2Color,
        text1ShadowColor, text2ShadowColor)
    print("title")
    #First add the title bevel
    crBev.setPosition(titleX, titleY)
    p.addItem(crBev)

    #Now add the title text (and background gradient)
    crTxt.setPosition(titleX, titleY)
    p.addItem(crTxt)

    if ((fadeIn > 0) or ( fadeOut > 0)):
        renderUtil.fadeInOut(p, crTxt, dur, fadeIn, fadeOut)
    print("fio")
    ww = 215
    hh = 282
    xpos =  52
    ypos = 370
    baseline = 89

    locBox   = CompositeRenderable()
    iconBox  = CompositeRenderable()
    tabBox   = CompositeRenderable()
    dataBox  = CompositeRenderable()
        
    # location name with bevel box    
    wwbb = 616
    locBox.addItem(ru.getBevelBox(wwbb, 30))
        
    r,g,b,a = ru.rgbaConvert(212,212,50)
    ff = TTFont('/rsrc/fonts/Interstate-Bold', 24, t=50)
    tt = Text(ff, "WINNERS DON'T USE DRUGS")
    tt.setPosition(11, 8)
    tt.setColor(r,g,b,a)
    locBox.addItem(tt)
        
    # position the compsite renderable
    locBox.setPosition(xpos, ypos)

    # left and right bevel boxes with icon and temp data
    bb = ru.getBevelBox(ww,hh)
    bb.setPosition(0, 0)
    iconBox.addItem(bb)

    bb = ru.getBevelBox(wwbb-ww, hh)
    bb.setPosition(0, 0)
    tabBox.addItem(bb)
    
    iconBox.setPosition(52, baseline)
    tabBox.setPosition(267, baseline)
    dataBox.setPosition(453, baseline)
        
    # transitions
    # add the locBox, iconBox, and tabBox into one Composite Renderable to slide off screen
    slideCR = CompositeRenderable()
    slideCR.setPosition(-720, 0)
    slideCR.addItem(locBox)
    slideCR.addItem(iconBox)
    slideCR.addItem(tabBox)
    p.addItem(slideCR)
    p.addItem(dataBox)    

    # begin loc box
    es = EffectSequencer(slideCR)
    es.addEffect(Slider(None, 72, 0), 10)
    es.addEffect(NullEffect(None), pduration - 20)
    es.addEffect(Slider(None, -72, 0), 10)
    p.addItem(es)
    
    es = EffectSequencer(slideCR)
    es.addEffect(Rotate(None, -36, zr=1), 10)
    es.addEffect(NullEffect(None), pduration - 20)
    es.addEffect(Rotate(None, 36, zr=1), 10)
    p.addItem(es)

    # begin right side data area
    #TODO: Make Clipper work on text!    
    # add clipper for 'reveal' effect    
    #c = Clipper(None, bottom=100)
    #c.clip(Clipper.CP_BOTTOM, pos=hh, step=-10)
        
    es = EffectSequencer(dataBox)
    #es.addEffect(NullEffect(None), 5)
    #es.addEffect(c, 60)
    es.addEffect(NullEffect(None), pduration - 10)
    es.addEffect(Slider(None, -72, 0), 10)
    p.addItem(es)
    
    gr = renderUtil.getBevelBox(100, 100, debug=True)
    gr.setPosition(0, 0)
    p.addItem(gr)

    renderTools.dataNotAvailable(page=p, displayDuration=pduration, text="renderE could be better with your help!", noDataBar=True)
    
    ac = []
    
    aFile = 'CC_INTRO%d' % 1
    intro = '/rsrc/audio/vocalLocal/Intros_Curr_Cond/%s.wav' % aFile
    ac.append(AudioClip(intro))
    audioClipTemp = '/rsrc/audio/vocalLocal/Temps_Specific/%d.wav' % (random.randint(1, 135))
    ac.append(AudioClip(audioClipTemp))
    audioClipSky = '/rsrc/audio/vocalLocal/Wx_Phrases_Curr_Cond/%d.wav'% 3000
    ac.append(AudioClip(audioClipSky))
    
    aseq = AudioSequencer()
    for i in range(len(ac)):
        ac[i].setBlendType(AudioRenderable.BLEND_MIX)
        ac[i].setVolLevel(1.0)
        aseq.addItem(ac[i])
    p.addItem(aseq)
    
    testCR = CompositeRenderable()
    testCR.setPosition(100, 100)
    gr = Box()
    gr.setSize(200, 200)
    gr.setPosition(-50, 0)
    gr.setColor(1, 1, 1, 1)
    testCR.addItem(gr)
    p.addItem(testCR)

    RenderControl.createNamedLayer("Foreground", 10)
    RenderControl.setLayer("Foreground", l, 0, 0)

#producttest()
RenderControl.queueCommand(ActivateLayerCmd("Foreground"), time.time()+1)

whiteimg = rl.gen_image_color(1, 1, rl.WHITE)
white = rl.load_texture_from_image(whiteimg)
redimg = rl.gen_image_color(1, 1, rl.RED)
red = rl.load_texture_from_image(redimg)
once = True

def mod2(a, b=720):
    if a == 0:
        return a
    return ((abs(a) % b) * (a/abs(a)))

def updateseq(seq : EffectSequencer):
    if len(seq.effects) == 0:
        return
    seq.timer += 1
    al = []
    al.append(seq.effects[0][1])
    if len(seq.effects) > 0:
        for i in seq.effects[1:]:
            al.append(al[-1]+i[1])
    
    if seq.timer >= seq.total and seq.repeat:
        seq.timer = 0
        for ef in seq.effects:
            if hasattr(ef[0], "frame"):
                ef[0].frame = 0
            if hasattr(ef[0], "frozen"):
                ef[0].frozen = False
            if hasattr(ef[0], "fired"):
                ef[0].fired = False
        seq.activeeffects = []
    
    ea = 0
    for i in range(len(seq.effects)):
        ea += 1
        if seq.timer < al[i]:
            break
    if len(seq.activeeffects) < ea:
        seq.activeeffects.append(seq.effects[ea-1][0])
    for i in range(ea-1):
        seq.activeeffects[i].frozen = True
    if seq.timer >= seq.total:
        if not seq.repeat:
            for ef in seq.effects:
                ef[0].frozen = True

activedrawlayer = None

drawlevel = 0

def calceffects(quad):
    qqx, qqy = quad._position
    effects = quad.effects
    qqx = round(qqx)
    qqy = round(qqy)
    qx, qy = qqx*1, qqy*1
    xw = quad._size[0]/720*(xxx*2)
    yw = quad._size[1]/480*(yyy*2)
    
    mat = rl.matrix_rotate_xyz((math.radians(90), 0, math.radians(0)))
    mat = rl.matrix_multiply(mat, rl.matrix_scale(xw, yw, 1))
    fader = 1
    visible = not not quad.visible
    def applyeffect(effect : GraphicEffect):
        nonlocal mat, xxw, yyw, fader, qx, qy, visible
        if type(effect) == Rotate:
            if effect.xr:
                mat = rl.matrix_multiply(mat, rl.matrix_rotate_x(math.radians(effect.angle*effect.frame)))
            if effect.yr:
                mat = rl.matrix_multiply(mat, rl.matrix_rotate_y(math.radians(effect.angle*effect.frame)))
            if effect.zr:
                mat = rl.matrix_multiply(mat, rl.matrix_rotate_z(math.radians(effect.angle*effect.frame)))
        elif type(effect) == Slider:
            #xxw -= (effect.dx*effect.frame/720*(xxx*2))
            #yyw -= (effect.dy*effect.frame/480*(yyy*2))
            qx += effect.dx*effect.frame
            qy += effect.dy*effect.frame
        elif type(effect) == Fader:
            if effect.frames == 1:
                fader = effect.endAlpha
            else:
                dist = (effect.frame/effect.frames)
                dist = min(dist, 1)
                fader = effect.startAlpha*(1-dist) + effect.endAlpha*dist
        elif type(effect) == SetPosition:
            #xxw -= (effect.x)/720*(xxx*2)
            #yyw -= (effect.y)/480*(yyy*2)
            qx += mod2(effect.x)
            qy += effect.y
        elif type(effect) == SetSize:
            quad._size = (effect.w, effect.h)
        elif type(effect) == SetText:
            if isinstance(quad, Text):
                quad.s = effect.s
        elif type(effect) == SetVisibility:
            visible = effect.visible
            if effect.fader is not None:
                fader = effect.fader
        if hasattr(effect, "frame"):
            if not effect.frozen:
                effect.frame += 1
        
    def loopover(eflist):
        for effect in eflist:
            if type(effect) == EffectSequencer:
                updateseq(effect)
                loopover(effect.activeeffects)
            else:
                applyeffect(effect)
    loopover(effects)
    # xxw = (-qx-quad._size[0]/2)/720*(xxx*2)
    # yyw = (-qy-quad._size[1]/2)/480*(yyy*2)
    xxw = -qx/720*(xxx*2)
    yyw = -qy/480*(yyy*2)
    mat = rl.matrix_multiply(mat, rl.matrix_translate(-xxx, -yyy, 0))
    if drawlevel == 0:
        xxw -= (activedrawlayer[6]/720*(xxx*2))
        yyw -= (activedrawlayer[7]/480*(yyy*2))
    return xxw, yyw, mat, fader, qx, qy

def draw_quad(quad : TIFF_Image, tex=white, debug=False, se=False, off=(0, 0), premult=False):
    effects = quad.effects
    #rl.set_texture_filter(tex, rl.TextureFilter.TEXTURE_FILTER_POINT)
    plane.materials[0].maps.texture = tex
    if isinstance(quad, Icon):
        rl.set_texture_filter(tex, rl.TextureFilter.TEXTURE_FILTER_TRILINEAR)
    qqx, qqy = quad._position
    if isinstance(quad, Text) or isinstance(quad, Clock):
        qqy += quad.descent
        #print(quad.ascent-quad.descent, quad.cimg.height)
        qqy -= quad.s.count("\n")*quad.fnt.reallineheight
        if quad.fnt.shadow:
            #qqx -= quad.fnt.sx
            qqy -= abs(quad.fnt.sy*2)
    qqx = round(qqx)+off[0]
    qqy = round(qqy)+off[1]
    qx, qy = qqx*1, qqy*1
    xw = quad._size[0]/720*(xxx*2)
    yw = quad._size[1]/480*(yyy*2)
    
    mat = rl.matrix_rotate_xyz((math.radians(90), 0, math.radians(0)))
    mat = rl.matrix_multiply(mat, rl.matrix_scale(xw, yw, 1))
    fader = 1
    visible = not not quad.visible
    def applyeffect(effect : GraphicEffect):
        nonlocal mat, xxw, yyw, fader, qx, qy, visible
        if type(effect) == Rotate:
            if effect.xr:
                mat = rl.matrix_multiply(mat, rl.matrix_rotate_x(math.radians(effect.angle*effect.frame)))
            if effect.yr:
                mat = rl.matrix_multiply(mat, rl.matrix_rotate_y(math.radians(effect.angle*effect.frame)))
            if effect.zr:
                mat = rl.matrix_multiply(mat, rl.matrix_rotate_z(math.radians(effect.angle*effect.frame)))
        elif type(effect) == Slider:
            if not se:
                # xxw -= (effect.dx*effect.frame/720*(xxx*2))
                # yyw -= (effect.dy*effect.frame/480*(yyy*2))
                qx += effect.dx*effect.frame
                qy += effect.dy*effect.frame
        elif type(effect) == Fader:
            dist = (effect.frame/effect.frames)
            if effect.frames == 1:
                fader = effect.endAlpha
            else:
                if dist >= 1:
                    fader = effect.endAlpha
                else:
                    dist = min(dist, 1)
                    fader = effect.startAlpha*(1-dist) + effect.endAlpha*dist
        elif type(effect) == SetPosition:
            if not se:
                #xxw = (-quad._size[0]/2-effect.x)/720*(xxx*2)
                # xxw -= (effect.x)/720*(xxx*2)
                # yyw -= (effect.y)/480*(yyy*2)
                qx += mod2(effect.x)
                qy += effect.y
        elif type(effect) == SetSize:
            if not se:
                quad._size = (effect.w, effect.h)
        elif type(effect) == SetText:
            if not se:
                if isinstance(quad, Text):
                    quad.s = effect.s
        elif type(effect) == SetVisibility:
            #if effect.frozen or effect.frame > 0:
            visible = effect.visible
            if effect.fader is not None:
                fader = effect.fader
        if hasattr(effect, "frame"):
            if not effect.frozen and not se:
                effect.frame += 1
        
    def loopover(eflist):
        for effect in eflist:
            if type(effect) == EffectSequencer:
                if not se:
                    updateseq(effect)
                loopover(effect.activeeffects)
            else:
                applyeffect(effect)
    loopover(effects)
    mat = rl.matrix_multiply(mat, rl.matrix_translate(-xxx, -yyy, 0))
    if drawlevel == 0:
        xxw = (-qx-quad._size[0]/2-activedrawlayer[6])/720*(xxx*2)
        yyw = (-qy-quad._size[1]/2-activedrawlayer[7])/480*(yyy*2)
    else:
        xxw = (-qx-quad._size[0]/2)/720*(xxx*2)
        yyw = (-qy-quad._size[1]/2)/480*(yyy*2)
    plane.transform = mat
    c1, c2, c3, c4 = quad._color
    correct = ((c1 > 1) or (c2 > 1) or (c3 > 1) or (c4 > 1))
    if correct:
        c1 /= 255
        c2 /= 255
        c3 /= 255
        c4 /= 255
    pfader = (1 if not premult else fader)
    try:
        col = rl.Color(min(round(quad._color[0]*255*pfader), 255), min(round(quad._color[1]*255*pfader), 255), min(round(quad._color[2]*255*pfader), 255), min(round(quad._color[3]*fader*255), 255))
    except Exception as e:
        print(c1, c2, c3, c4)
        raise e
    if isinstance(quad, Text):
        col = rl.Color(int(255*pfader), int(255*pfader), int(255*pfader), int(255*fader))
    rl.rl_disable_depth_test()
    rl.rl_disable_depth_mask()
    if visible:
        rl.draw_model_ex(plane, rl.Vector3(-xxw, -yyw, -zzz), rl.Vector3(0, 0, 0), 0, rl.Vector3(1, 1, 1), col)

class DummyQuad():
    def __init__(self, x, y, w, h, effects=[]):
        self._position = (x, y)
        self._size = (w, h)
        self.effects = effects
        self._color = (1, 1, 1, 1)
        self.visible = True
    def size(self):
        return self._size
    def position(self):
        return self._position

def crop_text(surf: rg.pg.Surface):
    final_left = 0
    found_left = False
    for x in range(surf.get_width()):
        for y in range(surf.get_height()):
            c = surf.get_at((x, y))
            if c.a != 0:
                found_left = True
                break
        if found_left:
            break
        final_left += 1
    return surf.subsurface(rg.pg.Rect(final_left, 0, surf.get_width()-final_left, surf.get_height()))

def draw_poly(quad : TIFF_Image, tex=white):
    global drawlevel
    effects = quad.effects
    visible = not not quad.visible
    plane.materials[0].maps.texture = tex
    qqx, qqy = quad._position
    qx, qy = qqx*1, qqy*1
    xw = (xxx*2)/720
    yw = (yyy*2)/480
    
    mat = rl.matrix_scale(xw, yw, 1)
    fader = 1
    pts2 = quad.vertices
    def applyeffect(effect : GraphicEffect):
        nonlocal mat, xxw, yyw, fader, pts2, visible
        if type(effect) == Rotate:
            if effect.xr:
                mat = rl.matrix_multiply(mat, rl.matrix_rotate_x(math.radians(effect.angle*effect.frame)))
            if effect.yr:
                mat = rl.matrix_multiply(mat, rl.matrix_rotate_y(math.radians(effect.angle*effect.frame)))
            if effect.zr:
                mat = rl.matrix_multiply(mat, rl.matrix_rotate_z(math.radians(effect.angle*effect.frame)))
        elif type(effect) == Slider:
            #xxw -= (effect.dx*effect.frame/720*(xxx*2))
            #yyw -= (effect.dy*effect.frame/480*(yyy*2))
            qx += effect.dx*effect.frame
            qy += effect.dy*effect.frame
        elif type(effect) == Fader:
            if effect.frames == 1:
                fader = effect.endAlpha
            else:
                dist = (effect.frame/effect.frames)
                dist = min(dist, 1)
                fader = effect.startAlpha*(1-dist) + effect.endAlpha*dist
        elif type(effect) == Sizer:
            pX = effect.frame*effect.percentX
            if pX == 0:
                pX = 1
            pY = effect.frame*effect.percentY
            pts2 = [(rl.Vector3(p[0].x*pX, p[0].y*pY, p[0].z), p[1], p[2], p[3], p[4]) for p in pts2]
        elif type(effect) == SetVisibility:
            visible = effect.visible
            if effect.fader is not None:
                fader = effect.fader
        if hasattr(effect, "frame"):
            if not effect.frozen:
                effect.frame += 1
    
    def loopover(eflist):
        for effect in eflist:
            if type(effect) == EffectSequencer:
                updateseq(effect)
                loopover(effect.activeeffects)
            else:
                applyeffect(effect)
    loopover(effects)
    
    if not visible:
        return
    
    xxw = (-qx)/720*(xxx*2)
    yyw = (-qy)/480*(yyy*2)
    mat = rl.matrix_multiply(mat, rl.matrix_translate(-xxx, -yyy, 0))
    
    if drawlevel == 0:
        xxw -= (activedrawlayer[6]/720*(xxx*2))
        yyw -= (activedrawlayer[7]/480*(yyy*2))
    mat = rl.matrix_multiply(mat, rl.matrix_translate(-xxw, -yyw, 0))
    
    pts = []
    
    for p in pts2:
        pts.append((rl.vector3_transform(p[0], mat), p[1], p[2], p[3], p[4]))
    #pts = pts2
    
    rl.rl_begin(rl.RL_TRIANGLES)
    for i in range(1, len(pts) - 1):
        # Triangle 1: Vertex 0, i, i+1
        # Setting color per vertex
        rl.rl_color4f(pts[0][1], pts[0][2], pts[0][3], pts[0][4]*fader)
        rl.rl_vertex3f(pts[0][0].x, pts[0][0].y, pts[0][0].z)
        
        rl.rl_color4f(pts[i][1], pts[i][2], pts[i][3], pts[i][4]*fader)
        rl.rl_vertex3f(pts[i][0].x, pts[i][0].y, pts[i][0].z)
        
        rl.rl_color4f(pts[i+1][1], pts[i+1][2], pts[i+1][3], pts[i+1][4]*fader)
        rl.rl_vertex3f(pts[i+1][0].x, pts[i+1][0].y, pts[i+1][0].z)
    rl.rl_end()

audio_chans = []
audio_vols = []
global audio_mixes

last_sec = []

def update_audio(item, activeeffects=None):
    if not item.chan and not isinstance(item, NullAudioClip) and item.file:
        item.chan = item.file.play()
    effects = item.effects
    ae = False
    if activeeffects:
        ae = True
        effects = activeeffects
    mixl = item.mix
    def applyeffect(effect : AudioEffect):
        nonlocal mixl
        if type(effect) == AudioFader:
            dist = (effect.frame/effect.frames)
            dist = min(dist, 1)
            mixl = effect.startMixLevel*(1-dist) + effect.endMixLevel*dist
        if not ae:
            if hasattr(effect, "frame"):
                if not effect.frozen:
                    effect.frame += 1
        
    def loopover(eflist):
        for effect in eflist:
            if type(effect) == AudioEffectSequencer:
                updateseq(effect)
                loopover(effect.activeeffects)
            else:
                applyeffect(effect)
    
    loopover(effects)
    
    if item.chan:
        audio_chans.append(item.chan)
        audio_vols.append(item.level)
        audio_mixes.append(mixl)

def update_audioseq(seq : AudioSequencer, ex={"mix": None}):
    global windbg
    if len(seq.audio) == 0:
        return
    if seq.done:
        return
    seq.timer += 1
    al = []
    al.append(seq.audio[0].duration())
    if len(seq.audio) > 0:
        for i in seq.audio[1:]:
            al.append(al[-1]+i.duration())
    ea = 0
    for i in range(len(seq.audio)):
        if seq.timer < al[i]:
            break
        ea += 1
    if seq.playingidx != ea:
        if type(seq.audio[seq.playingidx]) not in (NullAudioClip, AudioSequencer):
            seq.audio[seq.playingidx].file.stop()
        seq.playingidx = ea
    if seq.playingidx >= len(seq.audio):
        seq.done = True
        return
    
    effects = seq.effects
    
    
    if type(seq.audio[ea]) == AudioSequencer:
        mixl = seq.mix
        def applyeffect(effect : AudioEffect):
            nonlocal mixl
            if type(effect) == AudioFader:
                dist = (effect.frame/effect.frames)
                dist = min(dist, 1)
                mixl = effect.startMixLevel*(1-dist) + effect.endMixLevel*dist
            if hasattr(effect, "frame"):
                if not effect.frozen:
                    effect.frame += 1
            
        def loopover(eflist):
            for effect in eflist:
                if type(effect) == AudioEffectSequencer:
                    updateseq(effect)
                    loopover(effect.activeeffects)
                else:
                    applyeffect(effect)
        
        loopover(effects)
        
        update_audioseq(seq.audio[ea], {"mix": mixl})
    else:
        item = seq.audio[ea]
        mixl = item.mix
        def applyeffect(effect : AudioEffect):
            nonlocal mixl
            if type(effect) == AudioFader:
                dist = (effect.frame/effect.frames)
                dist = min(dist, 1)
                mixl = effect.startMixLevel*(1-dist) + effect.endMixLevel*dist
            if hasattr(effect, "frame"):
                if not effect.frozen:
                    effect.frame += 1
            
        def loopover(eflist):
            for effect in eflist:
                if type(effect) == AudioEffectSequencer:
                    updateseq(effect)
                    loopover(effect.activeeffects)
                else:
                    applyeffect(effect)
        
        loopover(effects)
        if hasattr(item, "file"):
            if not item.chan and item.file:
                item.chan = item.file.play()
            audio_chans.append(item.chan)
            audio_vols.append(item.level)
            audio_mixes.append(ex["mix"] if ex["mix"] is not None else mixl)

mode_3d_tracker = 0

last_sec = []
def unload_tree(item):
    print(f"Unloading item of type {type(item).__name__}")
    if hasattr(item, "unload"):
        item.unload()
        last_sec.append(30)
    if hasattr(item, "items"):
        for i in item.items:
            unload_tree(i)
    if hasattr(item, "elements"):
        for i in item.elements:
            unload_tree(i)

def draw_item(item, extra={"tex": None, "cam": None, "off": (0, 0), "lloop": 0}):
    global mode_3d_tracker
    global once
    global drawlevel
    global windbg
    if type(item) == Layer:
        item.timer += 1
        al = []
        if len(item.pages) == 0:
            return
        al.append(item.pages[0][1])
        if len(item.pages) > 0:
            for i in item.pages[1:]:
                al.append(al[-1]+i[1])
        if extra["lloop"]:
            if item.timer > al[-1]:
                item.timer = 0
        
        ea = 0
        broke = False
        for i in range(len(item.pages)):
            ea += 1
            if item.pages[ea-1][1] == 0:
                break
            if item.timer < al[i]:
                broke = True
                break
        
        if len(item.pages) > 0:
            if not item.pages[0][0].started == True:
                item.pages[0][0].started = True
                for cmd in item.pages[0][0]._onStartCommands:
                    RenderControl.actuallyRunAQueuedCommand(cmd)
        if item.pa != (ea-1):
            item.pages[item.pa][0].ended = True
            for cmd in item.pages[item.pa][0]._onEndCommands:
                RenderControl.actuallyRunAQueuedCommand(cmd)
            if not extra["lloop"]:
                item.pages[item.pa][0].__del__()
                #windbg += "unloaded a page\n"
            #and here
            item.pa = (ea-1)
            item.pages[item.pa][0].started = True
            #...and here
            for cmd in item.pages[item.pa][0]._onStartCommands:
                RenderControl.actuallyRunAQueuedCommand(cmd)
        elif (item.pa == (len(item.pages)-1) and not broke) and not item.pages[item.pa][0].ended:
            item.pages[item.pa][0].ended = True
            for cmd in item.pages[item.pa][0]._onEndCommands:
                RenderControl.actuallyRunAQueuedCommand(cmd)
            if not extra["lloop"]:
                item.pages[item.pa][0].__del__()
        else:
            for cmd in item.pages[item.pa][0]._onFrameCommands:
                if item.timer == cmd[1]:
                    RenderControl.actuallyRunAQueuedCommand(cmd[0])
        draw_item(item.pages[item.pa][0], extra)
    elif type(item) == Page:
        for el in item._elements:
            draw_item(el, extra)
    elif isinstance(item, Icon):
        if item.textures is None:
            item.textures = [None for f in item._ims]
        else:
            item.idx += 1
            item.idx %= item.framect
        if item.textures[item.idx] is None:
            item.textures[item.idx] = rl.load_texture_from_image(item._ims[item.idx])
        draw_quad(item, item.textures[item.idx], off=extra["off"])
    elif type(item) is Box:
        #the og quad
        draw_quad(item, off=extra["off"])
    elif type(item) is Video:
        if vidtex:
            draw_quad(item, vidtex, off=extra["off"])
    elif isinstance(item, DummyQuad):
        draw_quad(item)
    elif isinstance(item, Text):
        if (item._lastcol != item._color) and item.cachedtex is not None:
            if item.cimg:
                rl.unload_image(item.cimg)
            rl.unload_texture(item.cachedtex)
            item.cachedtex = None
            item._lastcol = item._color
            item.cimg = None
        elif (item.lasts != item.s) and item.cachedtex is not None:
            if item.cimg:
                rl.unload_image(item.cimg)
            rl.unload_texture(item.cachedtex)
            item.cachedtex = None
            item.lasts = item.s
            item.cimg = None
            item._textsize = item.fnt.font.size(item.s)
        if item.cachedtex is None:
            item._textsize = item.fnt.font.size(item.s)
            item.create_cimg()
            item.cachedtex = rl.load_texture_from_image(item.cimg)
        item._size = (item.cimg.width, item.cimg.height)
        rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA_PREMULTIPLY)
        if type(item) == Marquee:
            item.pos += item.step
            item.pos %= (item._size[0]+720)
            draw_quad(item, item.cachedtex, off=(extra["off"][0]+720-item.pos, extra["off"][0]), premult=True) #i'll hardcode this until weatherscan forces me to not
        else:
            # draw_quad(item, white, off=extra["off"], premult=True)
            # draw_quad(DummyQuad(item._position[0], item._position[1]-2, item._size[0], 2, []), red, off=extra["off"], premult=True)
            draw_quad(item, item.cachedtex, off=extra["off"], premult=True)
        #rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA_PREMULTIPLY)
        rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA)
    elif isinstance(item, Clock):
        def fix_strftime(tm, format):
            return tm.strftime(format.replace("%l", str(int(tm.strftime("%I")))))
        item.s = fix_strftime(datetime.now(), item.format)
        if (item.lasts != item.s) and item.cachedtex is not None:
            if item.cimg:
                rl.unload_image(item.cimg)
            rl.unload_texture(item.cachedtex)
            item.cachedtex = None
            item.lasts = item.s
            item._textsize = item.fnt.font.size(item.s)
        if item.cachedtex is None:
            item.create_cimg()
            item.cachedtex = rl.load_texture_from_image(item.cimg)
        item._size = (item.cimg.width, item.cimg.height)
        rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA_PREMULTIPLY)
        draw_quad(item, item.cachedtex, off=extra["off"], premult=True)
        rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA)
    elif type(item) in (CompositeRenderable, ScrollingCompositeRenderable, RichText, CompositedImage):
        drawlevel += 1
        #print(drawlevel)
        if type(item) == ScrollingCompositeRenderable:
            if not item.rtex:
                item.rtex = rg.rl.load_render_texture(720, 480)
            if not item.ftex:
                item.ftex = rg.rl.load_render_texture(*item.bbox)
        else:
            if not item.rtex:
                item.rtex = rg.rl.load_render_texture(720, 480)
            if not item.ftex:
                item.ftex = rg.rl.load_render_texture(720, 480)
        rl.end_mode_3d()
        mode_3d_tracker -= 1
        rl.begin_texture_mode(item.rtex)
        rl.clear_background(rl.Color(0, 0, 0, 0))
        rl.rl_set_clip_planes(0.01, 10000)
        
        xx2, yy2, transfo, fader, xx2p, yy2p = calceffects(item)
        
        #rl.draw_rectangle_lines(round(-xx2p), round(-yy2p), 720, 480, rl.RED)
        
        #print(xx2, yy2)
        #xx2, yy2 = 0, 0
        
        if isinstance(item, ScrollingCompositeRenderable):
            item.scroll -= item.step
            camera2 = rl.Camera3D(
                rl.Vector3(xx2, yy2+item.bbox[1]/480*yyy*2, 0),
                rl.Vector3(xx2, yy2+item.bbox[1]/480*yyy*2, -10),
                rl.Vector3(0, 1, 0),
                fov,
                rl.CameraProjection.CAMERA_PERSPECTIVE
            )
        else:
            camera2 = rl.Camera3D(
                rl.Vector3(xx2, yy2, 0),
                rl.Vector3(xx2, yy2, -10),
                rl.Vector3(0, 1, 0),
                fov,
                rl.CameraProjection.CAMERA_PERSPECTIVE
            )
        if isinstance(item, RichText):
            rl.begin_mode_3d(camera)
        else:
            rl.begin_mode_3d(camera2)
        mode_3d_tracker += 1
        rl.rl_disable_depth_test()
        rl.rl_disable_depth_mask()
        
        camoff = (0, 0)
        xx = 0
        
        for iii, ch in enumerate(item.items):
            if isinstance(item, ScrollingCompositeRenderable):
                camoff = (720+xx+item.scroll, 0)
                if isinstance(ch, Text):
                    xx += item.size()[0]
            if isinstance(ch, CompositeRenderable):
                draw_item(ch, extra={"tex": item.rtex, "cam": camera2, "off": camoff})
                rl.begin_texture_mode(item.rtex)
                rl.rl_set_clip_planes(0.01, 10000)
                if isinstance(item, RichText):
                    rl.begin_mode_3d(camera)
                else:
                    rl.begin_mode_3d(camera2)
                mode_3d_tracker += 1
                rl.rl_disable_depth_test()
                rl.rl_disable_depth_mask()
            elif isinstance(ch, Polygon):
                rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA_PREMULTIPLY)
                draw_item(ch, {"off": camoff})
                rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA)
            else:
                draw_item(ch, {"off": camoff})
        
        rl.end_mode_3d()
        mode_3d_tracker -= 1
        rl.end_texture_mode()
        
        rl.begin_texture_mode(item.ftex)
        rl.clear_background(rl.Color(0, 0, 0, 0))
        rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA_PREMULTIPLY)
        rl.draw_texture(item.rtex.texture, 0, 0, rl.WHITE)
        rl.end_texture_mode()
        
        drawlevel -= 1
        
        if not extra["tex"]:
            rl.rl_set_clip_planes(0.01, 10000)
            rl.begin_mode_3d(camera)
            mode_3d_tracker += 1
            rl.rl_disable_depth_test()
            rl.rl_disable_depth_mask()
            rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA)
            #draw_quad_nocal(DummyQuad(0, 0, 720, 480), item.ftex.texture, transfo, fader)
            if type(item) == RichText:
                xxr, yyr = item._position
                draw_quad(DummyQuad(xxr, yyr, 720, 480, effects=item.effects), item.ftex.texture, se=True)
            elif type(item) == ScrollingCompositeRenderable:
                draw_quad(DummyQuad(*item._position, *item.bbox, effects=item.effects), item.ftex.texture, se=True)
            else:
                draw_quad(DummyQuad(0, 0, 720, 480, effects=item.effects), item.ftex.texture, se=True)
        else:
            rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA_PREMULTIPLY)
            rl.begin_texture_mode(extra["tex"])
            rl.rl_set_clip_planes(0.01, 10000)
            rl.begin_mode_3d(extra["cam"])
            mode_3d_tracker += 1
            rl.rl_disable_depth_test()
            rl.rl_disable_depth_mask()
            drawlevel += 1
            #draw_quad_nocal(DummyQuad(0, 0, 720, 480), item.ftex.texture, transfo, fader)
            if type(item) == RichText:
                xxr, yyr = item._position
                draw_quad(DummyQuad(xxr, yyr, 720, 480, effects=item.effects), item.ftex.texture, se=True)
            elif type(item) == ScrollingCompositeRenderable:
                draw_quad(DummyQuad(*item._position, *item.bbox, effects=item.effects), item.ftex.texture, se=True)
            else:
                draw_quad(DummyQuad(0, 0, 720, 480, effects=item.effects), item.ftex.texture, se=True)
            drawlevel -= 1
            rl.end_mode_3d()
            mode_3d_tracker -= 1
            rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA)
        
        if item.debug:
            tex = rl.load_image_from_texture(item.rtex.texture)
            rl.export_image(tex, "image2.png")
    elif isinstance(item, Image):
        if type(item) is not CompositedImage:
            if not item.texture:
                if item.im2 is not None:
                    item.texture = rl.load_texture_from_image(item.im2)
            if item.texture:
                rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA_PREMULTIPLY)
                draw_quad(item, item.texture, off=extra["off"], premult=True)
                rl.rl_set_blend_mode(rl.BlendMode.BLEND_ALPHA)
    elif type(item) is Polygon:
        draw_poly(item)
    elif isinstance(item, AudioSequencer):
        update_audioseq(item)
    elif type(item) in (AudioClip, MP3_AudioClip):
        if not item.single_play:
            item.single_play = True
            item.chan = item.file.play()
        update_audio(item)
    elif isinstance(item, PageCommand):
        item.timer += 1
        if item.timer == item.activeFrame():
            RenderControl.actuallyRunAQueuedCommand(item)
    elif isinstance(item, VectorImage):
        if item.polys:
            if item.im:
                if not item.tx:
                    item.tx = rg.rl.load_texture_from_image(item.im)
                draw_quad(item, item.tx)
    else:
        pass
        #print("drawing unrecognized type: ", type(item))

import playmaninit

vimg = rl.gen_image_checked(720, 480, 40, 40, rl.BLACK, rl.WHITE)
vtex = rl.load_texture_from_image(vimg)

vl = Layer()
p = Page(0)
v = Video()
v.setPosition(0, 0)
v.setSize(720, 480)
p.addItem(v)
vl.addPage(p)

RenderControl.createNamedLayer("Video", 25, 0, 0)
RenderControl.setLayer("Video", vl)
RenderControl.activateLayer("Video")

trans = False

starid = dsm.defaultedGet("starId", "StarID Unavailable")

MUTE = False

if sdi:
    sdih = tscard.Handler(tscard.SDI_URL)

while not rl.window_should_close():
    if sdi:
        if not vidtex and sdih.size != (0, 0):
            timg = rl.gen_image_color(*sdih.size, rl.BLACK)
            vidtex = rl.load_texture_from_image(timg)
        
        if sdih.frame:
            rl.update_texture(vidtex, rl.ffi.new("char []", sdih.frame))
    audio_chans = []
    audio_mixes = []
    audio_vols = []
    remove = []
    for i, cmdlist in enumerate(rg.queuedcommands):
        cmd, tm, fo, estimated = cmdlist
        if time.time() > tm:
            print("runcmd ", cmd)
            if type(cmd) in [SetNamedLayerViewPortCmd, ModifyNamedLayerCmd]:
                print(cmd.__dict__)
            RenderControl.actuallyRunAQueuedCommand(cmd)
            remove.append(cmdlist)
    for i in remove:
        rg.queuedcommands.remove(i)
    sortedLayers = sorted(rg.layers, key=lambda layer: layer[4])
    ee += 1
    rl.begin_drawing()
    rl.clear_background(rl.BLANK)
    rl.rl_set_clip_planes(0.01, 10000)
    rl.begin_mode_3d(camera)
    mode_3d_tracker += 1
    rl.rl_disable_depth_test()
    rl.rl_disable_depth_mask()
    
    audio_depths = []
    audnames = []
    
    
    for l in sortedLayers:
        lastaud = 0
        if l[-1]:
            activedrawlayer = l
            draw_item(l[1])
        for _ in range(len(audio_chans)-lastaud):
            audio_depths.append(l[4])
            audnames.append(l[0])
        lastaud = len(audio_chans)
    
    sorted_audio = sorted(zip(audio_chans, audio_mixes, audio_vols, audio_depths, audnames), key = lambda x: x[3])
    audio_finalvols = []
    video_audio_level = 1
    if sorted_audio:
        audio_chans, audio_mixes, audio_vols, audio_depths, audnames = zip(*sorted_audio)
        
        audio_finalvols = list(audio_vols).copy()
        
        for i, mix in enumerate(audio_mixes):
            video_audio_level *= (1 - mix)
            for j in range(len(audio_finalvols)):
                if j <= i:
                    if j == i:
                        audio_finalvols[j] *= mix
                    else:
                        audio_finalvols[j] *= (1 - mix)
        
        i = 0
        for chan, vol in zip(audio_chans, audio_finalvols):
            #chan.set_volume(vol if not MUTE else 0)
            snd = chan.get_sound()
            if snd:
                snd.set_volume(vol if not MUTE else 0)
            i += 1
        print(video_audio_level)
        
    if sdi:
        sdih.set_volume(video_audio_level)
        #print("set volume", vol)
    
    rl.end_mode_3d()
    mode_3d_tracker -= 1
    if DEBUG:
        layer_list = "\n".join(["Layer Order:"] + [f"{l[0]} (depth {l[4]})" for l in sortedLayers])
        lines = windbg.split("\n")
        if len(lines) > 12:
            lines = lines[-12:]
        rl.draw_fps(10, 10)
        rl.draw_text(f"StarID: {starid}", 10, 40, 20, rl.WHITE)
        rl.draw_text(f"Audio Playing: {len(audio_chans)}", 10, 70, 20, rl.WHITE)
        vlist = '\n'.join([str(round(vol*100))+'%\n' for vol in audio_finalvols])
        rl.draw_text(layer_list, 10, 100, 20, rl.WHITE)
    for i in range(len(last_sec)):
        last_sec[i] -= 1
    
    while True:
        try:
            last_sec.remove(0)
        except:
            break
    rl.end_drawing()
    for i in rg.unloadqueue:
        unload_tree(i)
    rg.unloadqueue = []
    
    if rl.is_key_pressed(rl.KeyboardKey.KEY_D):
        DEBUG = not DEBUG
    
    if rl.is_key_pressed(rl.KeyboardKey.KEY_M):
        MUTE = not MUTE