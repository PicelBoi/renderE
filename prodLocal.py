
import os
import twc
import twc.products
import twccommon
import domestic.dataUtil as dataUtil
import twcWx.dataUtil as wxDataUtil
import twc.dsmarshal as dsm
from functools import reduce
import rendereglobals as rg

class AnimatedMap(twc.products.Product):
    """This class supports maps that "animate" (i.e. - support multiple data
       layer images that 'move' over the map). Although this class still
       works (and is still used) for maps that only have one data image to
       display -- you just won't see any 'movement'"""

    def __init__(self, params):
        twc.products.Product.__init__(self, params)

        # set the max number of images that can be missing before the
        # animation loop is cancelled (-1 = unlimited)
        self._maxAllowedImageGap = -1  # image file count

        # for DEBUGGING, show any image files present regardless of
        # expiration time (set to 1 to debug)
        self._ignoreImageExpiration = 0

        # for DEBUGGING, show any image files present regardless of
        # any gaps in the image animation (set to 1 to debug)
        self._ignoreTimeGaps        = 0

        # set image root
        imageRoot = os.environ["RENDEREROOT"]
        if twc.personality == "WxScan":
            prodString = 'Config.%s.%s.%s.%s.%s' % (dsm.getConfigVersion(),
                params.package, params.packageInst, params.product,
                params.productInst)

            # get all additional info about the map cut (especially the datacut type
            # and geographic location)
            mapDataString = prodString + '.MapData'
            mapCutData    = dsm.defaultedGet(mapDataString)

            dataCutType = mapCutData.datacutType
            dataCutInfo = dataCutType.split('.')

            self.updateData(
                productString = prodString,

                # figure out the data type so we know what directory to look in
                imageRoot = imageRoot + '/%s/%s.cuts/' % (dataCutInfo[0], dataCutInfo[1]),

                mapLocation = dataCutInfo[1], # us, pr, ak, hi, etc

                # list of data images to display
                imageList = [],

                # image parameters (-1 = undefined)
                imageFrequency = -1, # in seconds
                maxImages      = -1, # image file count

                # display "timing" for each image: show image for 'x' frames
                # (-1 = undefined)
                imageDuration      = -1,  # in frames
                lastImageDuration  = -1)  # in frames (frame count)
        else:
            self.updateData(
                    # here's the MOST important thing we set in here -- we need this
                    # productString for "everything" in the map world. We use it to
                    # locate map cuts, data images (if any), config entries, etc
                    productString = 'Config.%s.%s' % (dsm.getConfigVersion(), self.getName(),),

                    # set the base image root, each product will append its own 
                    # product-specific sub-dir
                    imageRoot=imageRoot,

                    # list of data images to display (we'll figure this out in the product)
                    imageList = [],

                    # image parameters (-1 = undefined until the product defines them)
                    imageFrequency = -1, # in seconds
                    maxImages      = -1, # image file count

                    # display "timing" for each image: show image for 'x' frames
                    # (-1 = undefined until the product defines them)
                    imageDuration      = -1,  # in frames
                    lastImageDuration  = -1)  # in frames (frame count)


    def _loadData(self): 
        params = twccommon.DefaultedData(self.getParams())
        data   = self.getData()

        # Assume there is no data (until we see that there is)
        data.noDataAvailable = 1
        # this is the DEFAULT no data available text; the product CAN
        # override this to display something else
        data.noDataAvailableText = "Temporarily Unavailable"

        # check for a map cut
        mapCut = rg.newjoin(os.environ["TWCPERSDIR"], "data", "map.cuts", '%s.map.tif' % (data.productString,))

        # if there's no map cut, we're not valid (regardless if there's data)
        if os.path.exists(mapCut) == 0:
            print(data.productString, mapCut)
            twccommon.Log.warning("no map cut found for %s. Can't display product." % (data.productString,))
            data.noDataAvailable = 1
            return

        # see if we have any data (TODO: fix ignoreImageExpiration someday for debugging):
        if twc.personality == "WxScan":
            data.imageList = dataUtil.getValidFileList(dataPath=data.imageRoot,
                                                    prefix=data.productString,
                                                    suffix='*[0-9].tif',
                                                    startTimeNdx=6, endTimeNdx=7, sortIndex=6)
        else:
            data.imageList = dataUtil.getValidFileList(dataPath=data.imageDir,
                                                    prefix=data.productString,
                                                    suffix='*[0-9].tif',
                                                    startTimeNdx=3, endTimeNdx=4, sortIndex=3)

        # IF we need to check for gaps AND we found valid images
        if (self._maxAllowedImageGap >= 0) and (len(data.imageList) > 0):
            # make sure there aren't any time gaps!
            # this needs to be the list of ALL valid images because this
            # function will clean up this product's valid images if there
            # is a time gap in the loop (per the reqs).
            data.imageList = dataUtil.checkImageListForGaps(
                self.getName(), data.imageList, data.imageFrequency,
                self._maxAllowedImageGap, self._ignoreTimeGaps)

        # per the requirements, restrict the time period to MAX_IMAGES
        data.imageList = data.imageList[0:data.maxImages]

        # If we still have images after checking for gaps....
        if len(data.imageList) > 0:
            # then,  clear the noDataAvailable flag because we've got data
            data.noDataAvailable = 0
        else:
            twccommon.Log.warning("no valid images found for %s. No data to display." % (data.productString,))

        # SORT oldest to newest
        # IMPORTANT: reversing must be the LAST step:
        # 1st we sort from newest to oldest (above - getImageFileList)
        # then we trim to the most recent images using a slice (above)
        # now we can safely reverse it to the required display order of
        # oldest to newest
        data.imageList.reverse()

        # Update data with params map data which does not need resolving
        data.vector = params.vector
        data.textString = params.textString
        data.tiffImage = params.tiffImage
        data.labeledTiffImage = params.labeledTiffImage


class ObservationMap(twc.products.Product):

    def __init__(self, params):
        twc.products.Product.__init__(self, params)

        self.updateData(
            # here's the MOST important thing we set in here -- we need this
            # productString for "everything" in the map world. We use it to
            # locate map cuts, data images (if any), config entries, etc
            productString = 'Config.%s.%s' % (dsm.getConfigVersion(), self.getName())
        )


    def _getObservationData(self, obsStation, dataType):
        # if we haven't heard of it or there's a datastore problem,
        # return None
        value = None

        # key = obs.{obsStation} i.e. - obs.KATL
        obsKey = 'obs.%s' % (obsStation,)
        observation = dsm.defaultedGet(obsKey, None)

        if observation is not None:
            observation = twccommon.DefaultedData(observation)

            # TODO: add ALL other types to be supported
            if dataType == 'temp':
                value = observation.temp
            elif dataType == 'skyCondition':
                value = wxDataUtil.formatSkyCondition(observation.skyCondition,\
                               'Observation', 0)
                               
                if value == 0:
                    value = None
                else:
                    value = value.iconFile
                
        return value


    def _loadData(self): 
        params = twccommon.DefaultedData(self.getParams())
        data = self.getData()

        data.noDataAvailable = 0
        # this is the DEFAULT no data available text; the product CAN
        # override this to display something else
        data.noDataAvailableText = "No Report"

        # check for a map cut
        mapCut = rg.newjoin(os.environ["TWCPERSDIR"], "data", "map.cuts", '%s.map.tif' % (data.productString,))

        # if there's no map cut, we're not valid (regardless if there's data)
        if os.path.exists(mapCut) == 0:
            print(data.productString, mapCut)
            twccommon.Log.warning("no map cut found for %s. Can't display product." % (data.productString,))
            data.noDataAvailable = 1
            return
 
        try:
            # lookup any obsIcon and obsValue data
            maxDataCount     = 0
            missingDataCount = 0

            # obsValue
            obsValues = []

            # If params has a obsValue field (obsValue != None)
            # and it is not empty (obsValue != [])
            if (params.obsValue):

                for properties,elements in params.obsValue:

                    # what data value are we looking for in the Ob?
                    dataType = properties[5]

                    updatedElements = []
                    dataCount       = 0
                    for item in elements:
                        obsStation = item[0]
                        position   = item[1]

                        # getObsData
                        value = self._getObservationData(obsStation, dataType)
                        if value == None:
                            missingDataCount += 1
                        updatedElements.append((value,position))
 
                    maxDataCount += len(elements)
                    obsValues.append((properties, tuple(updatedElements)))

            data.obsValue = obsValues

            # obsIcon
            obsIcons = []

            # If params has a obsIcon field (obsIcon != None)
            # and it is not empty (obsIcon != [])
            if (params.obsIcon):

                for properties,elements in params.obsIcon:

                    # icons don't have properties, skip to elements
                    updatedElements = []
                    for item in elements:
                        obsStation = item[0]
                        position   = item[1]

                        # getObsData
                        iconFile = self._getObservationData(obsStation, 'skyCondition')
                        if iconFile == None:
                            missingDataCount += 1
                        updatedElements.append((iconFile,position))

                    maxDataCount += len(elements)
                    obsIcons.append((properties, tuple(updatedElements)))

            data.obsIcon = obsIcons
            twccommon.Log.warning('MISSING %s, MAX, %s' % (missingDataCount, maxDataCount))
            # check for no data available
            if missingDataCount == maxDataCount:
                data.noDataAvailable = 1

        except:
            twccommon.Log.logCurrentException("ObservationMap loadData error:")
            data.noDataAvailable = 1

        # Update data with params map data which does not need resolving
        data.vector = params.vector
        data.tiffImage = params.tiffImage
        data.labeledTiffImage = params.labeledTiffImage
        data.textString = params.textString


class ForecastMap(twc.products.Product):

    def __init__(self, params):
        twc.products.Product.__init__(self, params)

        self.updateData(
            # here's the MOST important thing we set in here -- we need this
            # productString for "everything" in the map world. We use it to
            # locate map cuts, data images (if any), config entries, etc
            productString = 'Config.%s.%s' % (dsm.getConfigVersion(), self.getName())
        )


    def _getDailyForecastData(self, coopId, timePeriod, recType, dataType=None):
        if dataType is None:
            return self._getDailyForecastDataWxs(coopId, timePeriod, recType)
        value = None
        
        # key = {recType}.{coopId}.{time_period}.{dataType}
        # i.e. - dailyFcst.7219000.1060719026.daySkyCondition
        fcstKey  = '%s.%s.%d.%s' % (recType, coopId, timePeriod, dataType)
        fcstData = dsm.defaultedGet(fcstKey)

        if fcstData is not None:
            value = fcstData

            # If we need to convert the value to an icon filename
            if ((dataType == 'skyCondition') or
                (dataType == 'daySkyCondition') or
                (dataType == 'eveningSkyCondition')):
                    # We don't care about the text modifier so just use the 'Forecast' plugin
                    value = wxDataUtil.formatSkyCondition(int(fcstData), 'Forecast').iconFile

        return value

    def _getDailyForecastDataWxs(self, coopId, timePeriod, dataType):
        value = None

        # key = dailyFcst.{coopId}.time_period
        # i.e. - dailyFcst.7219000.1060719026
        fcstKey  = 'dailyFcst.%s.%d' % (coopId,timePeriod,)
        fcstData = dsm.defaultedGet(fcstKey)

        if fcstData is not None:
            fcstData = twccommon.DefaultedData(fcstData)

            # TODO: add all other types to be supported
            if dataType == 'highTemp':
                value = fcstData.highTemp
            elif dataType == 'lowTemp':
                value = fcstData.lowTemp
            elif dataType == 'daySkyCondition':
                value = wxDataUtil.formatSkyCondition(
                fcstData.daySkyCondition, 'Forecast').iconFile
            elif dataType == 'eveningSkyCondition':
                value = wxDataUtil.formatSkyCondition(
                fcstData.eveningSkyCondition, 'Forecast').iconFile
            elif dataType == 'golfIndex':
                value = fcstData.golfIndex

        return value

        
    def _loadDataTimePeriod(self, timePeriod, recType=None, valueField=None, iconField=None):
        if recType is None and valueField is None and iconField is None:
            return self._loadDataTimePeriodWxs(timePeriod)
        params = twccommon.DefaultedData(self.getParams())
        # we can't fill in the 'data' member variable here like the
        # other _loadData() methods since products like
        # RegionalForecastConditions call this function several
        # times with different time periods. Each call would
        # would overwrite 'data' each time. SO we used 'timePeriodData'.
        timePeriodData = twccommon.Data()
        # assume no data (until we see some)
        timePeriodData.noDataAvailable = 1

        # fcstValue
        fdata = []
        validValueList = []
        # If params has a fcstValue field (fcstValue != None)
        # and it is not empty (fcstValue != [])
        if (params.fcstValue):
            for properties,elements in params.fcstValue:
                # what data value are we looking for in the Fcst?
                # If the product doesn't override it, use the value in properties[5]
                if (valueField == None) and (len(properties) > 5):
                    valueField = properties[5]

                updatedElements = []
                for item in elements:
                    station  = item[0]
                    position = item[1]

                    # getFcstData
                    value = self._getDailyForecastData(station, timePeriod, recType, valueField)
                    # Note: zero is a valid temp, so check for None
                    validValueList.append(value != None) # Update a flag for each element
                    updatedElements.append((value, position))

                fdata.append((properties, tuple(updatedElements)))

        timePeriodData.fcstValue = fdata

        # fcstIcon
        idata = []
        validIconList = []
        # If params has a fcstIcon field (fcstIcon != None)
        # and it is not empty (fcstIcon != [])
        if (params.fcstIcon):
            for properties,elements in params.fcstIcon:
                # icons don't have properties, skip to elements
                updatedElements = []
                for item in elements:
                    station  = item[0]
                    position = item[1]

                    # getFcstData
                    iconFile = self._getDailyForecastData(station, timePeriod, recType, iconField)
                    validIconList.append((iconFile != None) and (iconFile != 'BlankIcon')) # Update a flag for each element
                    updatedElements.append((iconFile, position))

                idata.append((properties, tuple(updatedElements)))

        timePeriodData.fcstIcon = idata

        # Now create a list defining if the data is valid for each location
        # This list can be used to avoid displaying the city name if the data isn't valid.
        # The current rule is the location is valid if any part (temp, icon, ...) is valid
        if (validValueList and validIconList):
            timePeriodData.validLocList = list(map((lambda a,b: a or b), validValueList, validIconList))
        elif (validValueList):
            timePeriodData.validLocList = validValueList
        elif (validIconList):
            timePeriodData.validLocList = validIconList
        else:
            timePeriodData.validLocList = None

        # Now combine the valid flag for all locations into a single value.
        # If any location is valid, then clear the noDataAvailable flag.
        if (timePeriodData.validLocList) and ( reduce(lambda a, b: a or b, timePeriodData.validLocList, 0) ):
            timePeriodData.noDataAvailable = 0
        else:
            timePeriodData.noDataAvailable = 1

        # Update retVal with params map data which does not need resolving
        timePeriodData.vector = params.vector
        timePeriodData.tiffImage = params.tiffImage
        timePeriodData.labeledTiffImage = params.labeledTiffImage
        timePeriodData.textString = params.textString

        return timePeriodData

    def _loadDataTimePeriodWxs(self, timePeriod):
        params = twccommon.DefaultedData(self.getParams())
        # we can't fill in the 'data' member variable here like the
        # other _loadData() methods since products like
        # RegionalForecastConditions call this function several
        # times with different time periods. Each call would
        # would overwrite 'data' each time. SO we used 'timePeriodData'.
        timePeriodData = twccommon.Data()
        # assume no data (until we see some)
        timePeriodData.noDataAvailable = 1

        # fcstValue
        fdata = []
        validValueList = []
        # If params has a fcstValue field (fcstValue != None)
        # and it is not empty (fcstValue != [])
        if (params.fcstValue):
            for properties,elements in params.fcstValue:
                # what data value are we looking for in the Fcst?
                dataType = properties[5]

                updatedElements = []
                for item in elements:
                    station = item[0]
                    position   = item[1]

                    # getFcstData
                    value = self._getDailyForecastData(station, timePeriod, dataType)
                    # Note: zero is a valid temp, so check for None
                    validValueList.append(value != None) # Update a flag for each element
                    updatedElements.append((value,position))

                fdata.append((properties, tuple(updatedElements)))

            timePeriodData.fcstValue = fdata

            # fcstIcon
            idata = []
            validIconList = []
            # If params has a fcstIcon field (fcstIcon != None)
            # and it is not empty (fcstIcon != [])
            if (params.fcstIcon):
                for properties,elements in params.fcstIcon:
                    # icons don't have properties, skip to elements
                    updatedElements = []
                    for item in elements:
                        station = item[0]
                        position   = item[1]

                        # getFcstData
                        iconFile = self._getDailyForecastData(station, timePeriod, 'daySkyCondition')
                        validIconList.append(iconFile != None) # Update a flag for each element
                        updatedElements.append((iconFile,position))

                    idata.append((properties, tuple(updatedElements)))

                timePeriodData.fcstIcon = idata

            # Now create a list defining if the data is valid for each location
            # This list can be used to avoid displaying the city name if the data isn't valid.
            # The current rule is the location is valid if any part (temp, icon, ...) is valid
            timePeriodData.validLocList = list(map((lambda a,b: a or b), validValueList, validIconList))

            # Now combine the valid flag for all locations into a single value.
            # If any location is valid, then clear the noDataAvailable flag.
            if ( reduce(lambda a, b: a or b, timePeriodData.validLocList, 0) ):
                timePeriodData.noDataAvailable = 0
            else:
                timePeriodData.noDataAvailable = 1

        return timePeriodData
