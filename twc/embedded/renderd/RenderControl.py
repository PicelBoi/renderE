# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: RenderControl.py
# Compiled at: 2007-01-12 11:17:28
from . import _renderd
from .RenderScript import *
import rendereglobals as rg

def unloadLayer(l): #i'd deprecate this but it may still have some sort of value
    return
    if isinstance(l, Layer):
        for page in l.pages:
            unloadLayer(page)
    elif isinstance(l, Page):
        for item in l.elements:
            unloadLayer(item)
    elif isinstance(l, CompositeRenderable):
        for item in l.items:
            unloadLayer(item)
        if l.rtex:
            rg.rl.unload_render_texture(l.rtex)
        if l.ftex:
            rg.rl.unload_render_texture(l.ftex)
    elif isinstance(l, AudioSequencer):
        for item in l.audio:
            unloadLayer(item)
    elif isinstance(l, Text):
        if l.cachedtex:
            rg.rl.unload_texture(l.cachedtex)
    elif isinstance(l, Image):
        if l.im2:
            rg.rl.unload_image(l.im2)
            l.im2 = None
        if l.texture:
            rg.rl.unload_texture(l.texture)
            l.texture = None

rct = 0
rctb = 0
rctf = 0
import time as t
def actuallyRunAQueuedCommand(cmd):
    global rct, rctb, rctf
    print(f"processing command: {type(cmd).__name__}")
    if type(cmd) in (SetLayer, SetLayerCmd):
        ix = -1
        for i, layer in enumerate(rg.layers):
            if layer[0] == cmd.lname:
                ix = i+0
                break
        if ix > -1:
            unloadLayer(rg.layers[ix][1])
            rg.layers[ix][1] = cmd.layer
    elif type(cmd) in (AppendLayer, AppendLayerCmd):
        ix = -1
        print("appendlayer debug:")
        print(cmd.lname)
        print(cmd.layer.pages)
        for i, layer in enumerate(rg.layers):
            if layer[0] == cmd.lname:
                ix = i+0
                break
        print(ix)
        if ix > -1:
            if rg.layers[ix][1] is None:
                rg.layers[ix][1] = cmd.layer
            else:
                pg1 = cmd.layer.pages
                for p in pg1:
                    if p not in rg.layers[ix][1].pages:
                        rg.layers[ix][1].pages.append(p)
    elif type(cmd) in (CreateNamedLayer, CreateNamedLayerCmd):
        ix = -1
        for i, layer in enumerate(rg.layers):
            if layer[0] == cmd.lname:
                ix = i+0
                break
        if ix > -1:
            unloadLayer(rg.layers[ix][1])
        rg.layers.append([
            cmd.lname,
            None,
            0,
            0,
            cmd.depth,
            cmd.repeat,
            0,
            0,
            720,
            480,
            1,
            1,
            0,
            0,
            False
        ])
    elif isinstance(cmd, SetNamedLayerViewPortCmd):
        ix = -1
        for i, layer in enumerate(rg.layers):
            if layer[0] == cmd.lname:
                ix = i+0
                break
        if ix > -1:
            rg.layers[ix][6] = cmd.x
            rg.layers[ix][7] = cmd.y
            rg.layers[ix][8] = cmd.w
            rg.layers[ix][9] = cmd.h
            rg.layers[ix][10] = cmd.sx
            rg.layers[ix][11] = cmd.sy
            rg.layers[ix][12] = cmd.tx
            rg.layers[ix][13] = cmd.ty
    elif isinstance(cmd, ModifyNamedLayerCmd):
        ix = -1
        for i, layer in enumerate(rg.layers):
            if layer[0] == cmd.name:
                ix = i+0
                break
        if ix > -1:
            rg.layers[ix][0] = cmd.newName
            rg.layers[ix][4] = cmd.depth
            rg.layers[ix][5] = cmd.repeat
    elif type(cmd) in (DestroyNamedLayer, DestroyNamedLayerCmd):
        print("destroynamedlayer debug:")
        print(cmd.lname)
        ix = -1
        for i, layer in enumerate(rg.layers):
            if layer[0] == cmd.lname:
                ix = i+0
                break
        if ix > -1:
            unloadLayer(rg.layers[ix][1])
            del rg.layers[ix]
    elif isinstance(cmd, ReplaceLayerCmd):
        ix = -1
        for i, layer in enumerate(rg.layers):
            if layer[0] == cmd.name:
                ix = i+0
                break
        if ix > -1:
            rg.layers[ix][1] = cmd.layer
    elif type(cmd) in (ActivateLayer, ActivateLayerCmd):
        ix = -1
        for i, layer in enumerate(rg.layers):
            if layer[0] == cmd.lname:
                ix = i+0
                break
        if ix > -1:
            rg.layers[ix][14] = True
    elif type(cmd) in (DeactivateLayer, DeactivateLayerCmd):
        ix = -1
        for i, layer in enumerate(rg.layers):
            if layer[0] == cmd.lname:
                ix = i+0
                break
        if ix > -1:
            rg.layers[ix][14] = False
    elif type(cmd) in (LoadPresentation, LoadPresentationCmd):
        try:
            rg.runrscfunction(cmd.fileName.replace("\t", "\\t"))
        except:
            pass
    print(f"queued command has been processed! new queue length: {len(rg.queuedcommands)}")

def queueCommand(cmd, time=0, frameOffset=0, estimatedCmd=0):
    rg.queuedcommands.append([cmd, time, frameOffset, estimatedCmd])


def createNamedLayer(name, depth, repeat=0, autoDestroy=1, time=0, frameOffset=0):
    cmd = CreateNamedLayerCmd(name, depth, repeat, autoDestroy)
    return queueCommand(cmd, time, frameOffset)
    return


def destroyNamedLayer(name, time=0, frameOffset=0):
    cmd = DestroyNamedLayerCmd(name)
    return queueCommand(cmd, time, frameOffset)
    return


def modifyNamedLayer(name, newName, depth, repeat, autoDestroy, time=0, frameOffset=0):
    cmd = ModifyNamedLayerCmd(name, newName, depth, repeat, autoDestroy)
    return queueCommand(cmd, time, frameOffset)
    return
import time as _time

def setLayer(name, layer, time=0, frameOffset=0):
    cmd = SetLayerCmd(name, layer)
    return queueCommand(cmd, time, frameOffset)
    return


def appendLayer(name, layer, time=0, frameOffset=0):
    cmd = AppendLayerCmd(name, layer)
    return queueCommand(cmd, time, frameOffset)
    return


def replaceLayer(name, layer, time=0, frameOffset=0):
    cmd = ReplaceLayerCmd(name, layer)
    return queueCommand(cmd, time, frameOffset)
    return


def removeLayer(name, time=0, frameOffset=0):
    cmd = RemoveLayerCmd(name)
    return queueCommand(cmd, time, frameOffset)
    return


def activateLayer(name, time=0, frameOffset=0):
    cmd = ActivateLayerCmd(name)
    return queueCommand(cmd, time, frameOffset)
    return


def deactivateLayer(name, time=0, frameOffset=0):
    cmd = DeactivateLayerCmd(name)
    return queueCommand(cmd, time, frameOffset)
    return


def loadPresentation(fileName, time=0, frameOffset=0):
    cmd = LoadPresentationCmd(fileName)
    return queueCommand(cmd, time, frameOffset)
    return


def selectInputSource(avPort, time=0, frameOffset=0):
    cmd = SelectInputSourceCmd(avPort)
    return queueCommand(cmd, time, frameOffset, 1)
    return


def activateGpiPin(pin, time=0, frameOffset=0):
    cmd = ActivateGpiPinCmd(pin)
    return queueCommand(cmd, time, frameOffset)
    return


def deactivateGpiPin(pin, time=0, frameOffset=0):
    cmd = DeactivateGpiPinCmd(pin)
    return queueCommand(cmd, time, frameOffset)
    return


