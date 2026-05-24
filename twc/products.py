# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: products.py
# Compiled at: 2007-01-12 11:17:30
import lxml.etree, string, twc.DataStoreInterface as ds, twc.dsmarshal as dsm, twc.psp, twccommon, xml.dom.minidom
from functools import reduce
import loadtools
import os
class Product:

    def __init__(self, params):
        self.__duration = 0
        self.__rs = None
        self.__pres = None
        self.__pageDurations = []
        self.__params = params
        self.__data = twc.Data()
        self.__testData = twc.Data()
        self.__label = []
        return

    def getName(self):
        return self.__params.product
        return
    
    def getProdInstance(self):
        return self.__params.prodInst
        return

    def getShortName(self):
        return self.__params.prodName
        return

    def getType(self):
        return self.__params.prodType
        return

    def getParams(self):
        return self.__params
        return

    def updateParams(self, other=None, **params):
        self.__params.update(other, **params)
        return

    def getTestData(self):
        return self.__testData
        return

    def updateTestData(self, other=None, **params):
        self.__testData.update(other, **params)
        return

    def getData(self):
        return self.__data
        return

    def updateData(self, other=None, **params):
        self.__data.update(other, **params)
        return

    def getDuration(self):
        return self.__duration
        return

    def setDuration(self, duration):
        self.__duration = duration
        return

    def getDesiredDuration(self, minimum, maximum, optimal):
        if self.active():
            return self._getDesiredDuration(minimum, maximum, optimal)
        else:
            return 0
        return

    def getDesiredPageDurations(self, pageParams):
        if self.active():
            return self._getDesiredPageDurations(pageParams)
        else:
            return [0] * len(pageParams)
        return

    def getPageDurations(self):
        return self.__pageDurations
        return

    def setPageDurations(self, durations):
        self.__pageDurations = durations
        return
    
    def getLabel(self):
        return self.__label
        return

    def setLabel(self, label):
        self.__label = label
        return

    def addLabel(self, label, duration, image=None):
        d = twc.Data(label=label, duration=duration, image=image)
        self.__label.append(d)
        return

    def active(self):
        return 1
        return

    def loadData(self):
        self._loadData()
        return

    def setRenderScript(self, rs):
        self.__rs = rs
        return

    def setPresentation(self, pres):
        self.__pres = pres
        return

    def genRenderScript(self, layerName, pspIncludePath=None, **ns):
        ns = twc.buildPyNamespace(default=ns, params=self.__params, prod=self)
        if self.__rs:
            self.__params.layerName = layerName

            inclpaths = list(pspIncludePath)
            reppaths = [e.replace("/usr/twc/domestic", os.environ["RENDEREDOMESTIC"]) for e in inclpaths]

            print(reppaths)
            rsc = twc.psp.evalPage(self.__rs, ns, reppaths+inclpaths)
            return rsc
        elif self.__pres:
            return twc.presToRenderScript(self.__pres, layerName, **ns)
        else:
            return None
        return

    def _getDesiredDuration(self, minimum, maximum, optimal):
        return optimal
        return

    def _getDesiredPageDurations(self, pageParams):
        raise Exception('Multipage support not enabled for this product')
        return

    def _loadData(self):
        return


class DeactivateableProduct(Product):

    def active(self):
        pname = self.getName()
        fname = 'active%s' % (pname,)
        active = getattr(self.getParams(), fname, 1)
        return active
        return


class ProductLoader:

    def __init__(self):
        self.__prodMap = {}
        return

    def startProdType(self, prodType):
        return

    def loadProduct(self, prodType, prodName, prodInst):
        return

    def loadProductFile(self, fname, params):
        print("LOADPRODUCTFILE ", fname)
        try:
            (prodClass, rs, pres) = self.__prodMap[fname]
        except KeyError:
            (prodClass, rs, pres) = self._loadProductFile(fname)
            self.__prodMap[fname] = (prodClass, rs, pres)

        return self._makeProduct(prodClass, rs, pres, params)
        return

    def flush(self):
        self.__prodMap.clear()
        return

    def _makeProduct(self, prodClass, rs, pres, params):
        prod = prodClass(params)
        if rs:
            prod.setRenderScript(rs)
        elif pres:
            prod.setPresentation(pres)
        if prod.active():
            prod.loadData()
        else:
            prod = None
        return prod
        return

    def _parseProductDoc(self, doc):
        dom = None
        try:
            try:
                dom = xml.dom.minidom.parseString(doc)
            except Exception as e:
                with open("doc_crash.txt", "w") as f:
                    f.write(doc)
                raise e
            impls = dom.documentElement.getElementsByTagName('impl')
            prodClass = _processImpls(impls)
            rss = dom.documentElement.getElementsByTagName('rs')
            press = dom.documentElement.getElementsByTagName('pres')
            rs = None
            pres = None
            if rss:
                rs = _toString(rss[-1])
            elif press:
                pres = press[-1].toxml()
            return (prodClass, rs, pres)
        finally:
            if dom != None:
                dom.unlink()
        return

    def _loadProductFile(self, fname):
        f = None
        fn2 = nethandler.requestNetAssetExt(fname)
        #print("Loading Product:", os.path.basename(fname))
        if fn2 is None:
            fn2 = fname
        try:
            f = open(fn2)
            doc = f.read()
            return self._parseProductDoc(doc)
        finally:
            if f != None:
                f.close()
        return


def _toString(node):
    s = ''
    for child in node.childNodes:
        if child.nodeType == node.CDATA_SECTION_NODE:
            xml = child.toxml()
            cdtag = '<![CDATA['
            p1 = xml.find(cdtag) + len(cdtag)
            p2 = xml.find(']]>')
            s += xml[p1:p2]
        else:
            s += child.toxml()

    return s
    return

import functools, nethandler
implid = 0

from patches import filterfixer9000

def _processImpls(impls):
    global implid
    if len(impls) == 0:
        return Product
    impl = impls[-1]
    py = _toString(impl)
    ns = twc.buildPyNamespace()
    ns["reduce"] = reduce
    ns["functools"] = functools
    ns["filterfixer9000"] = filterfixer9000
    code = loadtools.fixsort(py).replace("os.access", "newaccess").replace("os.stat", "newstat").replace("os.path.exists", "newexists").replace("filter", "filterfixer9000").replace("os.path.join", "newjoin").replace("    \t", "        ").replace("\t", "        ")
    implid += 1
    exec(code, ns, ns)
    prodClass = ns['Product']
    return prodClass
    return


