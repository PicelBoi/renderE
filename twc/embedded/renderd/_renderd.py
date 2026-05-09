import rendereglobals as rg
from PIL import Image
from io import BytesIO
import os
import glob
import nethandler
import libmv
rl = rg.rl
pg = rg.pg

def parsePath(path : str):
    if path.startswith("/rsrc"):
        return path.replace("/rsrc", os.environ["RENDERERSRC"], 1)
    if path.startswith("/media"):
        return path.replace("/media", os.environ["RENDEREMEDIA"], 1)
    return path

def createImage(self, name, evict=0, x1=0, y1=0, x2=1, y2=1):
    ogname = name+""
    pname = parsePath(name)
    possible = glob.glob(pname+".*")
    print(possible)
    if len(possible) > 0:
        name = possible[0]
    else:
        name = nethandler.requestNetAsset(name, "gfx")
    if not name:
        print(f"No suitable image found for {ogname}!")
        exit(1)
    
    im = Image.open(name).convert("RGBA")
    arr = BytesIO()
    im.save(arr, format="PNG")
    arr = arr.getvalue()
    self.im2 = rl.load_image_from_memory('.png', arr, len(arr))
    self.texture = None
    self._size = (self.im2.width, self.im2.height)

def createIcon(self, name, evict=0):
    ogname = name+""
    pname = parsePath(name)
    possible = glob.glob(pname+".mv")
    print(possible)
    if len(possible) > 0:
        name = possible[0]
    else:
        name = nethandler.requestNetAssetExt(name, "mv")
    if not name:
        print(f"No suitable icon found for {ogname}!")
        exit(1)
    
    with open(name, "rb") as f:
        data = f.read()
    
    print("loading mv ", name)
    self._frames = libmv.loadmv(data)
    
    #self._rframes = [rl.ffi.new('char []', fr.tobytes()) for fr in self._frames]
    self.idx = 0
    self.framect = len(self._frames)

    self._ims = []
    for f in self._frames:
        arr = BytesIO()
        f.save(arr, format="PNG")
        arr = arr.getvalue()
        img = rl.load_image_from_memory('.png', arr, len(arr))
        self._ims.append(img)
    
    self.textures = None
    self._size = (self._ims[0].width, self._ims[0].height)

def createTTFont(self, name, pointSize, shadow, sr=0.08, sg=0.08, sb=0.08, sa=1.0, sx=1, sy=2, t=0, l=None, evict=0):
    self.pxSize = round(pointSize * 0.95)
    if (name, self.pxSize) in rg.font_cache:
        cached = rg.font_cache[(name, pointSize)]
        self.font = cached
    else:
        ogname = name+""
        pname = parsePath(name)
        possible = glob.glob(pname+".*")
        if len(possible) > 0:
            name = possible[0]
        else:
            name = nethandler.requestNetAsset(name, "font")
        if not name:
            print(f"No suitable font found for {ogname}!")
            exit(1)
        
        self.font = pg.Font(name, self.pxSize)
        rg.font_cache[(name, self.pxSize)] = self.font
    self.scol = (sr, sg, sb, sa)
    self.ascent = self.font.get_ascent()
    self.descent = self.font.get_descent()
    self.cachedtex = None
    
    ag = self.font.render("Ag", True, (255, 255, 255)).get_height()
    ag2 = self.font.render("Ag\nAg", True, (255, 255, 255)).get_height()
    self.reallineheight = ag2-ag

def createAudio(self):
    return

def createAudioClip(self, name, evict=0, duration_limit=0, loop_limit=1):
    ogname = name+""
    pname = parsePath(name)
    if os.path.exists(pname):
        name = ogname
    else:
        name = nethandler.requestNetAssetExt(name)
    if not name:
        print(f"No suitable sound found for {ogname}!")
        exit(1)
    self.name = name
    self.file = rg.pg.Sound(name)
    
    self.chan = None
    self.evict = evict
    self.duration_limit = duration_limit
    self.time_played = 0
    self.loop_limit = loop_limit
    self.level = 1
    self.mix = 1
    self.single_play = 0
    self.btype = 1