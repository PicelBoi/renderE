import pyray as rl
import pygame as pg
import os
import json
import sys
from pathlib import PurePath

def newjoin(*args):
    pp = PurePath(*args).as_posix()
    jp = os.path.join(*args)
    if jp.endswith("/") or jp.endswith("\\") and not (pp.endswith("/")):
        pp = pp + "/"
    # if pp != jp:
    #     print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    #     print(pp, jp)
    #     exit()
    pp = pp.replace("\\", "/")
    if pp.startswith("/media/backgrounds/"):
        pp = pp.replace("/media/backgrounds/", "net/media/backgrounds/", 1)
    return pp

pg.font.init()
pg.mixer.init(frequency=48000, size=-16, channels=2)

sys.path.insert(0, os.path.dirname(__file__))

zzz = 10

layers = []
queuedcommands = []
unloadqueue = []
datastore = {}
configs = {}
sessiondata = [{}, {}]
sessiondelete = [set(), set()]
runrsfunction = None
runrscfunction = None
newaccess = None
newstat = None
newexists = None
font_cache = {}

#optionally, specify your environment vars here

os.environ["RENDEREROOT"] = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
os.environ["TWCCLIDIR"] = ""
os.environ["TWCPERSDIR"] = newjoin(os.environ["RENDEREROOT"], "domesticpy")
os.environ["TWCDIR"] = ""
os.environ["RENDERERSRC"] = ""
os.environ["RENDEREMEDIA"] = ""
os.environ["RENDEREDOMESTIC"] = ""

if os.path.exists(newjoin(os.environ["RENDEREROOT"], "ds.json")):
    with open(newjoin(os.environ["RENDEREROOT"], "ds.json"), "r") as f:
        datastore = json.loads(f.read())

#os.environ["RENDEREROOT"] = "/path/to/renderE"
#os.environ["RENDERERSRC"] = "/usr/local/twc/rsrc"
#os.environ["RENDEREMEDIA"] = "/media"
#os.environ["RENDEREDOMESTIC"] = "/usr/twc/domestic"
#os.environ["TWCCLIDIR"] = "/usr/twc"
#os.environ["TWCPERSDIR"] = "/path/to/renderE/domesticpy"
#os.environ["TWCDIR"] = "/usr/twc"
