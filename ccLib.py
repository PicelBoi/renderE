import twc
import twc.DataStoreInterface as ds
import twc.dsmarshal as dsm
import twccommon
import twcWx.dataUtil as wxDataUtil

class CCLib(twc.products.Product):

    def _loadData(self):
        # load any data necessary; this method not invoked if not _active()
        params = self.getParams()

        # if we don't find a loc name later, we'll use the first one
        # in the list to display in the header
        try:
            locName = params.locName[0]
        except:
            locName = None

        try:
            obsStations = params.obsStation
        except:
            obsStations = None

        try:
            locNames = params.locName
        except:
            locNames = None

        # default obs and uv objects to None
        obs = None
        uv = None

        if ((obsStations != None) and (locNames != None)):
            # determine which obs station has data and use that one
            for stn, lname in zip(obsStations, locNames):

                obs = dsm.defaultedGet('obs.%s' % (stn, ))
                if obs != None:
                    obs = twccommon.DefaultedData(obs)
                    # load the wxDataUtil in the PlayManager space instead of the renderd space
                    if obs.skyCondition != None:
                        skyCond = wxDataUtil.formatSkyCondition(obs.skyCondition, "CcObservation", "INVALID")
                        if skyCond != "INVALID":
                            obs.iconFile = skyCond.iconFile
                            obs.textModifier = skyCond.textModifier
                        else:
                            obs.skyCondition = None

                    if obs.skyCondition == None and obs.temp == None:
                        obs = None
                    else:
                        locName = lname
                        uv = dsm.defaultedGet('uv.%s' % (stn, ))
                        if uv != None:
                            uv = twccommon.DefaultedData(uv)
                        break

        # add whatever we got for obs to the internal object
        self.updateData(locName=locName, obs=obs, uv=uv)
