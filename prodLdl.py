
import os
import twc
import twc.products
import twccommon
import domestic.dataUtil as dataUtil
import twcWx.dataUtil as wxDataUtil
import twc.dsmarshal as dsm
from functools import reduce

class Observation(twc.products.Product):

    def _getDefaultedObs(self,loc):
        obs = dsm.defaultedGet("obs.%s" % loc)
        if obs == None:
            return None
            
        obx = twccommon.DefaultedData(obs)    
        if twc.personality == "FlatRock":
            skyCond = wxDataUtil.formatSkyCondition(
                obx.skyCondition, 'Observation')
            obx.skyIcon = twc.findRsrc(
                '/icons/tiny/%s' % skyCond.iconFile, "mv")
            obx.skyText = skyCond.textModifier
            
        return obx

    def _loadData(self):
        data = self.getData()
        data.bulletins = []
        params = self.getParams()
        obsl = []
        for stn in params.obsStation:
            obs = self._getDefaultedObs(stn)
            if obs != None:
                if obs.temp == None and obs.skyCondition == None:
                    obs = None
            obsl.append(obs)

        data.obs = obsl
        self._hasData = (reduce(lambda a, b: a or b, obsl) != None)
        

