# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: __init__.py
# Compiled at: 2007-01-12 11:17:30
import glob, os, os.path, twccommon, twccommon.Log as Log, twc.dsmarshal as dsm, twc.psp, urllib, lxml.etree
from . import SkyConditionCodes
import nethandler
Data = twccommon.Data
DefaultedData = twccommon.DefaultedData

personality = nethandler.personality

def getAttribList(keys, default=None):
    """Get a merged together list of attributes specified
    by the given keys.  If default is specified then that 
    structure is merged in first.
    """
    if default == None:
        default = twccommon.Data()
    attribList = []
    for key in keys:
        try:
            attribList.append(dsm.get(key))
        except:
            pass

    return twccommon.mergeStructs(attribList, default)
    return


def writePid(pidFileName):
    f = open(pidFileName, 'w')
    pid = os.getpid()
    f.write('%d\n' % pid)
    f.close()
    return


def sendNotification(error):
    heId = 'Unknown'
    starId = 'Unknown'
    disable = 0
    notify = 'default'
    try:
        disable = dsm.defaultedGet('disableMonitor', 0)
        heId = dsm.defaultedGet('headendId', 'Unknown')
        starId = dsm.defaultedGet('starId', 'Unknown')
        notify = dsm.defaultedGet('notifyUrl', 'https://starlog.weather.com/starnotify')
    except:
        pass

    try:
        Log.error('Error Notification: %s' % error)
        if disable == 0:
            tmp = urllib.urlopen('%s?heId=%s&starId=%s&msg=%s' % (notify, heId, starId, error))
            tmp.close()
    except:
        Log.critical('Unknown exception trying to send error notification')

    return


def setStaticValue(key, value):
    path = '%s/%s' % (_STATIC_VAR_DIR, key)
    f = open(path, 'w')
    f.write(repr(value))
    f.close()
    return


def getStaticKeys():
    return map((lambda e: os.path.basename(e)), glob.glob('%s/*' % _STATIC_VAR_DIR))
    return


def getStaticValue(key, default=None):
    path = '%s/%s' % (_STATIC_VAR_DIR, key)
    try:
        f = open(path)
    except IOError:
        return default

    s = f.read()
    f.close()
    return eval(s)
    return


def getStaticItems():
    keys = getStaticKeys()
    values = map((lambda e: (e, getStaticValue(e))), keys)
    return values
    return

import rendereglobals as rg

def buildPyNamespace(default=None, **namespace):
    ns = {}
    ns["newaccess"] = rg.newaccess
    ns["newstat"] = rg.newstat
    ns["newexists"] = rg.newexists
    ns["newjoin"] = rg.newjoin
    if default != None:
        ns.update(default)
    ns.update(namespace)
    return ns
    return


def presToRenderScript(pres, layerName, **ns):
    doc = None
    result = None
    try:
        ns = buildPyNamespace(default=ns)
        psppres = twc.psp.evalPage(pres, ns)
        doc = lxml.etree.XML(psppres)
        result = _presXslt.applyStylesheet(doc, {'LAYER': (repr(layerName))})
        output = _presXslt.saveResultToString(result)
    finally:
        if doc != None:
            doc.freeDoc()
        if result != None:
            result.freeDoc()
    return output
    return


def findRsrc(rsrc, ext, req=1, language=None):
    rsrcRoot = [os.environ["RENDEREMEDIA"], os.environ["RENDERERSRC"], "net/rsrc", "net/media"]
    for path in rsrcRoot:
        searchFile = '%s%s' % (path, rsrc)
        if "backgroun" in rsrc:
            print("SEARCH RSRC", searchFile)
        if language:
            splitSearchFile = os.path.split(searchFile)
            languageSearchFile = '%s/%s/%s' % (splitSearchFile[0], language, splitSearchFile[1])
            if os.path.exists('%s.%s' % (languageSearchFile, ext)):
                return languageSearchFile
        if os.path.exists('%s.%s' % (searchFile, ext)):
            return searchFile

    netRoot = ["/media", "/rsrc"]
    for path in netRoot:
        searchFile = '%s%s' % (path, rsrc)
        if language:
            splitSearchFile = os.path.split(searchFile)
            languageSearchFile = '%s/%s/%s' % (splitSearchFile[0], language, splitSearchFile[1])
            netf = nethandler.requestNetAssetExt(languageSearchFile, ext)
            if netf:
                return languageSearchFile
        netf = nethandler.requestNetAssetExt(searchFile, ext)
        if netf:
            return searchFile

    if req:
        Log.error('File %s.%s does not exist in either /media or /rsrc' % (rsrc, ext))
        raise RuntimeError('File %s.%s does not exist in either /media or /rsrc' % (rsrc, ext))
    else:
        Log.warning('File %s.%s does not exist in either /media or /rsrc' % (rsrc, ext))
        return None
    return


def findRsrcList(rsrc, req=1):
    rsrcRoot = ['/media', '/rsrc']
    for path in rsrcRoot:
        file = '%s%s' % (path, rsrc)
        rsrcList = glob.glob(file)
        if len(rsrcList) > 0:
            return rsrcList

    if req:
        Log.error('File %s does not exist in either /media or /rsrc' % rsrc)
        raise RuntimeError('File %s does not exist in either /media or /rsrc' % rsrc)
    else:
        return []
    return


_STATIC_VAR_DIR = os.environ['TWCCLIDIR'] + '/data/staticCfg'
_presStylesheet = '<?xml version=\'1.0\'?>\n<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">\n\n<xsl:output omit-xml-declaration="yes" method="text" indent="no" />\n\n<xsl:template match="/pres">\nimport twc\nimport twccommon\nimport twc.embedded.renderd.RenderControl as RenderControl\nfrom twc.embedded.renderd.RenderScript import *\n\n\ndef last(*p):\n    return p[-1]\n\n\ndef lastValid(*p):\n    l = list(p)\n    l.reverse\n    \n    last = None\n    for e in l:\n        if not e:\n            break\n            \n        last = e\n        \n    return last\n\n\ndef parseBool(str):\n    if str == \'true\':\n        return 1\n    else:\n        return 0\n\n\ndef __makeMarquee(mdef):\n    gr = ScrollingCompositeRenderable()\n    gr.setPosition(mdef.x, mdef.y)\n    gr.setBoundingBoxSize(mdef.w, mdef.h)\n    gr.setSpeed(mdef.speed)\n    if mdef.spacing != None:\n        gr.setSpacing(mdef.spacing)\n        \n    for cdef in mdef.contents:\n        c = apply(cdef.maker, (cdef, ))\n        gr.addItem(c)\n        \n    return gr\n\n\ndef __makeBox(mdef):\n    gr = Box()\n    gr.setPosition(mdef.x, mdef.y)\n    gr.setSize(mdef.w, mdef.h)\n    gr.setColor(mdef.r, mdef.g, mdef.b, mdef.a)\n    return gr\n\n\ndef __makeText(mdef):\n    fname = \'/rsrc/fonts/%s\' % mdef.font\n    f = TTFont(fname, mdef.ps, t=mdef.t, shadow=mdef.shadow)\n    gr = Text(f, mdef.text)\n    gr.setPosition(mdef.x, mdef.y)\n    gr.setColor(mdef.r, mdef.g, mdef.b, mdef.a)\n    return gr\n\n\ndef __makeClock(mdef):\n    fname = \'/rsrc/fonts/%s\' % mdef.font\n    f = TTFont(fname, mdef.ps, t=mdef.t, shadow=mdef.shadow)\n    gr = Clock(f, mdef.format)\n    gr.setPosition(mdef.x, mdef.y)\n\n    tw, th = gr.size()\n    w = mdef.w\n    if w == None:\n        w = tw\n    h = mdef.h\n    if h == None:\n        h = th\n    gr.setSize(w, h)\n    gr.setColor(mdef.r, mdef.g, mdef.b, mdef.a)\n    return gr\n\n\ndef __makeTimeCode(mdef):\n    fname = \'/rsrc/fonts/%s\' % mdef.font\n    f = TTFont(fname, mdef.ps, t=mdef.t, shadow=mdef.shadow)\n    gr = TimeCode(f)\n    gr.setPosition(mdef.x, mdef.y)\n\n    tw, th = gr.size()\n    w = mdef.w\n    if w == None:\n        w = tw\n    h = mdef.h\n    if h == None:\n        h = th\n    gr.setSize(w, h)\n    gr.setColor(mdef.r, mdef.g, mdef.b, mdef.a)\n    return gr\n\n\ndef __makeIcon(mdef):\n    gr = Icon(mdef.src)\n\n    tw, th = gr.size()\n    w = mdef.w\n    if w == None:\n        w = tw\n    h = mdef.h\n    if h == None:\n        h = th\n\n    gr.setPosition(mdef.x, mdef.y)\n    gr.setSize(w, h)\n    #gr.setColor(mdef.r, mdef.g, mdef.b, mdef.a)\n    return gr\n\n\ndef __makeImage(mdef):\n    gr = TIFF_Image(mdef.src)\n    \n    tw, th = gr.size()\n    w = mdef.w\n    if w == None:\n        w = tw\n    h = mdef.h\n    if h == None:\n        h = th\n        \n    gr.setPosition(mdef.x, mdef.y)\n    gr.setSize(w, h)\n    #gr.setColor(mdef.r, mdef.g, mdef.b, mdef.a)\n    return gr\n\n\ndef __makePolygon(mdef):\n    gr = Polygon()\n    for x, y, r, g, b, a in mdef.verticies:\n        gr.addVertex(x, y, r, g, b, a)\n    gr.setPosition(mdef.x, mdef.y)\n    return gr\n\n\n__pdefs = {}\n\n<xsl:apply-templates select="pages"/>\n\n__pages = []\n__start = 0\n__seq   = 1\n\n<xsl:apply-templates select="schedule"/>\n\n__p = Page(__start)\nfor __page in __pages:\n    for __item in __page.items:\n        __item.setVisibility(0)\n        __item.setAnimationState(0)\n        \n        __es = EffectSequencer(__item)\n        if __page.start > 0:\n            __es.addEffect(NullEffect(), __page.start)\n        else:\n            __es.addEffect(NullEffect(), 1)\n        __es.addEffect(SetAnimationState(state=1), 1)\n        __es.addEffect(SetVisibility(visible=1), 1)\n        __es.addEffect(NullEffect(), __page.duration-1)\n        __es.addEffect(SetAnimationState(state=0), 1)\n        __es.addEffect(SetVisibility(visible=0), 1)\n            \n        __p.addItem(__es)\n        __p.addItem(__item)\n\n__l = Layer()\n__l.addPage(__p)\nlname = "<xsl:value-of select="$LAYER" />"\nRenderControl.setLayer(lname, __l)\n</xsl:template>\n\n\n<xsl:template match="pages">\n<xsl:apply-templates select="page" mode="pages" />\n</xsl:template>\n\n\n<xsl:template match="page" mode="pages">\n__contents = []\n__pdef = twccommon.Data()\n\n<xsl:apply-templates select="box|text|marquee|icon|image|polygon|clock|timecode" />\n\n__pdef.contents = __contents\n__pdefs["<xsl:value-of select="@id" />"] = __pdef\n</xsl:template>\n\n\n<xsl:template match="schedule">\n<xsl:apply-templates select="seq|par|page" mode="schedule" />\n</xsl:template>\n\n\n<xsl:template match="page" mode="schedule">\n__pdef = __pdefs["<xsl:value-of select="@id" />"]\n\n__page = twccommon.Data()\n__page.start = __start\n__page.duration = <xsl:value-of select="@duration" />\n__page.items = []\nfor mdef in __pdef.contents:\n    gr = apply(mdef.maker, (mdef, ))\n    __page.items.append(gr)\n\n__pages.append(__page)\n\nif __seq:\n    __start += __page.duration\n</xsl:template>\n\n\n<xsl:template match="par" mode="schedule">\n__seq = 0\n<xsl:apply-templates select="seq|par|page" mode="schedule" />\n</xsl:template>\n\n\n<xsl:template match="seq" mode="schedule">\n__seq = 1\n__startSave = __start\n\n<xsl:apply-templates select="seq|par|page" mode="schedule" />\n\n__start = __startSave\n</xsl:template>\n\n\n<xsl:template match="marquee">\n__mdef = twccommon.Data()\n__mdef.maker   = __makeMarquee\n\n__mdef.x       = last(0, <xsl:value-of select="@x" />)\n__mdef.y       = last(0, <xsl:value-of select="@y" />)\n__mdef.w       = last(0, <xsl:value-of select="@w" />)\n__mdef.h       = last(0, <xsl:value-of select="@h" />)\n__mdef.speed   = last(1, <xsl:value-of select="@speed" />)\n__mdef.spacing = last(None, <xsl:value-of select="@spacing" />)\n\n__mdefSave     = __mdef\n__contentsSave = __contents\n__contents     = []\n\n<xsl:apply-templates select="box|text|marquee|icon|image|polygon|clock|timecode" />\n\n__mdef          = __mdefSave\n__mdef.contents = __contents\n__contents      = __contentsSave\n__contents.append(__mdef)\n</xsl:template>\n\n\n<xsl:template match="box">\n__mdef = twccommon.Data()\n__mdef.maker   = __makeBox\n\n__mdef.x    = last(0, <xsl:value-of select="@x" />)\n__mdef.y    = last(0, <xsl:value-of select="@y" />)\n__mdef.w    = last(0, <xsl:value-of select="@w" />)\n__mdef.h    = last(0, <xsl:value-of select="@h" />)\n__mdef.r    = last(0, <xsl:value-of select="@r" />)\n__mdef.g    = last(0, <xsl:value-of select="@g" />)\n__mdef.b    = last(0, <xsl:value-of select="@b" />)\n__mdef.a    = last(1, <xsl:value-of select="@a" />)\n\n__contents.append(__mdef)\n</xsl:template>\n\n\n<xsl:template match="icon">\n__mdef = twccommon.Data()\n__mdef.maker   = __makeIcon\n\n__mdef.src  = "<xsl:value-of select="@src" />"\n__mdef.x    = last(0, <xsl:value-of select="@x" />)\n__mdef.y    = last(0, <xsl:value-of select="@y" />)\n__mdef.w    = last(None, <xsl:value-of select="@w" />)\n__mdef.h    = last(None, <xsl:value-of select="@h" />)\n__mdef.r    = last(0, <xsl:value-of select="@r" />)\n__mdef.g    = last(0, <xsl:value-of select="@g" />)\n__mdef.b    = last(0, <xsl:value-of select="@b" />)\n__mdef.a    = last(1, <xsl:value-of select="@a" />)\n\n__contents.append(__mdef)\n</xsl:template>\n\n\n<xsl:template match="image">\n__mdef = twccommon.Data()\n__mdef.maker   = __makeImage\n\n__mdef.src  = "<xsl:value-of select="@src" />"\n__mdef.x    = last(0, <xsl:value-of select="@x" />)\n__mdef.y    = last(0, <xsl:value-of select="@y" />)\n__mdef.w    = last(None, <xsl:value-of select="@w" />)\n__mdef.h    = last(None, <xsl:value-of select="@h" />)\n__mdef.r    = last(0, <xsl:value-of select="@r" />)\n__mdef.g    = last(0, <xsl:value-of select="@g" />)\n__mdef.b    = last(0, <xsl:value-of select="@b" />)\n__mdef.a    = last(1, <xsl:value-of select="@a" />)\n\n__contents.append(__mdef)\n</xsl:template>\n\n\n<xsl:template match="text">\n__mdef = twccommon.Data()\n__mdef.maker   = __makeText\n\n__mdef.font = lastValid(\'Interstate-Bold\', \'<xsl:value-of select="@font" />\')\n__mdef.ps   = last(12, <xsl:value-of select="@ps" />)\n__mdef.text = "<xsl:value-of select="." />"\n__mdef.x    = last(0, <xsl:value-of select="@x" />)\n__mdef.y    = last(0, <xsl:value-of select="@y" />)\n__mdef.r    = last(0, <xsl:value-of select="@r" />)\n__mdef.g    = last(0, <xsl:value-of select="@g" />)\n__mdef.b    = last(0, <xsl:value-of select="@b" />)\n__mdef.a    = last(1, <xsl:value-of select="@a" />)\n__mdef.shadow = last(0, <xsl:value-of select="@shadow" />)\n__mdef.t = last(0, <xsl:value-of select="@t" />)\n\n__contents.append(__mdef)\n</xsl:template>\n\n\n<xsl:template match="clock">\n__mdef = twccommon.Data()\n__mdef.maker   = __makeClock\n\n__mdef.font   = lastValid(\'Interstate-Bold\', \'<xsl:value-of select="@font" />\')\n__mdef.format = lastValid(\'%s\', \'<xsl:value-of select="@format" />\')\n__mdef.ps     = last(12, <xsl:value-of select="@ps" />)\n__mdef.x      = last(0, <xsl:value-of select="@x" />)\n__mdef.y      = last(0, <xsl:value-of select="@y" />)\n__mdef.w      = last(None, <xsl:value-of select="@w" />)\n__mdef.h      = last(None, <xsl:value-of select="@h" />)\n__mdef.r      = last(0, <xsl:value-of select="@r" />)\n__mdef.g      = last(0, <xsl:value-of select="@g" />)\n__mdef.b      = last(0, <xsl:value-of select="@b" />)\n__mdef.a      = last(1, <xsl:value-of select="@a" />)\n__mdef.shadow = last(0, <xsl:value-of select="@shadow" />)\n__mdef.t      = last(0, <xsl:value-of select="@t" />)\n\n__contents.append(__mdef)\n</xsl:template>\n\n\n<xsl:template match="timecode">\n__mdef = twccommon.Data()\n__mdef.maker   = __makeTimeCode\n\n__mdef.font   = lastValid(\'Interstate-Bold\', \'<xsl:value-of select="@font" />\')\n__mdef.ps     = last(12, <xsl:value-of select="@ps" />)\n__mdef.x      = last(0, <xsl:value-of select="@x" />)\n__mdef.y      = last(0, <xsl:value-of select="@y" />)\n__mdef.w      = last(None, <xsl:value-of select="@w" />)\n__mdef.h      = last(None, <xsl:value-of select="@h" />)\n__mdef.r      = last(0, <xsl:value-of select="@r" />)\n__mdef.g      = last(0, <xsl:value-of select="@g" />)\n__mdef.b      = last(0, <xsl:value-of select="@b" />)\n__mdef.a      = last(1, <xsl:value-of select="@a" />)\n__mdef.shadow = last(0, <xsl:value-of select="@shadow" />)\n__mdef.t      = last(0, <xsl:value-of select="@t" />)\n\n__contents.append(__mdef)\n</xsl:template>\n\n\n<xsl:template match="polygon">\n__mdef = twccommon.Data()\n__mdef.maker   = __makePolygon\n\n__mdef.x    = last(0, <xsl:value-of select="@x" />)\n__mdef.y    = last(0, <xsl:value-of select="@y" />)\n\n__verticies = []\n<xsl:apply-templates select="vertex"/>\n__mdef.verticies = __verticies\n\n__contents.append(__mdef)\n</xsl:template>\n\n\n<xsl:template match="vertex">\n__verticies.append((\n    last(1, <xsl:value-of select="@x" />),\n    last(1, <xsl:value-of select="@y" />),\n    last(1, <xsl:value-of select="@r" />),\n    last(1, <xsl:value-of select="@g" />),\n    last(1, <xsl:value-of select="@b" />),\n    last(1, <xsl:value-of select="@a" />),\n))\n</xsl:template>\n\n</xsl:stylesheet>\n'
_presXml = lxml.etree.XML(_presStylesheet)
_presXslt = lxml.etree.XSLT(_presXml)

