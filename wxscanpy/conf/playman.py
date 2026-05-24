
import os
import config
import twc.products
import twc.EventLog as EventLog
import wxscan
import wxscan.Properties
import twc.dsmarshal
dsm      = twc.dsmarshal

TWCDIR     = os.environ['TWCDIR']
TWCCLIDIR  = os.environ['TWCCLIDIR']
TWCPERSDIR = os.environ['TWCPERSDIR']


config.set('appName',              'playman')
config.set('channel',              'SystemEventChannel')
config.set('pluginRoot',           TWCPERSDIR + '/plugin')
config.set('resourceRoot',         '/rsrc')
config.set('pidFileName',          TWCPERSDIR + '/data/pid')

config.set('tempDir',              TWCPERSDIR + '/data/volatile/tmp')
config.set('productRoot',          TWCPERSDIR + '/products')
config.set('productPluginRoot',    TWCPERSDIR + '/plugin/playman/products')
config.set('packagePluginRoot',    TWCPERSDIR + '/plugin/playman/packages')
config.set('csAudioLog',           'temp/csaudiolog')
config.set('runlog',               'temp/runlog')
config.set('datalog',              'temp/datalog')
config.set('datalogDebug',         1)
config.set('mediaRoot',            '/media')


#Set Config Version Here
configVersion = "1"


### Package/Product Defaults
d = twc.Data()
d.backgroundImage = 'wxscan_video_bg'
dsm.setDefault('Config.' + configVersion + '.LocalBroadcaster.Background_Default', d)

d = twc.Data()
d.backgroundImage = 'wxscan_default_bg'
d.affiliateLogo = 'blankLogo'
d.transitionIn = 'FadeIn'
d.transitionOut = 'FadeOut'
dsm.setDefault('Config.' + configVersion + '.default', d)

dsm.setDefault('SevereMode', 0)
dsm.setDefault('Clock', 'default.clock')
dsm.setDefault('SevereClock', 'default_severe.clock')

# Severe Mode PILs
d = ['TOR','FFW','SVR','SVS','HHH']
dsm.setDefault('Config.' + configVersion + '.severeMode.pilList', d)

d = twc.Data()
d.ellipseRGBA = ((132, 169, 214, 102), (74, 122, 229, 166), (132, 169, 214, 145), (74, 122, 229, 115))
d.arcRGBA = (95, 128, 182, 230)
d.bkgImage = 'airport_intro_bg'
dsm.setDefault('Config.' + configVersion + '.Airport.Local_PackageIntro', d)

d = twc.Data()
d.bkgImage = 'airport_bg'
d.packageTitle = 'Airport Conditions'
d.shortPackageTitle = 'Airport Conditions'
d.titlePointerColor = (132, 169, 214, 255)
dsm.setDefault('Config.' + configVersion + '.Airport', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
d.locId = []
d.locIdCoordinate = []
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.BoatAndBeach.Local_CurrentWaterTemperatures', d)

d = twc.Data()
d.ellipseRGBA = ((10, 140, 10, 69), (205, 255, 84, 166), (10, 140, 10, 199), (10, 90, 10, 189))
d.arcRGBA = (10, 140, 10, 230)
d.bkgImage = 'boatbeach_intro_bg'
dsm.setDefault('Config.' + configVersion + '.BoatAndBeach.Local_PackageIntro', d)

d = twc.Data()
d.bkgImage = 'boatbeach_bg'
d.packageTitle = 'Boat & Beach'
d.shortPackageTitle = 'Boat & Beach'
d.titlePointerColor = (65, 178, 10, 255)
dsm.setDefault('Config.' + configVersion + '.BoatAndBeach', d)

d = twc.Data()
d.titlePointerColor = (255, 212, 14, 255)
d.highlightColor = (80, 140, 255, 255)
d.bkgColor = (42, 89, 229, 205)
d.periodColor = (40, 40, 115, 255)
d.bkgImage = 'core_bg'
d.packageTitle = 'Your Local Forecast'
d.shortPackageTitle = 'Your Local Forecast'
dsm.setDefault('Config.' + configVersion + '.Core1', d)
dsm.setDefault('Config.' + configVersion + '.LocalBroadcaster', d)

d = twc.Data()
d.titlePointerColor = (255, 212, 14, 255)
d.highlightColor = (80, 140, 255, 255)
d.bkgColor = (42, 89, 229, 205)
d.periodColor = (40, 40, 115, 255)
d.bkgImage = 'core_bg'
d.packageTitle = 'Your Local Radar'
d.shortPackageTitle = 'Your Local Radar'
dsm.setDefault('Config.' + configVersion + '.Core5', d)

d = twc.Data()
d.titlePointerColor = (255, 212, 14, 255)
d.highlightColor = (80, 140, 255, 255)
d.bkgColor = (42, 89, 229, 205)
d.periodColor = (40, 40, 115, 255)
d.bkgImage = 'core_bg'
d.packageTitle = 'Your Local Forecast'
d.shortPackageTitle = 'Your Local Forecast'
dsm.setDefault('Config.' + configVersion + '.Core2', d)

d = twc.Data()
d.titlePointerColor = (255, 212, 14, 255)
d.highlightColor = (80, 140, 255, 255)
d.shortPackageTitle = 'Forecast en Espa\xf1ol'
d.bkgColor = (42, 89, 229, 205)
d.periodColor = (40, 40, 115, 255)
d.bkgImage = 'core_bg'
d.packageTitle = 'Forecast en Espa\xf1ol'
dsm.setDefault('Config.' + configVersion + '.Core2Spanish', d)

d = twc.Data()
d.titlePointerColor = (255, 212, 14, 255)
d.highlightColor = (80, 140, 255, 255)
d.bkgColor = (42, 89, 229, 205)
d.periodColor = (40, 40, 115, 255)
d.bkgImage = 'core_bg'
d.packageTitle = 'Your Local Forecast'
d.shortPackageTitle = 'Your Local Forecast'
dsm.setDefault('Config.' + configVersion + '.Core3', d)

d = twc.Data()
d.titlePointerColor = (255, 212, 14, 255)
d.highlightColor = (80, 140, 255, 255)
d.bkgColor = (42, 89, 229, 205)
d.periodColor = (40, 40, 115, 255)
d.bkgImage = 'core_bg'
d.packageTitle = 'Your Local Forecast'
d.shortPackageTitle = 'Your Local Forecast'
dsm.setDefault('Config.' + configVersion + '.Core4', d)

d = twc.Data()
d.titlePointerColor = (255, 212, 14, 255)
d.highlightColor = (80, 140, 255, 255)
d.shortPackageTitle = 'Forecast en Espa\xf1ol'
d.bkgColor = (42, 89, 229, 205)
d.periodColor = (40, 40, 115, 255)
d.bkgImage = 'core_bg'
d.packageTitle = 'Forecast en Espa\xf1ol'
dsm.setDefault('Config.' + configVersion + '.Core4Spanish', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.Garden.Local_EstimatedPrecipitation', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.Garden.Local_FrostFreezeWarnings', d)

d = twc.Data()
d.ellipseRGBA = ((10, 140, 10, 69), (205, 255, 84, 166), (10, 140, 10, 199), (10, 90, 10, 189))
d.arcRGBA = (10, 140, 10, 230)
d.bkgImage = 'garden_intro_bg'
dsm.setDefault('Config.' + configVersion + '.Garden.Local_PackageIntro', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.Garden.Local_PalmerDroughtSeverity', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.Garden.Local_PrecipitationQpfForecast', d)

d = twc.Data()
d.promoLogo = 'blankLogo'
d.promoImage = 'garden_promo'
d.promoText = ['For more information on weather', 
               'and  your  lawn  and  garden,', 
               'go to weather.com/garden.']
dsm.setDefault('Config.' + configVersion + '.Garden.Local_Promo', d)

d = twc.Data()
d.shortPackageTitle = 'Garden'
d.packageTitle = 'Garden'
d.bkgImage = 'garden_bg'
d.titlePointerColor = (65, 178, 10, 255)
dsm.setDefault('Config.' + configVersion + '.Garden', d)

d = twc.Data()
d.ellipseRGBA = ((10, 140, 10, 69), (205, 255, 84, 166), (10, 140, 10, 199), (10, 90, 10, 189))
d.arcRGBA = (10, 140, 10, 230)
d.bkgImage = 'golf_intro_bg'
#dsm.setDefault('Golf.Local_PackageIntro', d)
#XXX
dsm.setDefault('Config.' + configVersion + '.Golf.Local_PackageIntro', d)

d = twc.Data()
d.promoText = ['Check the forecast for any', 'golf course in the U.S.', 'at weather.com/golf']
d.promoImage = 'golf_promo'
d.promoLogo = 'blankLogo'
dsm.setDefault('Config.' + configVersion + '.Golf.Local_Promo', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
d.indexCoordinate = []
d.locCoordinate = []
d.locName = []
d.coopId = []
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.Golf.Local_RegionalGolfIndexForecast', d)

d = twc.Data()
d.shortPackageTitle = 'Golf Forecast'
d.packageTitle = 'Golf Forecast'
d.bkgImage = 'golf_bg'
d.titlePointerColor = (20,160,10,255)
dsm.setDefault('Config.' + configVersion + '.Golf', d)

d = twc.Data()
d.ellipseRGBA = ((10, 182, 193, 69), (74, 122, 229, 166), (10, 170, 180, 199), (10, 182, 193, 189))
d.arcRGBA = (10, 182, 193, 230)
d.bkgImage = 'health_intro_bg'
dsm.setDefault('Config.' + configVersion + '.Health.Local_PackageIntro', d)

d = twc.Data()
d.promoText = ['For more on weather and your health,', 'tune to The Weather Channel or go', 'to weather.com/health']
d.promoImage = 'health_promo'
d.promoLogo = 'blankLogo'
dsm.setDefault('Config.' + configVersion + '.Health.Local_Promo', d)

d = twc.Data()
d.titlePointerColor = (14, 212, 190, 255)
d.summerFlag = 0
dsm.setDefault('Config.' + configVersion + '.Health.Local_SunSafetyFacts', d)

d = twc.Data()
d.bkgImage = 'health_bg'
d.packageTitle = 'Weather & Your Health'
d.shortPackageTitle = 'Health'
d.titlePointerColor = (14, 212, 190, 255)
dsm.setDefault('Config.' + configVersion + '.Health', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.International.Local_InternationalForecast', d)

d = twc.Data()
d.ellipseRGBA = ((160, 160, 160, 102), (160, 160, 160, 166), (160, 160, 160, 145), (160, 160, 160, 115))
d.arcRGBA = (160, 160, 160, 230)
d.bkgImage = 'international_intro_bg'
dsm.setDefault('Config.' + configVersion + '.International.Local_PackageIntro', d)

d = twc.Data()
d.bkgImage = 'international_bg'
d.packageTitle = 'International Forecast'
d.shortPackageTitle = "Int'l Forecast"
d.titlePointerColor = (160, 160, 160, 255)
dsm.setDefault('Config.' + configVersion + '.International', d)

d = twc.Data()
d.text = []
d.upNextDuration = 4
dsm.setDefault('Config.' + configVersion + '.LASCrawl', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
# don't assume we'll have cities or roads defined
d.locName = []
d.locCoordinate = []
d.dotCoordinate = []
d.roadSignData = []
d.roadSignCoordinate = []
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.Local_LocalDoppler', d)
dsm.setDefault('Config.' + configVersion + '.Local_LocalDopplerSpanish', d)

d = twc.Data()
d.bkgImage = 'city_bg'
dsm.setDefault('Config.' + configVersion + '.Local_MenuBoard', d)

d = twc.Data()
d.bkgImage = 'city_bg'
dsm.setDefault('Config.' + configVersion + '.Local_NetworkIntro', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.Local_RadarSatelliteComposite', d)
dsm.setDefault('Config.' + configVersion + '.Local_RadarSatelliteCompositeSpanish', d)

d = twccommon.Data()
d.title = 'Traffic Flow'
d.activeVocalCue = 1
dsm.setDefault('Config.' + configVersion + '.Local_TrafficFlow', d)

d = twc.Data()
d.packageTitle = 'Traffic Overview'
d.titlePointerColor = (222, 147, 42, 255)
dsm.setDefault('Config.' + configVersion + '.Local_TrafficOverview', d)

d = twc.Data()
d.bkgImage = 'severe_map_banner_bg'
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.SevereCore1A.Local_LocalDoppler', d)
dsm.setDefault('Config.' + configVersion + '.SevereCore1B.Local_LocalDoppler', d)
dsm.setDefault('Config.' + configVersion + '.SevereCore1A.Local_RadarSatelliteComposite', d)
dsm.setDefault('Config.' + configVersion + '.SevereCore2.Local_LocalDoppler', d)

d = twc.Data()
d.titlePointerColor = (190, 30, 20, 255)
d.highlightColor = (80, 80, 80, 255)
d.bkgColor = (178, 178, 178, 205)
d.periodColor = (40, 40, 40, 255)
d.bkgImage = 'severe_core_bg'
d.packageTitle = 'Your Local Forecast'
d.shortPackageTitle = 'Your Local Forecast'
dsm.setDefault('Config.' + configVersion + '.SevereCore1A', d)

d = twc.Data()
d.titlePointerColor = (190, 30, 20, 255)
d.highlightColor = (80, 80, 80, 255)
d.bkgColor = (178, 178, 178, 205)
d.periodColor = (40, 40, 40, 255)
d.bkgImage = 'severe_core_bg'
d.packageTitle = 'Your Local Forecast'
d.shortPackageTitle = 'Your Local Forecast'
dsm.setDefault('Config.' + configVersion + '.SevereCore1B', d)

d = twc.Data()
d.titlePointerColor = (190, 30, 20, 255)
d.highlightColor = (80, 80, 80, 255)
d.bkgColor = (178, 178, 178, 205)
d.periodColor = (40, 40, 40, 255)
d.bkgImage = 'severe_core_bg'
d.packageTitle = 'Your Local Forecast'
d.shortPackageTitle = 'Your Local Forecast'
dsm.setDefault('Config.' + configVersion + '.SevereCore2', d)

d = twc.Data()
d.ellipseRGBA = ((131, 59, 165, 102), (131, 59, 145, 166), (131, 59, 165, 145), (131, 59, 145, 115))
d.arcRGBA = (139, 91, 165, 230)
d.bkgImage = 'ski_intro_bg'
dsm.setDefault('Config.' + configVersion + '.Ski.Local_PackageIntro', d)

d = twc.Data()
d.displayTrailPercentage = [1, 1, 1]
dsm.setDefault('Config.' + configVersion + '.Ski.Local_SkiConditions', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.Ski.Local_SnowfallQpfForecast', d)

d = twc.Data()
d.titlePointerColor = (139, 97, 165, 255)
d.summerFlag = 0
dsm.setDefault('Config.' + configVersion + '.Ski.Local_SunSafetyFacts', d)

d = twc.Data()
d.bkgImage = 'ski_bg'
d.packageTitle = 'Ski & Snow'
d.shortPackageTitle = 'Ski & Snow'
d.titlePointerColor = (139, 97, 165, 255)
dsm.setDefault('Config.' + configVersion + '.Ski', d)

d = twc.Data()
d.ellipseRGBA = ((222,147,42, 102), (222,147,42,166), (163,109,35,145),(222,147,42,115))
d.arcRGBA = (222, 147, 42,  230)
d.bkgImage = 'traffic_intro_bg'
dsm.setDefault('Config.' + configVersion + '.Traffic.Local_PackageIntro', d)

d = twc.Data()
d.shortPackageTitle = 'Traffic Conditions'
d.packageTitle = 'Traffic Conditions'
d.bkgImage = 'traffic_bg'
d.packageFlavor=3
d.titlePointerColor = (222, 147, 42, 255)
dsm.setDefault('Config.' + configVersion + '.Traffic', d)

d = twc.Data()
d.minPageDuration = 10
d.title = 'Traffic Report'
dsm.setDefault('Config.' + configVersion + '.Traffic.Local_TrafficReport', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.Travel.Local_NationalTravelWeather', d)

d = twc.Data()
d.ellipseRGBA = ((132, 169, 214, 102), (74, 122, 229, 166), (132, 169, 214, 145), (74, 122, 229, 115))
d.arcRGBA = (95, 128, 182, 230)
d.bkgImage = 'travel_intro_bg'
dsm.setDefault('Config.' + configVersion + '.Travel.Local_PackageIntro', d)

d = twc.Data()
d.bkgImage = 'map_banner_bg'
d.coopId = []
d.locName = []
d.locCoordinate = []
d.iconCoordinate = []
d.tempCoordinate = []
d.vectors = []
dsm.setDefault('Config.' + configVersion + '.Travel.Local_RegionalForecastConditions', d)

d = twc.Data()
d.shortPackageTitle = 'Travel Forecast'
d.packageTitle = 'Travel Forecast'
d.bkgImage = 'travel_bg'
d.titlePointerColor = (132, 169, 214, 255)
dsm.setDefault('Config.' + configVersion + '.Travel', d)

d = twc.Data()
d.bkgImage = 'weather_bulletin_bg'
d.titlePointerColor = (190, 30, 20, 255)
dsm.setDefault('Config.' + configVersion + '.Local_WeatherBulletin', d)

d = twc.Data()
d.packageTitle = ''
d.shortPackageTitle = ''
dsm.setDefault('Config.' + configVersion + '.NullPackage', d)


#
# Default Config for localAvail script that runs from cron
d = twc.Data()
d.preRoll = 8
d.schedule = ((14,60), (29,60), (44,60), (58,120), )
dsm.setDefault('Config.' + configVersion + '.Local_Avail_Schedule', d)

# City Ticker Products
# 
d = twc.Data()
d.playlist = ['_LocalCitiesCurrentConditions.rs',
              '_TravelCitiesCurrentConditions.rs',
              '_LocalCitiesForecast.rs',
              '_TravelCitiesForecast.rs',
              '_AirportDelays.rs']
d.step = 3  # crawl rate of the marquis in pixels/frame
dsm.setDefault('Config.' + configVersion + '.CityTicker', d)

### viewport config
xshift = 60.0
yshift = 68.0
mw = 720 - (2*xshift)
localw = 432
LSF = localw/mw
RSF = 224.0/300.0
d = [
# Fields are   lname, depth, repeat, x, y, w, h, sx, sy, tx, ty
    (wxscan.Properties.MUSIC_LAYER_NAME,       15, 0,   0,   0, 1, 1, 1, 1, 0, 0),
    #(wxscan.Properties.AUDIO_LAYER_NAME,       25, 0,   0,   0, 1, 1, 1, 1, 0, 0),
    (wxscan.Properties.SMLOCAL_LAYER_NAME, 20, 0, 236, 186, 484, 249, 1, 1, 0, 0),
    (wxscan.Properties.BKGVIDEO_LAYER_NAME,    7, 0,   0,   0, 720, 480, 1, 1, 0, 0),
    ('Background',  10, 0,   0,   0, 720, 480, 1, 1, 0, 0),
    ('Foreground',  90, 0,   0,   0, 720, 480, 1, 1, 0, 0),

    ('Cc',          20, 0,   0,  80, 224, 274, 1, 1, 0, 0),
    ('Radar',       20, 0,   0,  79, 224, 118, 1, 1, -12, -12),
    ('ticker',      20, 1, 224,  61, 496,  19, 1, 1, 0, 0),
    (wxscan.Properties.LASCRAWL_LAYER_NAME,    20, 0, 224,  36, 495,  25, 1, 1, 0, 0),
    (wxscan.Properties.BULLETIN_LAYER_NAME,    30, 1, 224,  36, 496,  44, 1, 1, 0, 0),
    ('Fcst',        20, 0, 236,  88, 483, 90, 1, 1, 0, 0),
    ('Local',       20, 0, 238, 188, localw, 229, LSF, LSF, -xshift, -yshift),
    ('Menu',        20, 0, 238, 417, 481,  19, 1, 1, 0, 0),
]
dsm.setDefault('Config.' + configVersion + '.viewports', d)
#
# playlists config
#

#
#   Core1.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("NetworkIntro",0,10,10,10,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("CurrentConditions",0,12,12,12,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",0,8,8,8,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",1,8,8,8,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalDoppler",0,16,16,16,0,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("TextForecast",0,42,42,42,0,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,14,14,14,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("Almanac",0,10,10,10,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Core1.A', d)
#
#   Core1.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("NetworkIntro",0,10,10,10,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("WeatherBulletin",0,8,8,8,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("CurrentConditions",0,12,12,12,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",0,8,8,8,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",1,8,8,8,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalDoppler",0,16,16,16,0,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("TextForecast",0,42,42,42,0,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,16,16,16,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Core1.B', d)
#
#   Core1.C
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("NetworkIntro",0,10,10,10,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("WeatherBulletin",0,14,14,14,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("CurrentConditions",0,10,10,10,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",0,7,7,7,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",1,7,7,7,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalDoppler",0,16,16,16,0,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("TextForecast",0,42,42,42,0,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,14,14,14,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Core1.C', d)
#
#   LocalBroadcaster.A
#
d = twc.Data()
d.loadHeuristic = "loadPriorityOneOnly_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("NetworkIntro",0,10,10,10,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("Movie",0,110,110,110,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("CurrentConditions",0,12,12,12,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",0,8,8,8,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",1,8,8,8,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalDoppler",0,16,16,16,0,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("TextForecast",0,42,42,42,0,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,14,14,14,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("Almanac",0,10,10,10,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.LocalBroadcaster.A', d)
#
#   LocalBroadcaster.B
#
d = twc.Data()
d.loadHeuristic = "loadPriorityOneOnly_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("NetworkIntro",0,10,10,10,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("Movie",0,110,110,110,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("WeatherBulletin",0,8,8,8,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("CurrentConditions",0,12,12,12,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",0,8,8,8,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",1,8,8,8,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalDoppler",0,16,16,16,0,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("TextForecast",0,42,42,42,0,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,16,16,16,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.LocalBroadcaster.B', d)
#
#  LocalBroadcasterCore1.C
#
d = twc.Data()
d.loadHeuristic = "loadPriorityOneOnly_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("NetworkIntro",0,10,10,10,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("Movie",0,110,110,110,1,1,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("WeatherBulletin",0,14,14,14,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("CurrentConditions",0,10,10,10,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",0,7,7,7,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalObservations",1,7,7,7,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("LocalDoppler",0,16,16,16,0,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("TextForecast",0,42,42,42,0,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,14,14,14,1,2,0,["bg1","fg1","short","twoMinNoText","crawl","menu1","radar1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.LocalBroadcaster.C', d)
#
#   Core2.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("CurrentConditions",0,14,14,14,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalDoppler",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecast",0,14,14,14,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,16,16,16,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core2.A', d)
#
#   Core2.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("CurrentConditions",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalDoppler",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecast",0,12,12,12,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,14,14,14,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core2.B', d)
#
#   Core2.C
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,14,14,14,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("CurrentConditions",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalDoppler",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecast",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core2.C', d)
#
#   Core3.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("CurrentConditions",0,12,12,12,1,1,0,["bg1","fg1","short","oneMinNoText","crawl","menu1","radar1"]),
    ("LocalDoppler",0,12,12,12,0,1,0,["bg1","fg1","short","oneMinNoText","crawl","menu1","radar1"]),
    ("TextForecast",0,36,36,36,1,1,0,["bg1","fg1","short","oneMinNoText","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core3.A', d)
#
#   Core3.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,5,5,5,1,1,0,["bg1","fg1","short","oneMinNoText","crawl","menu1","radar1"]),
    ("CurrentConditions",0,7,7,7,1,1,0,["bg1","fg1","short","oneMinNoText","crawl","menu1","radar1"]),
    ("LocalDoppler",0,12,12,12,0,1,0,["bg1","fg1","short","oneMinNoText","crawl","menu1","radar1"]),
    ("TextForecast",0,36,36,36,1,1,0,["bg1","fg1","short","oneMinNoText","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core3.B', d)
#
#   Core3.C
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,14,14,14,1,1,0,["bg1","fg1","short","oneMinNoText","crawl","menu1","radar1"]),
    ("CurrentConditions",0,10,10,10,1,1,0,["bg1","fg1","short","oneMinNoText","crawl","menu1","radar1"]),
    ("LocalDoppler",0,12,12,12,0,1,0,["bg1","fg1","short","oneMinNoText","crawl","menu1","radar1"]),
    ("TextForecast",0,24,24,24,1,1,0,["bg1","fg1","short","oneMinNoText","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core3.C', d)
#
#   Core4.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("CurrentConditions",0,14,14,14,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("RadarSatelliteComposite",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecast",0,14,14,14,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core4.A', d)
#
#   Core4.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("CurrentConditions",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("RadarSatelliteComposite",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecast",0,12,12,12,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,14,14,14,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core4.B', d)
#
#   Core4.C
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,11,11,11,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("CurrentConditions",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("RadarSatelliteComposite",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecast",0,11,11,11,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecast",0,12,12,12,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core4.C', d)
#
#   Core5.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("LocalDoppler",0,60,60,60,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core5.A', d)
#
#   Core2Spanish.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("CurrentConditionsSpanish",0,14,14,14,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalDopplerSpanish",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecastSpanish",0,14,14,14,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecastSpanish",0,16,16,16,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core2Spanish.A', d)
#
#   Core2Spanish.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("CurrentConditionsSpanish",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalDopplerSpanish",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecastSpanish",0,12,12,12,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecastSpanish",0,14,14,14,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core2Spanish.B', d)
#
#   Core2Spanish.C
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,14,14,14,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("CurrentConditionsSpanish",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalDopplerSpanish",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecastSpanish",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecastSpanish",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core2Spanish.C', d)
#
#   Core4Spanish.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("CurrentConditionsSpanish",0,14,14,14,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("RadarSatelliteCompositeSpanish",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecastSpanish",0,14,14,14,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecastSpanish",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core4Spanish.A', d)
#
#   Core4Spanish.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("CurrentConditionsSpanish",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("RadarSatelliteCompositeSpanish",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecastSpanish",0,12,12,12,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecastSpanish",0,14,14,14,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core4Spanish.B', d)
#
#   Core4Spanish.C
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,11,11,11,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("CurrentConditionsSpanish",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("RadarSatelliteCompositeSpanish",0,16,16,16,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("DaypartForecastSpanish",0,11,11,11,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("ExtendedForecastSpanish",0,12,12,12,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Core4Spanish.C', d)
#
#   Airport.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalAirportConditions",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalAirportConditions",1,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalAirportConditions",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalAirportConditions",3,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("NationalAirportConditions",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("NationalAirportConditions",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Airport.A', d)
#
#   Airport.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalAirportConditions",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalAirportConditions",1,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalAirportConditions",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("NationalAirportConditions",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("NationalAirportConditions",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("NationalAirportConditions",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Airport.B', d)
#
#   Airport.C
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalAirportConditions",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("LocalAirportConditions",1,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("NationalAirportConditions",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("NationalAirportConditions",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("NationalAirportConditions",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("NationalAirportConditions",3,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Airport.C', d)
#
#   BoatAndBeach.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SurfReport",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("CurrentWaterTemperatures",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("CoastalWatersForecast",0,30,30,30,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Tides",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.BoatAndBeach.A', d)
#
#   BoatAndBeach.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SurfReport",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("CoastalWatersForecast",0,30,30,30,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Tides",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Tides",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.BoatAndBeach.B', d)
#
#   Garden.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("GardeningForecast",0,12,12,12,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("EstimatedPrecipitation",0,12,12,12,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("PrecipitationQpfForecast",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("PalmerDroughtSeverity",0,12,12,12,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("FrostFreezeWarnings",0,12,12,12,1,1,1,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Promo",0,12,12,12,1,2,1,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Garden.A', d)
#
#   Garden.C
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("GardeningForecast",0,12,16,12,1,2,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("PrecipitationQpfForecast",0,8,12,8,1,2,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("PalmerDroughtSeverity",0,12,16,12,1,2,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("FrostFreezeWarnings",0,12,12,12,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Promo",0,12,12,12,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Garden.B', d)
#
#   Golf.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("TeeTimeForecast",0,12,12,12,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("RegionalGolfIndexForecast",0,12,12,12,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("GolfCourseForecast",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("GolfCourseForecast",1,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("GolfCourseForecast",2,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Promo",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault('Config.' + configVersion + '.Playlist.Golf.A', d)
#
#   Health.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("OutdoorActivityForecast",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("HealthForecast",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("AirQualityForecast",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("UltravioletIndex",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SunSafetyFacts",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SunSafetyFacts",1,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Promo",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Health.A', d)
#
#   Health.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("OutdoorActivityForecast",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("AllergyReport",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("HealthForecast",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("AirQualityForecast",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("UltravioletIndex",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SunSafetyFacts",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Promo",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Health.B', d)
#
#   Health.C
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("OutdoorActivityForecast",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("AllergyReport",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("HealthForecast",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("UltravioletIndex",0,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SunSafetyFacts",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SunSafetyFacts",1,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Promo",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Health.C', d)
#
#   Health.D
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("OutdoorActivityForecast",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("HealthForecast",0,12,12,12,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("UltravioletIndex",0,12,12,12,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SunSafetyFacts",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SunSafetyFacts",1,8,8,8,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Promo",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Health.D', d)
#
#   International.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",3,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",4,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",5,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.International.A', d)
#
#   International.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",3,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",4,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.International.B', d)
#
#   International.C
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",2,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",3,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.International.C', d)
#
#   International.D
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",1,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",2,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.International.D', d)
#
#   International.E
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",3,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",1,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.International.E', d)
#
#   International.F
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",3,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",4,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalDestinations",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.International.F', d)
#
#   International.G
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",3,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",4,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("InternationalForecast",5,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.International.G', d)
#
#   Null.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = [];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("Null",0,1,60,1,1,1,0,[]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.NullPackage.A', d)
#
#   Ski.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SkiConditions",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SkiConditions",1,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SkiConditions",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SkiConditions",3,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SnowfallQpfForecast",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("SunSafetyFacts",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Ski.A', d)
#
#   Traffic.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar", "SmLocal"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1","smNull"]),
    ("TrafficOverview.1",0,10,23,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1","smNull"]),
    ("TrafficOverview.2",0,10,23,9,1,2,0,["bg1","fg1","short","text","crawl","menu1","radar1","smNull"]),
    ("TrafficOverview.3",0,10,23,9,1,5,0,["bg1","fg1","short","text","crawl","menu1","radar1","smNull"]),
    ("TrafficReport.1",0,10,23,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1","smNull"]),
    ("TrafficReport.2",0,10,23,9,1,3,0,["bg1","fg1","short","text","crawl","menu1","radar1","smNull"]),
    ("TrafficReport.3",0,10,23,9,1,4,0,["bg1","fg1","short","text","crawl","menu1","radar1","smNull"]),
    ("TrafficFlow.1",0,10,23,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1","smNull"]),
    ("TrafficFlow.2",0,10,23,9,1,2,0,["bg1","fg1","short","text","crawl","menu1","radar1","smNull"]),
    ("TrafficSponsor",0,10,10,10,0,1,0,["bg1","fg1","short","text","crawl","menu1","radar1","smTrafficSponsor"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Traffic.A', d)
#
#   Travel.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu","Radar"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("PackageIntro",0,4,4,4,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("NationalTravelWeather",0,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("RegionalForecastConditions",0,18,18,18,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Destinations",0,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Destinations",1,10,10,10,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
    ("Destinations",2,9,9,9,1,1,0,["bg1","fg1","short","text","crawl","menu1","radar1"]),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.Travel.A', d)
#
#   SevereCore1A.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("SevereWeatherMessage",0,6,6,6,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("CurrentConditions",0,10,10,10,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("LocalObservations",0,7,7,7,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("LocalObservations",1,7,7,7,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("RadarSatelliteComposite",0,12,12,12,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("LocalDoppler",0,24,24,24,0,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("TextForecast",0,42,42,42,0,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("ExtendedForecast",0,12,12,12,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.SevereCore1A.A', d)
#
#   SevereCore1A.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,6,6,6,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("CurrentConditions",0,10,10,10,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("LocalObservations",0,7,7,7,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("LocalObservations",1,7,7,7,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("RadarSatelliteComposite",0,12,12,12,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("LocalDoppler",0,24,24,24,0,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("TextForecast",0,42,42,42,0,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
    ("ExtendedForecast",0,12,12,12,1,1,0,["bg1","fg1","long","twoMinNoText","crawl","menu1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.SevereCore1A.B', d)
#
#   SevereCore1B.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("SevereWeatherMessage",0,5,5,5,1,1,0,["bg1","fg1","long","text","crawl","menu1"]),
    ("CurrentConditions",0,8,8,8,1,1,0,["bg1","fg1","long","text","crawl","menu1"]),
    ("LocalDoppler",0,24,24,24,0,1,0,["bg1","fg1","long","text","crawl","menu1",]),
    ("DaypartForecast",0,11,11,11,0,1,0,["bg1","fg1","long","text","crawl","menu1"]),
    ("ExtendedForecast",0,12,12,12,1,1,0,["bg1","fg1","long","text","crawl","menu1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.SevereCore1B.A', d)
#
#   SevereCore1B.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,5,5,5,1,1,0,["bg1","fg1","long","text","crawl","menu1"]),
    ("CurrentConditions",0,8,8,8,1,1,0,["bg1","fg1","long","text","crawl","menu1"]),
    ("LocalDoppler",0,24,24,24,0,1,0,["bg1","fg1","long","text","crawl","menu1"]),
    ("DaypartForecast",0,11,11,11,0,1,0,["bg1","fg1","long","text","crawl","menu1"]),
    ("ExtendedForecast",0,12,12,12,1,1,0,["bg1","fg1","long","text","crawl","menu1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.SevereCore1B.B', d)
#
#   SevereCore2.A
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("SevereWeatherMessage",0,8,8,8,1,1,0,["bg1","fg1","long","text","crawl","menu1"]),
    ("LocalDoppler",0,52,52,52,0,1,0,["bg1","fg1","long","text","crawl","menu1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.SevereCore2.A', d)
#
#   SevereCore2.B
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Local"
d.childPrefixes = ["Background", "Foreground","Cc","Fcst","LasCrawl","Menu"];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("WeatherBulletin",0,8,8,8,1,1,0,["bg1","fg1","long","text","crawl","menu1"]),
    ("LocalDoppler",0,52,52,52,0,1,0,["bg1","fg1","long","text","crawl","menu1"]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.SevereCore2.B', d)
#
#
#
#
#
#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Background"
d.childPrefixes = [];
d.units = "percent"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("Default",0,100,100,100,1,1,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Background.bg1', d)
#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Foreground"
d.childPrefixes = [];
d.units = "percent"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("Null",0,100,100,100,1,1,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Foreground.fg1', d)
#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Cc"
d.childPrefixes = [];
d.units = "percent"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("ShortCurrentConditions",0,100,100,100,1,1,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Cc.short', d)
#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Cc"
d.childPrefixes = [];
d.units = "percent"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("LongCurrentConditions",0,100,100,100,1,1,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Cc.long', d)
#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriorityOneOnly_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Fcst"
d.childPrefixes = [];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("DaypartForecast",0,15,60,15,1,1,0,[]),
    ("TextForecast",0,30,60,30,1,1,0,[]),
    ("ExtendedForecast",0,15,60,15,1,1,0,[]),
    ("Unavailable",0,1,60,1,1,2,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Fcst.text', d)
#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriorityOneOnly_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Fcst"
d.childPrefixes = [];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("DaypartForecast",0,15,30,15,1,1,0,[]),
    ("ExtendedForecast",0,15,30,15,1,1,0,[]),
    ("DaypartForecast",0,15,30,15,1,1,0,[]),
    ("ExtendedForecast",0,15,30,15,1,1,0,[]),
    ("Unavailable",0,1,60,1,1,2,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Fcst.oneMinNoText', d)
#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriorityOneOnly_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Fcst"
d.childPrefixes = [];
d.units = "seconds"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("DaypartForecast",0,15,30,15,1,1,0,[]),
    ("ExtendedForecast",0,15,30,15,1,1,0,[]),
    ("DaypartForecast",0,15,30,15,1,1,0,[]),
    ("ExtendedForecast",0,15,30,15,1,1,0,[]),
    ("DaypartForecast",0,15,30,15,1,1,0,[]),
    ("ExtendedForecast",0,15,30,15,1,1,0,[]),
    ("DaypartForecast",0,15,30,15,1,1,0,[]),
    ("ExtendedForecast",0,15,30,15,1,1,0,[]),
    ("Unavailable",0,1,120,1,1,2,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Fcst.twoMinNoText', d)
#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "LasCrawl"
d.childPrefixes = [];
d.units = "percent"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("Default",0,100,100,100,1,1,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.LasCrawl.crawl', d)
#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Menu"
d.childPrefixes = [];
d.units = "percent"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("Default",0,100,100,100,1,1,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Menu.menu1', d)
#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriorityOneOnly_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Radar"
d.childPrefixes = [];
d.units = "percent"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("LocalDoppler",0,100,100,100,1,1,0,[]),
    ("Null",0,100,100,100,1,2,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Radar.radar1', d)
#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriority_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "Radar"
d.childPrefixes = [];
d.units = "percent"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("Null",0,100,100,100,1,1,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.Radar.noRadar', d)

#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriorityOneOnly_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "SmLocal" # this is the dir name under /twc/products and also the viewport name
d.childPrefixes = [];
d.units = "percent"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("TrafficSponsor",0,100,100,100,1,1,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.SmLocal.smTrafficSponsor', d)

#
#
#
d = twc.Data()
d.loadHeuristic = "loadPriorityOneOnly_v1"
d.overHeuristic = "overPriority_v1"
d.underHeuristic = "underPriority_v1"
d.prodPrefix = "SmLocal" # this is the dir name under /twc/products and also the viewport name
d.childPrefixes = [];
d.units = "percent"
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("Null",0,100,100,100,1,1,0,[]),
]
dsm.setDefault("Config." + configVersion + '.Playlist.SmLocal.smNull', d)

#
#   FallbackCore.A - 120 second version
#
d = twc.Data()
d.playlist = [
    ("Local", (("NetworkIntro",0,10),("CurrentConditions",0,12),
              ("LocalObservations",0,12),("LocalObservations",1,12),
              ("LocalDoppler",0,16), ("TextForecast",0,42),
              ("ExtendedForecast",0,14), ("Almanac",0,14),),),
    ("Cc", (("LongCurrentConditions",0,120),),),
    ("Fcst", (("DaypartForecast",0,15),("TextForecast",0,30),
              ("ExtendedForecast",0,15),("DaypartForecast",0,15),
              ("TextForecast",0,30),("ExtendedForecast",0,15),),),
    ("Menu", (("Default",0,120),),),
    ("LasCrawl", (("Default",0,120),),),
    ("Background", (("Default",0,120),),),
    ("Foreground", (("Null",0,120),),),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.FallbackCore.A', d)
#
#   FallbackCore.B - 60 second version
#
d = twc.Data()
d.playlist = [
    #("Product Name",prodInst,optimal,max,min,step,priority,exclusive,childPlaylists)
    ("Local", (("CurrentConditions",0,14), ("LocalDoppler",0,16), 
              ("DaypartForecast",0,14),
              ("ExtendedForecast",0,16))),
    ("Cc", (("LongCurrentConditions",0,60),),),
    ("Fcst", (("DaypartForecast",0,15),("TextForecast",0,30),
              ("ExtendedForecast",0,15),),),
    ("Menu", (("Default",0,60),),),
    ("LasCrawl", (("Default",0,60),),),
    ("Background", (("Default",0,60),),),
    ("Foreground", (("Null",0,60),),),
]  
dsm.setDefault("Config." + configVersion + '.Playlist.FallbackCore.B', d)
