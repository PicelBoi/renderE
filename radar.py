
import os
import twc
import twc.products
import twccommon
import domestic.dataUtil as dataUtil
import twcWx.dataUtil as wxDataUtil
import twc.dsmarshal as dsm
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
        data = self.getData()


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
        data.imageList = dataUtil.getValidFileList(dataPath=data.imageRoot,
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
