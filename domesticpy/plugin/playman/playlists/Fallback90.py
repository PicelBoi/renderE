# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: Fallback90.py
# Compiled at: 2007-01-12 11:33:37
from functools import reduce
import twc
if twc.personalityCode < 4:
    s = {'Local': [('CurrentConditions', [10 * 30]), ('RegionalObservationMap', [8 * 30]), ('RegionalDopplerRadar', [8 * 30]), ('DaypartForecast', [12 * 30]), ('TextForecast', [36 * 30]), ('7DayForecast', [16 * 30])], 'BackgroundMusic': [('Default', [90 * 30])], 'Tag': [('Null', [50 * 30]), ('Default', [40 * 30])]}

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

