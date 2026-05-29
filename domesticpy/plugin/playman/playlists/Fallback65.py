# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: Fallback65.py
# Compiled at: 2015-09-21 16:18:17
from functools import reduce
s = {'Local': [('IntroFS', [2 * 30]), ('WelcomeFS', [3 * 30]), ('NowFS', [12 * 30]), ('RegionalRadarFS', [12 * 30]), ('HourlyForecastFS', [12 * 30]), ('7DayForecastFS', [12 * 30]), ('SummaryFS', [12 * 30])], 'AdCrawl': [('Void', [25 * 30]), ('Default', [40 * 30])]}

def getSchedule(duration):
    return _adjustScheduleLength(s, duration)
    return


def _adjustScheduleLength(s, duration):
    news = {}
    for (stype, pl) in s.items():
        news[stype] = _adjustPlaylistLength(pl, duration)

    return news
    return


def _adjustPlaylistLength(pl, duration):
    tally = 0
    newpl = []
    pllen = len(pl)
    for (prod, durlist) in pl:
        dur = reduce((lambda a, b: a + b), durlist)
        newtally = tally + dur
        if newtally > duration:
            break
        newpl.append((prod, durlist))
        tally = newtally

    remainder = duration - tally
    if remainder > 0:
        durlist = durlist[:-1] + [remainder]
        newpl.append((prod, durlist))
    return newpl
    return

