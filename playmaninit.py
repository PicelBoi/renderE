import rendereglobals as rg
import os
import twc
if twc.personality == "WxScan":
    import wxscanpy.plugin.playman.playCmd.local as pmlc
    import wxscanpy.plugin.playman.playCmd.pm as pm
    import wxscanpy.plugin.playman.playCmd.ldl as pmldl
    import wxscanpy.plugin.playman.playCmd.bulletin as pmbl
    import wxscanpy.plugin.playman.playCmd.rsload as pmrs
    import wxscanpy.plugin.playman.playCmd.backgroundMusic as pmbgm
else:
    import domesticpy.plugin.playman.playCmd.local as pmlc
    import domesticpy.plugin.playman.playCmd.pm as pm
    import domesticpy.plugin.playman.playCmd.ldl as pmldl
    import domesticpy.plugin.playman.playCmd.bulletin as pmbl
import twccommon.embedded

twccommon.embedded.runconfpy(os.path.join(os.path.dirname(__file__), "wxscanpy" if twc.personality == "WxScan" else "domesticpy", "conf", "playman.py"))

rg.configs["playman"].productRoot = "net/usr/twc/wxscan/products"
rg.configs["playman"].tempDir = "temp"
pm.init(rg.configs["playman"])
pmlc.init(rg.configs["playman"])
pmldl.init(rg.configs["playman"])
pmbl.init(rg.configs["playman"])
if twc.personality == "WxScan":
    pmrs.init(rg.configs["playman"])
    pmbgm.init(rg.configs["playman"])

