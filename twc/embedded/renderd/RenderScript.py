# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: RenderScript.py
# Compiled at: 2007-01-12 11:17:28

import rendereglobals as rg
from . import _renderd
import os

class ObjectWrapper:

    def __init__(self):
        raise RuntimeError('Instantiated abstract class: ' + self.__name__)

    def __del__(self):
        pass


class Layer(ObjectWrapper):

    def __init__(self):
        self.pages = []
        self.timer = 0
        self.totals = []
        self.pa = 0
        return

    def addPage(self, page):
        self.pages.append((page, page.duration()))
        if len(self.totals) == 0:
            self.totals.append(page.duration())
        else:
            self.totals.append(page.duration()+self.totals[-1])


class Page(ObjectWrapper):

    def __init__(self, duration=0):
        """duration == 0 means page plays forever"""
        self.timer = 0
        self._duration = duration
        self.started = False
        self.ended = False
        self._elements = []
        self._onStartCommands = []
        self._onFrameCommands = []
        self._onEndCommands = []

    def addItem(self, item):
        if isinstance(item, PageCommand):
            frame = item.activeFrame()
            if frame == 0:
                return self.addOnStartCommand(item)
            elif frame == self._duration - 1:
                return self.addOnEndCommand(item)
            else:
                return self.addOnFrameCommand(item, frame)
        else:
            #res = _renderd.Page_addItem(self, item)
            res = 1
            self._elements.append(item)
            return res

    def addOnStartCommand(self, cmd):
        self._onStartCommands.append(cmd)
        return

    def addOnFrameCommand(self, cmd, activeFrame, forceAtEnd=0):
        #res = _renderd.Page_addOnFrameCommand(self, activeFrame, cmd, forceAtEnd)
        self._onFrameCommands.append([cmd, activeFrame, forceAtEnd])
        return 

    def addOnEndCommand(self, cmd):
        #res = _renderd.Page_addOnEndCommand(self, cmd)
        self._onEndCommands.append(cmd)
        return 

    def elements(self):
        return self._elements

    def onStartCommands(self):
        return self._onStartCommands

    def onFrameCommands(self):
        return self._onFrameCommands

    def onEndCommands(self):
        return self._onEndCommands

    def duration(self):
        return self._duration

    def __del__(self):
        for i in self._elements:
            rg.unloadqueue.append(i)

class Font(ObjectWrapper):

    def __init__(self, pointsize):
        self.pointsize = pointsize

    def pointSize(self):
        return self.pointsize

    def tracking(self):
        return 0

    def leading(self):
        return self.font.get_linesize()

    def stringSize(self, str):
        bn = self.font.size(str)
        return bn

    def stringWidth(self, str):
        (w, h) = self.stringSize(str)
        return w

    def stringHeight(self, str):
        (w, h) = self.stringSize(str)
        return h


class TTFont(Font):

    def __init__(self, name, pointSize, shadow=1, sr=0.08, sg=0.08, sb=0.08, sa=1.0, sx=1, sy=2, t=0, l=None, evict=0):
        self.shadow = shadow
        self.scol = (sr, sg, sb, sa)
        self.sx = sx*1
        self.sy = sy*1
        Font.__init__(self, pointSize)
        if l == None:
            l = pointSize
        _renderd.createTTFont(self, name, pointSize, shadow, sr, sg, sb, sa, sx, sy, t / 2, l, evict)


class TTOutlineFont(Font):

    def __init__(self, name, pointSize, thickness=1, t=0, l=None, evict=0):
        if l == None:
            l = pointSize
        Font.__init__(self, pointSize)
        _renderd.createTTOutlineFont(self, name, pointSize, thickness, t / 2, l, evict)


class Renderable(ObjectWrapper):

    def setAnimationState(self, animate):
        return #_renderd.Renderable_setAnimationState(self, animate)

    def animationState(self):
        return #_renderd.Renderable_getAnimationState(self)

    def setVisibility(self, visible):
        self.visible = visible
        return

    def visibility(self):
        return self.visible


class PageCommand(Renderable):

    def __init__(self, activeFrame=0):
        self.timer = -1
        self._activeFrame = activeFrame

    def activeFrame(self):
        return self._activeFrame


class CreateNamedLayer(PageCommand):

    def __init__(self, activeFrame, lname, depth, repeat=0, autoDestroy=1):
        PageCommand.__init__(self, activeFrame)
        self.lname = lname
        self.depth = depth
        self.repeat = repeat
        self.autoDestroy = autoDestroy


class DestroyNamedLayer(PageCommand):

    def __init__(self, activeFrame, lname):
        PageCommand.__init__(self, activeFrame)
        self.lname = lname


class SetLayer(PageCommand):

    def __init__(self, activeFrame, lname, layer):
        PageCommand.__init__(self, activeFrame)
        self.lname = lname
        self.layer = layer


class AppendLayer(PageCommand):

    def __init__(self, activeFrame, lname, layer):
        PageCommand.__init__(self, activeFrame)
        self.lname = lname
        self.layer = layer


class RemoveLayer(PageCommand):

    def __init__(self, activeFrame, lname):
        PageCommand.__init__(self, activeFrame)
        self.lname = lname


class ActivateLayer(PageCommand):

    def __init__(self, activeFrame, lname):
        PageCommand.__init__(self, activeFrame)
        self.lname = lname


class DeactivateLayer(PageCommand):

    def __init__(self, activeFrame, lname):
        PageCommand.__init__(self, activeFrame)
        self.lname = lname


class SelectInputSource(PageCommand):

    def __init__(self, activeFrame, src):
        PageCommand.__init__(self, activeFrame)


class LoadPresentation(PageCommand):

    def __init__(self, activeFrame, fileName):
        PageCommand.__init__(self, activeFrame)
        self.fileName = fileName


class ActivateGpiPin(PageCommand):

    def __init__(self, activeFrame, pin):
        PageCommand.__init__(self, activeFrame)


class DeactivateGpiPin(PageCommand):

    def __init__(self, activeFrame, pin):
        PageCommand.__init__(self, activeFrame)


class RenderCommand(ObjectWrapper):
    pass


class CreateNamedLayerCmd(RenderCommand):

    def __init__(self, lname, depth, repeat=0, autoDestroy=1):
        self.lname = lname
        self.depth = depth
        self.repeat = repeat
        self.autoDestroy = autoDestroy


class DestroyNamedLayerCmd(RenderCommand):

    def __init__(self, lname):
        self.lname = lname


class SetNamedLayerViewPortCmd(RenderCommand):

    def __init__(self, lname, x, y, w, h, sx=1, sy=1, tx=0, ty=0):
        self.lname = lname
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.sx = sx
        self.sy = sy
        self.tx = tx
        self.ty = ty


class SetLayerCmd(RenderCommand):

    def __init__(self, lname, layer):
        self.lname = lname
        self.layer = layer


class AppendLayerCmd(RenderCommand):

    def __init__(self, lname, layer):
        self.lname = lname
        self.layer = layer


class RemoveLayerCmd(RenderCommand):

    def __init__(self, lname):
        self.lname = lname


class ActivateLayerCmd(RenderCommand):

    def __init__(self, lname):
        self.lname = lname


class DeactivateLayerCmd(RenderCommand):

    def __init__(self, lname):
        self.lname = lname
        


class SelectInputSourceCmd(RenderCommand):

    def __init__(self, src, activeFrame=0):
        _renderd.createSelectInputSource(self, src, activeFrame)
        


class LoadPresentationCmd(RenderCommand):

    def __init__(self, fileName):
        self.fileName = fileName
        


class ActivateGpiPinCmd(RenderCommand):

    def __init__(self, pin):
        _renderd.createActivateGpiPin(self, pin)
        


class DeactivateGpiPinCmd(RenderCommand):

    def __init__(self, pin):
        _renderd.createDeactivateGpiPin(self, pin)
        


class ModifyNamedLayerCmd(RenderCommand):

    def __init__(self, name, newName, depth, repeat, autoDestroy):
        self.name = name
        self.newName = newName
        self.depth = depth
        self.repeat = repeat
        self.autoDestroy = autoDestroy
        


class ReplaceLayerCmd(RenderCommand):

    def __init__(self, name, layer):
        self.name = name
        self.layer = layer
        


class SignalEventCmd(RenderCommand):

    def __init__(self, type, params, channel='SystemEventChannel'):
        _renderd.createSignalEvent(self, type, params, channel)
        


class GraphicRenderable(Renderable):

    def __init__(self):
        self._position = (0, 0)
        self._size = (0, 0)
        self.effects = []
        self.sequencer = None
        self.visible = True
        self.setTransitionable(1)
        
        self._color = (1, 1, 1, 1)
    
    def size(self):
        return self._size
        
    def addGraphicEffect(self, effect):
        self.effects.append(effect)
    
    def addEffectSequencer(self, seq, repeat, loopLimit):
        self.effects.append(seq)
    

    def setTransitionable(self, val):
        self._transitionable = val
        

    def transitionable(self):
        return self._transitionable
        return

    def setPosition(self, x, y):
        self._position = (x, y)
        return

    def position(self):
        return self._position
        return

    def setSize(self, w, h):
        self._size = (w, h)
        return

    def size(self):
        return self._size

    def setColor(self, r=0, g=0, b=0, a=1):
        self._color = (r, g, b, a)
        return

    def color(self):
        return self._color
        return


class Box(GraphicRenderable):

    def __init__(self):
        super().__init__()
        return
        


class Clock(GraphicRenderable):
    LEFT = 0
    RIGHT = 1
    CENTER = 2

    def __init__(self, font, format, lcase_ampm=1, justification=LEFT, timezone='', timezoneDisplay=''):
        """Specify the font and format used to display the time.
        format is a string in the format expected by the strftime c-lib func.
        timezone is a string used to set the TZ environment variable for alternate timezones.
        timzoneDisplay is the string value that will replace '<z>' within the format string.
        """
        GraphicRenderable.__init__(self)
        self.font = font
        self.format = format
        self.lcase_ampm = lcase_ampm
        self.justification = justification
        self.timezone = timezone
        self.timezoneDisplay = timezoneDisplay
        self.s = '10:09'
        self.lasts = ''
        self.cachedtex = None
        self.cachedimg = None
        self.cimg = None
        self.fnt = font
        self.ascent = self.fnt.ascent
        self.descent = self.fnt.descent
        
        self.textbase : rg.pg.Surface = self.fnt.font.render(builtins.str(self.s), True, (255, 255, 255))
        self.textbase = rg.pg.transform.smoothscale_by(self.textbase, (1, 0.93))
        
        self._lastcol = tuple(list(self._color))
        self._textsize = self.textbase.size
        self._size = self.textbase.size
        
        self.basesize = self.textbase.get_size()
        #_renderd.createClock(self, font, format, lcase_ampm, justification, timezone, timezoneDisplay)
    
    def create_cimg(self):
        if self.fnt.shadow:
            newsurf = rg.pg.Surface((self._textsize[0]+abs(self.fnt.sx*2), self._textsize[1]+abs(self.fnt.sy*2)), rg.pg.SRCALPHA)
            newsurf.fill((0, 0, 0, 0))
            newsurf.blit(self.fnt.font.render(self.s, True, [c*255 for c in self.fnt.scol]), (self.fnt.sx, self.fnt.sy))
            newsurf.blit(self.fnt.font.render(self.s, True, [c*255 for c in self._color]), (0, 0))
        else:
            newsurf = rg.pg.Surface(self._textsize, rg.pg.SRCALPHA)
            newsurf.blit(self.fnt.font.render(self.s, True, [c*255 for c in self._color]), (0, 0))
        newsurf = rg.pg.transform.smoothscale_by(newsurf, (1, 0.93))
        buf = BytesIO()
        rg.pg.image.save(newsurf, buf, ".bmp")
        self.cimg = rg.rl.load_image_from_memory(".bmp", buf.getvalue(), len(buf.getvalue()))
        rg.rl.image_alpha_premultiply(self.cimg)


class TimeCode(GraphicRenderable):

    def __init__(self, font):
        GraphicRenderable.__init__(self)
        

from io import BytesIO
import builtins

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

class Text(GraphicRenderable):

    def __init__(self, font : TTFont, str):
        GraphicRenderable.__init__(self)
        self.fnt = font
        self.s = builtins.str(str)
        self.lasts = builtins.str(self.s)
        self.bounds = None
        self.cachedimg = None
        self.cachedtex = None
        self.buf = BytesIO()
        self.ascent = self.fnt.font.get_ascent()
        self.descent = self.fnt.font.get_descent()
        
        
        self.textbase : rg.pg.Surface = self.fnt.font.render(builtins.str(self.s), True, (255, 255, 255))
        self.textbase = rg.pg.transform.smoothscale_by(self.textbase, (1, 0.93))
        
        self.basesize = self.textbase.get_size()
        self._lastcol = tuple(list(self._color))
        self._textsize = self.textbase.size
        self._size = self.textbase.size
        self.cimg = None
    
    def create_cimg(self):
        if self.fnt.shadow:
            newsurf = rg.pg.Surface((self._textsize[0]+abs(self.fnt.sx*2), self._textsize[1]+abs(self.fnt.sy*2)), rg.pg.SRCALPHA)
            newsurf.fill((0, 0, 0, 0))
            newsurf.blit(self.fnt.font.render(self.s, True, [c*255 for c in self.fnt.scol]), (self.fnt.sx, self.fnt.sy))
            newsurf.blit(self.fnt.font.render(self.s, True, [c*255 for c in self._color]), (0, 0))
        else:
            newsurf = rg.pg.Surface(self._textsize, rg.pg.SRCALPHA)
            newsurf.blit(self.fnt.font.render(self.s, True, [c*255 for c in self._color]), (0, 0))
        newsurf = rg.pg.transform.smoothscale_by(newsurf, (1, 0.93))
        buf = BytesIO()
        rg.pg.image.save(newsurf, buf, ".bmp")
        self.cimg = rg.rl.load_image_from_memory(".bmp", buf.getvalue(), len(buf.getvalue()))
        rg.rl.image_alpha_premultiply(self.cimg)
    
    def unload(self):
        if self.cimg:
            rg.rl.unload_image(self.cimg)
            self.cimg = None
        if self.cachedimg:
            rg.rl.unload_image(self.cachedimg)
            self.cachedimg = None
        if self.cachedtex:
            rg.rl.unload_texture(self.cachedtex)
            self.cachedtex = None

    def font(self):
        return self.fnt
        return

    def str(self):
        return self.s
        return

    def size(self):
        return self.basesize

    def setBoundingBoxSize(self, w, h):
        self.bounds = (w, h)
    
    def setColor(self, r=0, g=0, b=0, a=1):
        super().setColor(r, g, b, a)
        if self.cimg:
            rg.rl.unload_image(self.cimg)
            self.cimg = None
        self.create_cimg()
        return
        


class Marquee(Text):

    def __init__(self, font, str, step=2, repeat=1):
        Text.__init__(self, font, str)
        
        self.step = step
        self.repeat = repeat
        self.pos = 0
        return

    def setSpeed(self, step):
        #return _renderd.Marquee_setSpeed(self, step)
        self.step = step
        return


class QTMovie(GraphicRenderable):

    def __init__(self, name, evict=0):
        GraphicRenderable.__init__(self)
        _renderd.createQTMovie(self, name, evict)
        return

    def getNumFrames(self):
        return _renderd.QTMovie_getNumFrames(self)
        return

    def setLooping(self, looping):
        return _renderd.QTMovie_setLooping(self, looping)
        return

class Icon(GraphicRenderable):

    def __init__(self, name:str, evict=0):
        GraphicRenderable.__init__(self)
        if name.startswith("/rsrc/icons_s/"):
            name = name.replace("/rsrc/icons_s/", "/media/icons/small/", 1)
        
        if name.startswith("/rsrc/icons_m/"):
            name = name.replace("/rsrc/icons_m/", "/media/icons/medium/", 1)
        
        if name.startswith("/rsrc/icons_l/"):
            name = name.replace("/rsrc/icons_l/", "/media/icons/large/", 1)
        self.name = name
        self.evict = evict
        self.unloaded = False
        _renderd.createIcon(self, name, evict)
        return
    
    def unload(self):
        if self.unloaded:
            return
        if self.textures:
            for i, tx in enumerate(self.textures):
                if tx:
                    print(f"unloading texture {i}")
                    rg.rl.unload_texture(tx)
                tx = None
        if self._ims:
            print(self._ims)
            print(self.name)
            for i, im in enumerate(self._ims):
                if im:
                    print(f"unloading image {i}")
                    rg.rl.unload_image(im)
                self._ims[i] = None
        self.unloaded = True


class Image(GraphicRenderable):
    pass


class JPEG_Image(Image):

    def __init__(self, name, evict=0, x1=0, y1=0, x2=1, y2=1):
        Image.__init__(self)
        _renderd.createImage(self, name, evict, x1, y1, x2, y2)
        return
    def unload(self):
        if self.texture:
            print("Unloading Texture...")
            rg.rl.unload_texture(self.texture)
        if self.im2:
            print("Unloading Image...")
            rg.rl.unload_image(self.im2)


class TIFF_Image(Image):

    def __init__(self, name, evict=0, x1=0, y1=0, x2=1, y2=1):
        Image.__init__(self)
        _renderd.createImage(self, name, evict, x1, y1, x2, y2)
        return
    def unload(self):
        if self.texture:
            print("Unloading Texture...")
            rg.rl.unload_texture(self.texture)
            self.texture = None
        if self.im2:
            print("Unloading Image...")
            if rg.rl.is_image_valid(self.im2):
                rg.rl.unload_image(self.im2)
                self.im2 = None

class CompositedImage(Image):

    def __init__(self, debug=False):
        GraphicRenderable.__init__(self)
        self.rtex = None
        self.ftex = None
        self._size = (720, 480)
        self.items = []
        self.debug = debug
        return

    def unload(self):
        if self.rtex:
            rg.rl.unload_render_texture(self.rtex)
            self.rtex = None
        if self.ftex:
            rg.rl.unload_render_texture(self.ftex)
            self.ftex = None

    def addItem(self, child):
        self.items.append(child)
        return
    

class ClipboardImage(Image):

    def __init__(self):
        GraphicRenderable.__init__(self)
        #_renderd.createClipboardImage(self)
        return

import json
class VectorImage(GraphicRenderable):
    """A image made up of points, lines, and curves."""

    def __init__(self, name, lineThickness=1, evict=0):
        GraphicRenderable.__init__(self)
        self.polys = []
        self.lineThickness = lineThickness
        self.im = None
        self.tx = None
        if os.path.exists(name + ".vg"):
            with open(name + ".vg", "r") as f:
                fl = json.loads(f.read())
            self._size = (fl[0], fl[1])
            self.polys = fl[2]
            buf = BytesIO()
            tempsurf = rg.pg.Surface((fl[0], fl[1]), rg.pg.SRCALPHA)
            
            for pol in self.polys:
                for i in range(len(pol)):
                    if i == (len(pol)-1):
                        break
                    first = pol[i]
                    second = pol[i+1]
                    
                    rg.pg.draw.aaline(tempsurf, (255, 255, 255), first, second, self.lineThickness)
            rg.pg.image.save(tempsurf, buf, ".bmp")
            bv = buf.getvalue()
            self.im = rg.rl.load_image_from_memory(".bmp", bv, len(bv))
    
    def unload(self):
        if self.tx:
            rg.rl.unload_texture(self.tx)
            self.tx = None
        if self.im:
            rg.rl.unload_image(self.im)
            self.im = None
        #_renderd.createVectorImage(self, name, lineThickness, evict)


class CompositeRenderable(GraphicRenderable):

    def __init__(self, debug=False):
        GraphicRenderable.__init__(self)
        self.rtex = None
        self.ftex = None
        self._size = (720, 480)
        self.items = []
        self.debug = debug
        return

    def unload(self):
        if self.rtex:
            rg.rl.unload_render_texture(self.rtex)
            self.rtex = None
        if self.ftex:
            rg.rl.unload_render_texture(self.ftex)
            self.ftex = None

    def addItem(self, child):
        self.items.append(child)
        return

    def size(self):
        top = None
        right = None
        for child in self.items:
            pos = child.position()
            size = child.size()
            if not right:
                right = pos[0]+size[0]
            else:
                right = max(right, pos[0]+size[0])
            if not top:
                top = pos[1]+size[1]
            else:
                top = max(top, pos[1]+size[1])
        return (abs(right), abs(top))

class ScrollingCompositeRenderable(CompositeRenderable):

    def __init__(self, step=2, spacing=2, repeat=1):
        GraphicRenderable.__init__(self)
        self.step = step
        self.spacing = spacing
        self.repeat = repeat
        self.scroll = 0
        self.rtex = None
        self.ftex = None
        self.bbox = (720, 480)
        self.debug = False
        self.items = []
        return

    def unload(self):
        if self.rtex:
            rg.rl.unload_render_texture(self.rtex)
            self.rtex = None
        if self.ftex:
            rg.rl.unload_render_texture(self.ftex)
            self.ftex = None

    def setSpeed(self, step):
        self.step = step
        return

    def setSpacing(self, spacing):
        self.spacing = spacing
        return

    def setBoundingBoxSize(self, w, h):
        self.bbox = (w, h)
        self._size = (w, h)
        return

    def getBoundingBoxSize(self):
        return self.bbox
        return

    def addItem(self, child):
        self.items.append(child)
        return


class Polygon(GraphicRenderable):

    def __init__(self):
        GraphicRenderable.__init__(self)
        self.vertices = []
        self.leftmost = 0
        self.rightmost = 0
        self.topmost = 0
        self.bottommost = 0
        return

    def addVertex(self, x, y, r=1, g=1, b=1, a=1):
        self.vertices.append((rg.rl.Vector3(x, y, -rg.zzz), r, g, b, a))
        if x < self.leftmost:
            self.leftmost = x
        if y > self.topmost:
            self.topmost = y
        if x > self.rightmost:
            self.rightmost = x
        if y < self.bottommost:
            self.bottommost = y
        self._size = (abs(self.rightmost-self.leftmost), abs(self.topmost-self.bottommost))
        return


class RichText(CompositeRenderable):

    def __init__(self, textItemList):
        CompositeRenderable.__init__(self)
        w = 0
        h = 0
        tempList = []
        for item in textItemList:
            (strText, font, color) = item
            (r, g, b, a) = color
            gr = Text(font, strText)
            gr.setColor(r, g, b, a)
            gr.setPosition(w, font.sy)
            (wgr, hgr) = gr.size()
            tempList.append(gr)
            w += wgr
            if hgr > h:
                h = hgr

        self.setSize(w, h)
        for item in tempList:
            self.addItem(item)

        return


class Video(GraphicRenderable):

    def __init__(self):
        GraphicRenderable.__init__(self)
        return


class Effect(ObjectWrapper):

    def setTarget(self, target):
        return


class GraphicEffect(Effect):
    def setTarget(self, target):
        target.addGraphicEffect(self)


class NullEffect(GraphicEffect):

    def __init__(self, target=None):
        if target != None:
            self.setTarget(target)
        return


class Bounce(GraphicEffect):

    def __init__(self, target=None, dx=0, dy=0, x=0, y=0, h=720, w=480):
        self.frame = 0
        self.frozen = False
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if target != None:
            self.setTarget(target)
        return


class Slider(GraphicEffect):

    def __init__(self, target=None, dx=0, dy=0):
        self.frame = 0
        self.frozen = False
        self.dx = dx
        self.dy = dy
        if target != None:
            self.setTarget(target)
        return


class Sizer(GraphicEffect):

    def __init__(self, target=None, percentX=1, percentY=1):
        self.frame = 0
        self.frozen = False
        self.percentX = percentX
        self.percentY = percentY
        if target != None:
            self.setTarget(target)
        return


class Strobe(GraphicEffect):

    def __init__(self, target=None, variance=0.49, step=0.01):
        self.frame = 0
        self.frozen = False
        self.variance = variance
        self.step = step
        if target != None:
            self.setTarget(target)
        return


class Fader(GraphicEffect):
    def __init__(self, target=None, startAlpha=0, endAlpha=1, frames=30):
        self.frame = 0
        self.frozen = False
        self.startAlpha = startAlpha
        self.endAlpha = endAlpha
        self.frames = frames
        if target != None:
            self.setTarget(target)
        return


class Rotate(GraphicEffect):

    def __init__(self, target=None, angle=1, x=0, y=0, xr=0, yr=0, zr=0):
        self.frame = 0
        self.frozen = False
        self.angle = angle
        self.x = x
        self.y = y
        self.xr = xr
        self.yr = yr
        self.zr = zr
        if target != None:
            self.setTarget(target)
        return


class Clipper(GraphicEffect):
    CP_LEFT = 0
    CP_RIGHT = 1
    CP_TOP = 2
    CP_BOTTOM = 3

    def __init__(self, target=None, left=None, right=None, top=None, bottom=None):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        if target != None:
            self.setTarget(target)
        return

    def clip(self, plane, pos, step=0.0):
        #_renderd.Clipper_clip(self, plane, pos, step)
        return


class Snapshot(GraphicEffect):

    def __init__(self, target=None):
        _renderd.createSnapshot(self)
        if target != None:
            self.setTarget(target)
        return


class SetText(GraphicEffect):

    def __init__(self, str, target=None):
        self.s = str
        self.fired = False
        if target != None:
            self.setTarget(target)
        return


class PropertyEffect(GraphicEffect):
    pass


class SetColor(PropertyEffect):

    def __init__(self, target=None, r=0, g=0, b=0, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.fired = False
        if target != None:
            self.setTarget(target)
        return


class SetColorScale(PropertyEffect):

    def __init__(self, target=None, r=0, g=0, b=0, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        if target != None:
            self.setTarget(target)
        return


class SetSize(PropertyEffect):

    def __init__(self, target=None, w=1, h=1):
        self.w = w
        self.h = h
        self.fired = False
        if target != None:
            self.setTarget(target)
        return


class SetSizeScale(PropertyEffect):

    def __init__(self, target=None, w=1, h=1):
        self.w = w
        self.h = h
        if target != None:
            self.setTarget(target)
        return


class SetPosition(PropertyEffect):

    def __init__(self, target=None, x=0, y=0):
        self.x = x
        self.y = y
        if target != None:
            self.setTarget(target)
        return


class SetRotationAngle(PropertyEffect):

    def __init__(self, target=None, angle=1):
        self.angle = angle
        self.fired = False
        if target != None:
            self.setTarget(target)
        return


class SetAnimationState(Effect):

    def __init__(self, target=None, state=1):
        self.state = state
        if target != None:
            self.setTarget(target)
        return


class SetVisibility(Effect):

    def __init__(self, target=None, visible=1):
        self.visible = visible
        self.fired = False
        self.frame = 0
        self.frozen = False
        
        self.fader = None
        if target != None:
            self.setTarget(target)
        return


class AudioRenderable(Renderable):
    BLEND_OVERWRITE = 0
    BLEND_MIX = 1
    BLEND_ADD = 2

    def setVolLevel(self, level):
        self.level = level
        return

    def setMixLevel(self, level):
        self.mix = level
        return

    def setBlendType(self, type):
        self.btype = type
        return
    
    def addEffectSequencer(self, seq, repeat, loopLimit):
        self.effects.append(seq)

    def unload(self):
        if self.chan:
            self.chan.stop()
        if hasattr(self, "file"):
            if self.file:
                self.file.stop()

class Audio(AudioRenderable):

    def __init__(self):
        _renderd.createAudio(self)
        return


class AudioClip(AudioRenderable):

    def __init__(self, name, evict=0, duration_limit=0, loop_limit=1):
        _renderd.createAudioClip(self, name, evict, duration_limit, loop_limit)
        self.effects = []
        return

    def setLoopLimit(self, limit):
        self.loop_limit = limit
        return

    def duration(self):
        return (self.file.get_length()*30)
        return

    def size(self):
        return _renderd.AudioClip_getSize(self)
        return


class NullAudioClip(AudioRenderable):

    def __init__(self, duration_limit=0):
        self.duration_limit = duration_limit
        self.evict = 1
        self.loop_limit = 1
        self.level = 1
        self.mix = 1
        self.chan = None
        self.name = ""
        self.effects = []
        #_renderd.createAudioClip(self, "", 1, duration_limit, 1)
        return

    def duration(self):
        return self.duration_limit

    def size(self):
        return _renderd.NullAudioClip_getSize(self)
        return


class MP3_AudioClip(AudioRenderable):

    def __init__(self, name, evict=0, duration_limit=0, loop_limit=1):
        _renderd.createAudioClip(self, name, evict, duration_limit, loop_limit)
        self.effects = []
        return

    def setLoopLimit(self, limit):
        self.loop_limit = limit
        return

    def duration(self):
        return self.file.get_length()*30


class AudioEffect(Effect):
    def setTarget(self, target):
        target.addAudioEffect(self)

import random
class EffectSequencer(Renderable):

    def __init__(self, target, repeat=0, loopLimit=0):
        self.effects = []
        self.activeeffects = []
        self.timer = -1 #first frame is time 0 but 1 gets added first
        self.total = 0
        self.repeat = repeat
        self.loopLimit = loopLimit
        self.skipped = False
        target.addEffectSequencer(self, repeat, loopLimit)
        return

    def _eval_fader(self):
        if len(self.effects) > 1:
            for i in range(len(self.effects)-1):
                if (type(self.effects[i][0]) == SetVisibility) and (type(self.effects[i+1][0]) == Fader):
                    self.effects[i][0].fader = self.effects[i+1][0].startAlpha
                elif (type(self.effects[i][0]) == SetVisibility):
                    self.effects[i][0].fader = None
    
    def addEffect(self, effect, duration, confirm=False):
        self.effects.append((effect, duration))
        self.total += duration
        self._eval_fader()
        return


class ImageSequencer(Renderable):

    def __init__(self, repeat=0):
        self.repeat = repeat
        self.images = []
        return

    def addImage(self, imageFile, duration):
        self.images.append((imageFile, duration))
        return


class AudioSequencer(AudioRenderable):

    def __init__(self, repeat=0):
        self.timer = 0
        self.done = False
        self.playingidx = 0
        self.repeat = repeat
        self.audio = []
        self.effects = []
        self.level = 1
        self.mix = 1
        return

    def addItem(self, child):
        self.audio.append(child)
        return

    def duration(self):
        return sum([e.duration() for e in self.audio])-len(self.audio)
        return

    def size(self):
        return _renderd.AudioSequencer_getSize(self)
        return
    
    def unload(self):
        for a in self.audio:
            a.unload()
        self.audio = []

class AudioFader(AudioEffect):

    def __init__(self, target=None, startMixLevel=0, endMixLevel=1, frames=30):
        self.startMixLevel = startMixLevel
        self.endMixLevel = endMixLevel
        self.frames = frames
        self.frozen = False
        self.frame = 0
        if target != None:
            self.setTarget(target)
        return


class AudioEffectSequencer(Renderable):

    def __init__(self, target, repeat=0):
        self.total = 0
        self.effects = []
        self.activeeffects = []
        self.timer = -1 #first frame is time 0 but 1 gets added first
        self.repeat = repeat
        target.addEffectSequencer(self, repeat, 1)
        return

    def addEffect(self, effect, duration):
        self.effects.append((effect, duration))
        self.total += duration
        return


class AudioNullEffect(AudioEffect):

    def __init__(self, target=None):
        if target != None:
            self.setTarget(target)
        return


