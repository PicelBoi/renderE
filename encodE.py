import twc.dsmarshal as dsm
import requests as r
import twccommon
import traceback
import sqlite3 as sql
import time
from datetime import datetime
import sys

doonly = False
only = ""
if len(sys.argv) > 1:
    doonly = True
    only = sys.argv[1]

print("encodE by LeWolfYT")
print("LFRecord.db is from MARIENCODER!")
print("Make sure to support it too!")

expiretime = time.time()+30*60

stationmap = { #maps closed stations onto not-closed stations
    "KPFN": "KECP"
}

db = sql.connect("LFRecord.db")

cver = dsm.rget("configVersion")
obs = dsm.rget(f"Config.{cver}.interestlist.obsStation")

obstype = [o.startswith("T") for o in obs]

obsadd = [o for o in obs if o.startswith("T")]
obs = [(o if not o.startswith("T") else o[1:]) for o in obs]

coopid = set(dsm.rget(f"Config.{cver}.interestlist.coopId"))
counties = dsm.rget(f"Config.{cver}.interestlist.county")
aqis = dsm.rget(f"Config.{cver}.interestlist.aq")
primarycoop = dsm.rget(f"primaryCoopId")
textfcstcoop = dsm.rget(f"Config.{cver}.Local_TextForecast").coopId
daypartcoop = dsm.rget(f"Config.{cver}.Local_DaypartForecast").coopId[0]
sevendaycoop = dsm.rget(f"Config.{cver}.Local_7DayForecast").coopId
headlinecounty = dsm.rget(f"Config.{cver}.Local_NWSHeadlines").zone
getawaycoop = dsm.rget(f"Config.{cver}.Local_GetawayForecast").coopId
uvcoop = dsm.rget(f"Config.{cver}.Ldl_UVForecast").coopId

metrofcstcoop = [v[0] for v in dsm.rget(f"Config.{cver}.Local_MetroForecastMap").fcstValue[0][1]]
regfcstcoop = [v[0] for v in dsm.rget(f"Config.{cver}.Local_RegionalForecastMap").fcstValue[0][1]]

coopid.add(textfcstcoop)
coopid.add(daypartcoop)
coopid.add(sevendaycoop)
coopid.add(primarycoop)

coopid.update(obsadd)

coopid.update(getawaycoop)

hourlycoop = set()
hourlycoop.add(daypartcoop)
hourlycoop.update(metrofcstcoop)
hourlycoop.update(regfcstcoop)

coopid = list(coopid)

print("Headline county ", headlinecounty)

cur = db.cursor()

windmap = {"Calm": 0, "N": 1, "NNE": 2, "NE": 3, "ENE": 4, "E": 5, "ESE": 6, "SE": 7, "SSE": 8, "S": 9, "SSW": 10, "SW": 11, "WSW": 12, "W": 13, "WNW": 14, "NW": 15, "NNW": 16, "Var": 17}

cidmap = {}

for cid in coopid:
    print(f"Searching for coopId {cid}")
    c2 = cur.execute("SELECT * FROM LFRecord WHERE coopId = ?", (cid,))
    res = c2.fetchone()
    if not res:
        print(f"Failure finding coopId {cid}!")
    else:
        print(f"Found coopId {cid}!")
        cidmap[cid] = (res[7], res[8])

def visround(v):
    return 999 if v is None else round(v)

if not doonly or only == "sensor":
    print(f"starting sensor data!")
    dat = r.get(f"https://wx.lewolfyt.cc?geo={','.join(cidmap[primarycoop])}&include=current,historical").json()
    data = twccommon.Data()
    data.skyCondition = dat["current"]["info"]["narrationCode"]
    data.temp = dat["current"]["conditions"]["temperature"]
    data.humidity = dat["current"]["conditions"]["humidity"]
    data.dewpoint = dat["current"]["conditions"]["dewPoint"]
    data.altimeter = dat["current"]["conditions"]["pressure"]
    data.visibility = visround(dat["current"]["conditions"]["visibility"])
    data.windDirection = windmap[dat["current"]["conditions"]["windCardinal"]]
    data.windSpeed = dat["current"]["conditions"]["windSpeed"]
    data.gusts = dat["current"]["conditions"]["windGusts"]
    data.heatIndex = dat["current"]["conditions"]["heatIndex"]
    data.windChill = dat["current"]["conditions"]["windChill"]
    data.pressureTendency = dat["current"]["conditions"]["pressureTendency"]
    #wxdata.setData(f"obs", stat, data, dat["current"]["info"]["expires"])
    #dat["current"]["info"]["expires"]
    dsm.rset(f"obs.SENSOR", data, expiretime)

if not doonly or only == "obs":
    for i, stat in enumerate(obs):
        print(f"starting obs for {stat}!")
        try:
            if obstype[i]:
                url = f"https://wx.lewolfyt.cc?geo={','.join(cidmap[stat])}&include=current,extended,historical"
            else:
                url = f"https://wx.lewolfyt.cc?icao={stat if stat not in stationmap else stationmap[stat]}&include=current,extended,historical"
            dat = r.get(url).json()
            data = twccommon.Data()
            data.skyCondition = dat["current"]["info"]["narrationCode"]
            data.temp = dat["current"]["conditions"]["temperature"]
            data.humidity = dat["current"]["conditions"]["humidity"]
            data.dewpoint = dat["current"]["conditions"]["dewPoint"]
            data.altimeter = dat["current"]["conditions"]["pressure"]
            data.visibility = visround(dat["current"]["conditions"]["visibility"])
            data.windDirection = windmap[dat["current"]["conditions"]["windCardinal"]]
            data.windSpeed = dat["current"]["conditions"]["windSpeed"]
            data.gusts = dat["current"]["conditions"]["windGusts"]
            data.heatIndex = dat["current"]["conditions"]["heatIndex"]
            data.windChill = dat["current"]["conditions"]["windChill"]
            data.pressureTendency = dat["current"]["conditions"]["pressureTendency"]
            #wxdata.setData(f"obs", stat, data, dat["current"]["info"]["expires"])
            #dat["current"]["info"]["expires"]
            dsm.rset(f"obs.{stat}", data, expiretime)
            rdata = twccommon.Data()
            rdata.tempMax = dat["historical"][1]["tempMax"]
            rdata.tempMin = dat["historical"][1]["tempMin"]
            dsm.rset(f"recObs.{stat}", rdata, expiretime)
        except:
            print(traceback.print_exc())
            print(f"obs failure for {stat}")
    dsm.rcommit()

curr_time = time.time()
y, m, d, H, M, S, wd, day, dst = time.localtime(curr_time)

times = []

#taken from TextForecast
if (H < 4):
    # Start with the 7PM yesterday to 7AM today data.
    # The window for the start of this data (7PM) begins yesterday
    # at noon (and extends to midnight).
    # So, we are looking for the UTC of yesterday at noon.
    times.append(time.mktime((y,m,d-1,12,0,0,0,0,-1)))
    times.append(time.mktime((y,m,d,0,0,0,0,0,-1)))
    times.append(time.mktime((y,m,d,12,0,0,0,0,-1)))
    times.append(time.mktime((y,m,d+1,0,0,0,0,0,-1)))
elif (H < 16):
    # Start with the data for 7AM - 7PM today
    # This will be the UTC data of midnight today
    times.append(time.mktime((y,m,d,0,0,0,0,0,-1)))
    times.append(time.mktime((y,m,d,12,0,0,0,0,-1)))
    times.append(time.mktime((y,m,d+1,0,0,0,0,0,-1)))
    times.append(time.mktime((y,m,d+1,12,0,0,0,0,-1)))
else: 
    # Start with the data for 7PM today to 7AM tomorrow
    # This will be the UTC data of noon today.
    times.append(time.mktime((y,m,d,12,0,0,0,0,-1)))
    times.append(time.mktime((y,m,d+1,0,0,0,0,0,-1)))
    times.append(time.mktime((y,m,d+1,12,0,0,0,0,-1)))
    times.append(time.mktime((y,m,d+2,0,0,0,0,0,-1)))
#i'm just gonna... lie!
def fixac(ac):
    codes = ac.split(":")
    return ":".join([c for c in codes if not c.startswith("DA")])
if not doonly or only == "text":
    print(times)
    print("starting textfcst!")
    try:
        textfcst = r.get(f"https://api.weather.com/v1/geocode/{'/'.join(cidmap[textfcstcoop])}/forecast/daily/10day.json?language=en-US&units=e&apiKey=e1f10a1e78da46f5b10a1e78da96f525").json()["forecasts"]

        done = 0
        ix = 0
        fcsts = []
        expiry = []
        while done < 4:
            if "day" in textfcst[ix]:
                fcsts.append(twccommon.Data(
                    daypartName=textfcst[ix]["day"]["daypart_name"],
                    audioCode=fixac(textfcst[ix]["day"]["vocal_key"]),
                    phrase=textfcst[ix]["day"]["narrative"]
                ))
                expiry.append(textfcst[ix]["expire_time_gmt"])
                done += 1
                if done == 4:
                    break
                fcsts.append(twccommon.Data(
                    daypartName=textfcst[ix]["night"]["daypart_name"],
                    audioCode=fixac(textfcst[ix]["night"]["vocal_key"]),
                    phrase=textfcst[ix]["night"]["narrative"]
                ))
                expiry.append(textfcst[ix]["expire_time_gmt"])
                done += 1
                if done == 4:
                    break
                ix += 1
            else:
                fcsts.append(twccommon.Data(
                    daypartName=textfcst[ix]["night"]["daypart_name"],
                    audioCode=fixac(textfcst[ix]["night"]["vocal_key"]),
                    phrase=textfcst[ix]["night"]["narrative"]
                ))
                expiry.append(textfcst[ix]["expire_time_gmt"])
                done += 1
                if done == 4:
                    break
                ix += 1
        for fcst, tm, ex in zip(fcsts, times, expiry):
            dsm.rset(f"textFcst.{textfcstcoop}.{round(tm)}", fcst, expiretime)
    except:
        traceback.print_exc()
        print("TextForecast generation failed!")

    dsm.rcommit()

if not doonly or only == "hourly":
    print(f"starting local hourly!")
    for coop in list(hourlycoop):
        try:
            print(cidmap[coop])
            dat = r.get(f"https://wx.lewolfyt.cc?geo={','.join(cidmap[coop])}").json()
            
            for hr in dat["hourly"]:
                data = twccommon.Data()
                data.skyCondition = hr["narrationCode"]
                data.temp = round(hr["temperature"])
                data.windDir = windmap[hr["windCardinal"]]
                data.windSpeed = hr["windSpeed"]
                data.heatIndex = round(hr["heatIndex"])
                data.windChill = round(hr["windChill"])
                #hr["expires"]
                print("hourly data for", hr["valid"])
                dsm.rset(f"hourlyFcst.{coop}.{hr['valid']}", data, expiretime)
        except:
            print(traceback.print_exc())
            print(f"daypart failure for {coop}")
        
    dsm.rcommit()

if not doonly or only == "fcst":
    cidlist = list(set([sevendaycoop] + [primarycoop] + getawaycoop + metrofcstcoop + regfcstcoop))
    for ci in cidlist:
        try:
            print(f"starting forecast data for {ci}!")
            print(cidmap[sevendaycoop])
            dat = r.get(f"https://wx.lewolfyt.cc?geo={','.join(cidmap[ci])}&extendeddays=10").json()
            
            for i in range(8):
                j = i + (dat["extended"]["daily"][0]["partiallyObserved"])
                jj = (i*2+1) if dat["extended"]["daily"][0]["partiallyObserved"] else (i*2)
                dailydat = dat["extended"]["daily"][j]
                daypartdat = dat["extended"]["daypart"][jj]
                daypartdat2 = dat["extended"]["daypart"][jj+1]
                
                y,m,d,H,M,S,wday,jday,dst = time.localtime(dailydat["valid"])
                ktime = time.mktime((y,m,d,0,0,0,wday,jday,-1))
                
                data = twccommon.Data()
                data.daySkyCondition = daypartdat["narrationCode"]
                data.skyCondition = daypartdat["narrationCode"]
                data.eveningSkyCondition = daypartdat2["narrationCode"]
                data.highTemp = dailydat["calendarTempMax"]
                data.lowTemp = dailydat["calendarTempMin"]
                data.dayWindSpeed = daypartdat["windSpeed"]
                data.dayWindDir = windmap[daypartdat["windCardinal"]]
                data.golfIndex = 3
                #dailydat["expires"]
                dsm.rset(f"dailyFcst.{ci}.{int(ktime)}", data, expiretime)
        except:
            print(traceback.print_exc())
            print(f"fcst failure for {ci}")
    dsm.rcommit()

if (not doonly or only == "uvf") or only == "tag":
    try:
        print(f"starting uv forecast data for {uvcoop}!")
        dat = r.get(f"https://wx.lewolfyt.cc?geo={','.join(cidmap[uvcoop])}&extendeddays=10").json()
        
        #ldl uv forecast
        # create fcst times
        y,m,d,H,M,S,dow,doy,dst = time.localtime(time.time())
        todayStart = time.mktime((y,m,d,0,0,0,0,0,-1))
        tomStart   = time.mktime((y,m,d+1,0,0,0,0,0,-1))

        # get uv fcst
        # check for fcst time - before 4pm = today, after 4pm = tom
        if H >= 0 and H < 16:
            start = todayStart
        else:
            start = tomStart
        # set data
        dsm.rset('uvDailyFcst.%s.%d' % (uvcoop, start), twccommon.Data(index=dat["extended"]["daypart"][0]["uvIndex"]), expiretime)
    except:
        print(traceback.print_exc())
        print(f"uvf failure for {uvcoop}")

dsm.rcommit()

if only == "tag":
    idx = dsm.rget("primaryIndexId")
    primpollen = dsm.rget("primaryPollenStation")
    print(f"starting tag data!")
    y,m,d,H,M,S,wd,day,dst = time.localtime(time.time())
    IdxDate = int(time.mktime((y, m, d, 0, 0, 0, 0, 0, -1)))
    IdxDate2 = int(time.mktime((y, m, d+1, 0, 0, 0, 0, 0, -1)))
    mosquito = r.get(f"https://api.weather.com/v2/indices/mosquito/daily/15day?geocode={','.join(cidmap[primarycoop])}&language=en-US&format=json&apiKey=e1f10a1e78da46f5b10a1e78da96f525").json()["mosquitoIndex24hour"]["eveningMosquitoIndex"]
    dsm.rset(f"evening_mosquito.{idx}.{IdxDate}", twccommon.Data(dayIndex=mosquito[0]), expiretime)
    dsm.rset(f"evening_mosquito.{idx}.{IdxDate2}", twccommon.Data(dayIndex=mosquito[1]), expiretime)
    
    grillby_s = r.get(f"https://api.weather.com/v2/indices/travel/daypart/15day?geocode={','.join(cidmap[primarycoop])}&language=en-US&format=json&apiKey=e1f10a1e78da46f5b10a1e78da96f525").json()["travelIndex12hour"]
    second_day = (1 if grillby_s["dayInd"][0]=="N" else 2)
    dsm.rset(f"sight_seeing.{idx}.{IdxDate}", twccommon.Data(dayIndex=grillby_s["leisureTravelIndex"][0]), expiretime)
    dsm.rset(f"sight_seeing.{idx}.{IdxDate2}", twccommon.Data(dayIndex=grillby_s["leisureTravelIndex"][second_day]), expiretime)
    
    bonehurtingjuice = r.get(f"https://api.weather.com/v2/indices/achePain/daypart/15day?geocode={','.join(cidmap[primarycoop])}&language=en-US&format=json&apiKey=e1f10a1e78da46f5b10a1e78da96f525").json()["achesPainsIndex12hour"]
    second_day = (1 if bonehurtingjuice["dayInd"][0]=="N" else 2)
    dsm.rset(f"achesAndPain.{idx}.{IdxDate}", twccommon.Data(dayIndex=bonehurtingjuice["achesPainsIndex"][0]), expiretime)
    dsm.rset(f"achesAndPain.{idx}.{IdxDate2}", twccommon.Data(dayIndex=bonehurtingjuice["achesPainsIndex"][second_day]), expiretime)
    
    peelingoffmyskin = r.get(f"https://api.weather.com/v2/indices/drySkin/daypart/15day?geocode={','.join(cidmap[primarycoop])}&language=en-US&format=json&apiKey=e1f10a1e78da46f5b10a1e78da96f525").json()["drySkinIndex12hour"]
    second_day = (1 if peelingoffmyskin["dayInd"][0]=="N" else 2)
    dsm.rset(f"dry_skin.{idx}.{IdxDate}", twccommon.Data(dayIndex=peelingoffmyskin["drySkinIndex"][0]), expiretime)
    dsm.rset(f"dry_skin.{idx}.{IdxDate2}", twccommon.Data(dayIndex=peelingoffmyskin["drySkinIndex"][second_day]), expiretime)
    
    
    ow_my_lungs = r.get(f"https://api.weather.com/v2/indices/pollen/daypart/15day?geocode={','.join(cidmap[primarycoop])}&language=en-US&format=json&apiKey=e1f10a1e78da46f5b10a1e78da96f525").json()["pollenForecast12hour"]
    second_day = (1 if ow_my_lungs["dayInd"][0] == "N" else 2)
    dsm.rset(f"pollen.{primpollen}", twccommon.Data(
        treePollen=ow_my_lungs["treePollenIndex"][0],
        grassPollen=ow_my_lungs["grassPollenIndex"][0],
        weedPollen=ow_my_lungs["ragweedPollenIndex"][0],
        moldCount=None,
        reportTime=ow_my_lungs["fcstValid"][0]
    ), expiretime)
    dsm.rset(f"pollen.{primpollen}", twccommon.Data(
        treePollen=ow_my_lungs["treePollenIndex"][second_day],
        grassPollen=ow_my_lungs["grassPollenIndex"][second_day],
        weedPollen=ow_my_lungs["ragweedPollenIndex"][second_day],
        moldCount=None,
        reportTime=ow_my_lungs["fcstValid"][second_day]
    ), expiretime)
    
dsm.rcommit()

codes = {
    "CFW": "CFW005",
    "CFA": "CFW006",
    "FFW": "FFS007",
    "FFA": "FFS008",
    "FLA": "FFS009",
    "FLW": "LSH005",
    "TOA": "SLS001",
    "HWW": "NPW014",
    "HWA": "NPW013"
}

codes = {
    "Snow Advisory": "WSW020",
    "Flood Advisory Update": "FLS001",
    "Dense Fog Advisory": "NPW005",
    "Fog Advisory Update": "NPW004",
    "High Wind Watch Update": "NPW007",
    "Fog Advisory": "NPW006",
    "Dense Fog Advisory Update": "NPW001",
    "Fog Advisory Update": "NPW002",
    "Fog Warning Update": "NPW041",
    "Dense Fog Warning Update": "NPW040",
    "Fog Warning": "NPW043",
    "Flood Warning Update": "FLS002",
    "Wind Advisory Update": "NPW009",
    "High Wind Warning Update": "NPW008",
    "Emergency Management Bulletin": "HHH001",
    "Flash Flood Warning Update": "FFS003",
    "Flood Watch Update": "FFS002",
    "Flash Flood Watch Update": "FFS001",
    "Lake Effect Snow Warning": "WSW028",
    "Flash Flood Warning Update": "FFS007",
    "Flood Watch Update": "FFS005",
    "Flash Flood Watch Update": "FFS004",
    "Ice Storm Warning Update": "WSW023",
    "Blizzard Warning": "WSW022",
    "Heavy Snow Warning": "WSW021",
    "Snow Squall Warning": "WSW021",
    "Flash Flood Watch Update": "FFS008",
    "Lake Effect Snow Warning Update": "WSW027",
    "Ice Storm Warning": "WSW025",
    "Ice Storm Warning Update": "WSW024",
    "Flood Watch Update": "FFA007",
    "Flood Advisory Update": "FLS003",
    "Severe Weather Update": "SVS003",
    "Flood Warning Update": "FLS005",
    "Flood Advisory Update": "FLS004",
    "Coastal Flood Warning Update": "CFW001",
    "Coastal Flood Watch Update": "CFW002",
    "Coastal Flood Warning": "CFW005",
    "Coastal Flood Watch": "CFW006",
    "Coastal Flood Statement": "CFW007",
    "High Surf Advisory Update": "CFW008",
    "High Surf Advisory": "CFW010",
    "Severe Thunderstorm Watch": "SLS002",
    "Severe Weather Watch": "SLS003",
    "Severe Thunderstorm Warning": "SVR001",
    "Tornado Watch": "SLS001",
    "Heat Advisory Update": "NPW034",
    "Excessive Heat Warning": "NPW035",
    "Heat Advisory": "NPW036",
    "Weather Advisory": "NPW037",
    "Flash Flood Watch Update": "FFA001",
    "Freeze Advisory Update": "WSW038",
    "Flood Watch Update": "FFA002",
    "Flash Flood Watch": "FFA005",
    "Flash Flood Warning": "FFW001",
    "Flood Watch": "FFA006",
    "Blizzard Warning Update": "WSW012",
    "Winter Weather Advisory Update": "WSW013",
    "Snow Advisory Update": "WSW010",
    "Heavy Snow Warning Update": "WSW011",
    "Heavy Snow Warning Update": "WSW016",
    "Blizzard Warning Update": "WSW017",
    "Snow Advisory Update": "WSW014",
    "Snow Advisory Update": "WSW015",
    "Freeze Advisory": "NPW024",
    "Winter Weather Advisory": "WSW018",
    "Snow and Blowing Snow Advisory": "WSW019",
    "Flood Update": "FLS009",
    "Flood Advisory": "FLS008",
    "Freeze Warning Update": "NPW018",
    "Flood Advisory Update": "FLS006",
    "Heat Advisory Update": "NPW032",
    "Frost Advisory Update": "WSW042",
    "Test Warning": "AAA001",
    "Flood Advisory": "FLS007",
    "Tornado Warning Update": "SPS008",
    "Severe Thunderstorm Watch Update": "SPS009",
    "Significant Weather Outlook": "SPS006",
    "Tornado Watch Update": "SPS007",
    "Hazardous Weather Outlook": "SPS001",
    "Fog Warning Update": "NPW039",
    "Wind Chill Advisory Update": "NPW029",
    "Wind Chill Advisory Update": "NPW028",
    "Frost Advisory": "NPW027",
    "Frost Advisory Update": "NPW026",
    "Frost Advisory Update": "NPW025",
    "Frost Warning Update": "WSW033",
    "Freeze Advisory Update": "NPW022",
    "Frost Warning": "NPW021",
    "Freeze Warning": "NPW020",
    "Winter Storm Warning Update": "WSW001",
    "Tropical Storm Local Statement": "HLS002",
    "Winter Storm Warning Update": "WSW003",
    "Winter Storm Watch Update": "WSW002",
    "Winter Storm Warning": "WSW005",
    "Winter Storm Watch Update": "WSW004",
    "Winter Weather Message": "WSW007",
    "Winter Weather Advisory Update": "WSW008",
    "Snow Advisory Update": "WSW009",
    "Winter Storm Watch": "WSW006",
    "Flood Warning": "FLW002",
    "Winter Weather Message": "WSW044",
    "Frost Advisory Update": "WSW041",
    "Freeze Advisory": "WSW040",
    "Frost Advisory": "WSW043",
    "Tsunami Bulletin": "TSU001",
    "Hurricane Local Statement": "HLS003",
    "Tropical Depression Local Statement": "HLS004",
    "Typhoon Local Statement": "HLS005",
    "High Wind Watch Update": "SPS015",
    "High Wind Warning Update": "SPS014",
    "Weather Statement": "SPS017",
    "Significant Weather Alert": "SPS018",
    "Special Weather Statement": "SPS016",
    "Winter Storm Warning Update": "SPS011",
    "Lake Effect Snow Advisory Update": "WSW029",
    "Winter Storm Update": "SPS013",
    "Severe Thunderstorm Warning Update": "SPS010",
    "Freeze Warning Update": "NPW016",
    "Frost Warning Update": "NPW017",
    "High Wind Warning": "NPW014",
    "Wind Advisory": "NPW015",
    "Wind Advisory Update": "NPW012",
    "High Wind Watch": "NPW013",
    "High Wind Watch Update": "NPW010",
    "High Wind Warning Update": "NPW011",
    "Lake Levels": "LLL001",
    "Winter Storm Watch Update": "SPS012",
    "Severe Thunderstorm Warning Update": "SVS001",
    "Frost Warning Update": "NPW019",
    "Dense Fog Warning Update": "NPW038",
    "Wind Chill Advisory": "NPW030",
    "Flash Flood Statement": "FFS010",
    "Freeze Advisory Update": "WSW039",
    "Excessive Heat Warning Update": "NPW031",
    "Freeze Warning Update": "WSW034",
    "Frost Warning Update": "WSW035",
    "Freeze Warning": "WSW036",
    "Frost Warning": "WSW037",
    "Lake Effect Snow Advisory Update": "WSW030",
    "Lake Effect Snow Advisory": "WSW031",
    "Freeze Warning Update": "WSW032",
    "Hurricane Local Statement": "HLS001",
    "Dense Fog Warning": "NPW042",
    "River Flood Warning": "FLW001",
    "Excessive Heat Warning Update": "NPW033",
    "Red Cross Message": "RED001",
    "Tornado Warning Update": "SVS002",
    "Flood Watch Update": "FFS009",
    "Tornado Warning": "TOR001",
    "Lakeshore Flood Warning Update": "LSH001",
    "Lakeshore Flood Watch Update": "LSH002",
    "Lakeshore Flood Warning Update": "LSH003",
    "Lakeshore Flood Watch Update": "LSH004",
    "Lakeshore Flood Warning": "LSH005",
    "Lakeshore Flood Watch": "LSH006",
    "Lakeshore Flood Statement": "LSH007",
    "Lake Effect Snow Watch Update": "WSW045",
    "Lake Effect Snow Watch Update": "WSW046",
    "Lake Effect Snow Watch": "WSW047",
    "Blizzard Watch Update": "WSW048",
    "Blizzard Watch Update": "WSW049",
    "Blizzard Watch": "WSW050",
    "Heavy Sleet Warning Update": "WSW051",
    "Heavy Sleet Warning Update": "WSW052",
    "Heavy Sleet Warning": "WSW053",
    "Freezing Rain Advisory Update": "WSW054",
    "Freezing Rain Advisory Update": "WSW055",
    "Freezing Rain Advisory": "WSW056",
    "Sleet Advisory Update": "WSW057",
    "Sleet Advisory Update": "WSW058",
    "Sleet Advisory": "WSW059",
    "Blowing Snow Advisory Update": "WSW060",
    "Blowing Snow Advisory Update": "WSW061",
    "Blowing Snow Advisory": "WSW062",
    "Wind Chill Warning Update": "WSW063",
    "Wind Chill Warning Update": "WSW064",
    "Wind Chill Warning": "WSW065",
    "Wind Chill Watch Update": "WSW066",
    "Wind Chill Watch Update": "WSW067",
    "Wind Chill Watch": "WSW068",
    "Wind Chill Advisory Update": "WSW069",
    "Wind Chill Advisory Update": "WSW070",
    "Wind Chill Advisory": "WSW071",
    "Excessive Cold Warning Update": "NPW044",
    "Excessive Cold Warning": "NPW046",
    "Excessive Cold Watch Update": "NPW047",
    "Excessive Cold Watch": "NPW049",
    "Excessive Heat Watch Update": "NPW050",
    "Excessive Heat Watch": "NPW052",
    "Freeze Watch Update": "NPW053",
    "Freeze Watch": "NPW055",
    "Inland Hurricane Watch Update": "NPW056",
    "Inland Hurricane Watch": "NPW058",
    "Inland Tropical Storm Watch Update": "NPW059",
    "Inland Tropical Storm Watch": "NPW061",
    "Inland Hurricane Warning Update": "NPW062",
    "Inland Hurricane Warning": "NPW064",
    "Inland Tropical Storm Warning Update": "NPW065",
    "Inland Tropical Storm Warning": "NPW067",
    "Dust Storm Warning Update": "NPW068",
    "Dust Storm Warning": "NPW070",
    "Air Stagnation Advisory Update": "NPW071",
    "Air Stagnation Advisory": "NPW073",
    "Ashfall Advisory Update": "NPW074",
    "Ashfall Advisory": "NPW076",
    "Blowing Dust Advisory Update": "NPW077",
    "Blowing Dust Advisory": "NPW079",
    "Blowing Snow Advisory Update": "NPW080",
    "Blowing Snow Advisory": "NPW082",
    "Dense Smoke Advisory Update": "NPW083",
    "Dense Smoke Advisory": "NPW085",
    "Freezing Fog Advisory Update": "NPW086",
    "Freezing Fog Advisory": "NPW088",
    "Lake Wind Advisory Update": "NPW089",
    "Lake Wind Advisory": "NPW091",
    "Excessive Heat Outlook": "NPW092",
    "Excessive Cold Outlook": "NPW093",
    "Freeze Outlook": "NPW094",
    "High Wind Outlook": "NPW095",
    "Wind Chill Outlook": "NPW096",
    "Avalanche Watch Update": "AVA001",
    "Avalanche Watch": "AVA003",
    "Avalanche Warning Update": "AVW001",
    "Avalanche Warning": "AVW003",
    "Civil Danger Warning Update": "CDW001",
    "Civil Danger Warning": "CDW003",
    "Civil Emergency Message": "CEM040",
    "Immediate Evacuation Bulletin": "EVI001",
    "Earthquake Warning Update": "EQW001",
    "Earthquake Warning": "EQW003",
    "Fire Warning Update": "FRW001",
    "Fire Warning": "FRW003",
    "Hazardous Materials Warning Update": "HMW001",
    "Hazardous Materials Warning": "HMW003",
    "Local Area Emergency": "LAE001",
    "Shelter in Place Warning": "SPW001",
    "Volcano Warning Update": "VOW001",
    "Volcano Warning": "VOW003"
}

if (not doonly or only == "bulletin") and only != "clearbulletin" and False:
    print("starting bulletins")
    for c in counties:
        try:
            alerts = r.get(f"https://api.weather.gov/alerts/active?zone={c}").json()
            headline_groups = {}
            pri = -1
            for f in alerts["features"]:
                try:
                    props = f["properties"]
                    if props["event"] not in codes:
                        print(f"skipping {props['event']} since it's not in the list")
                        continue
                    bull = twccommon.Data()
                    code = codes[props["event"]]
                    bull.pil = code[:3]
                    bull.pilExt = code[3:] #this is the only one. so i'm using it.
                    bull.text = props["headline"]
                    print(f"adding bulletin for {c}: {bull.text}")
                    bull.issueTime = int(datetime.fromisoformat(props["sent"]).timestamp())
                    bull.expiration = int(datetime.fromisoformat(props["expires"]).timestamp())
                    bull.dispExpiration = bull.expiration
                    group = dsm.rget(f"Config.1.pil.{code}")
                    if pri != -1:
                        if group.priority > pri:
                            headline_groups[group.group] = bull
                            pri = group.priority
                    else:
                        headline_groups[group.group] = bull
                        pri = group.priority
                except:
                    traceback.print_exc()
                    print(f"failed to add headline for {props['event']} in county {c}")
            
            print(f"{c} headlines done!")
            for g in list(headline_groups.keys()):
                dsm.rset("bulletin.%s.%d" % (c, int(g)), headline_groups[g], expiretime)
        except:
            traceback.print_exc()
            print(f"error on {c}!")

    dsm.rcommit()

if only == "clearbulletin":
    headline_groups = [1, 2, 3, 4, 5]
    for c in counties:
        for g in headline_groups:
            dsm.rset("bulletin.%s.%d" % (c, g), [], time.time())


exit()
print("starting nws headlines")

try:
    alerts = r.get(f"https://api.weather.gov/alerts/active?zone=MTC015").json()
    hexpiretime = 1
    zoneprops = {}
    headlines = []
    vocal = []
    for f in alerts["features"]:
        try:
            props = f["properties"]
            headline = props["headline"]
            hexpiretime = max(int(datetime.fromisoformat(props["expires"]).timestamp()), hexpiretime)
            headlines.append(headline)
            vocalcode = codes[props["eventCode"]["SAME"][0]]
            vocal.append(vocalcode)
            print(f"added headline {headline} {vocal}")
        except:
            traceback.print_exc()
            print("anywho,")
    print("expires", hexpiretime)
    dsm.rset(f"hdln.{headlinecounty}", twccommon.Data(headlines=headlines, vocal=vocal), hexpiretime)
except:
    print("headline failure!")