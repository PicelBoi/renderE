# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: FallbackLdl120.py
# Compiled at: 2007-01-12 11:33:37
from functools import reduce
import twc
if twc.personalityCode < 2:
    s = {'Ldl': [('LASCrawl', [4 * 30]), ('TornadoWatch', [6 * 30]), ('LocalStarIDMessage', [10 * 30]), ('CurrentSkyTemp', [4 * 30]), ('CurrentWinds', [4 * 30]), ('CurrentGusts', [4 * 30]), ('CurrentHumidity', [4 * 30]), ('CurrentApparentTemp', [4 * 30]), ('CurrentDewpoint', [4 * 30]), ('CurrentPressure', [4 * 30]), ('CurrentCeiling', [4 * 30]), ('CurrentVisibility', [4 * 30]), ('CurrentMTDPrecip', [4 * 30]), ('Date', [4 * 30]), ('TornadoWatch', [6 * 30]), ('LocalStarIDMessage', [10 * 30]), ('CurrentSkyTemp', [4 * 30]), ('CurrentWinds', [4 * 30]), ('CurrentGusts', [4 * 30]), ('CurrentHumidity', [4 * 30]), ('CurrentApparentTemp', [4 * 30]), ('CurrentDewpoint', [4 * 30]), ('CurrentPressure', [4 * 30]), ('CurrentCeiling', [4 * 30]), ('CurrentVisibility', [4 * 30]), ('CurrentMTDPrecip', [4 * 30])], 'TimeTemp': [('Default', [120 * 30])], 'Logo': [('Default', [120 * 30])]}
else:
    s = {'Ldl': [('IntroAnimation', [2 * 30]), ('CurrentObs', [12 * 30]), ('StarIDMessage', [4 * 30]), ('Void', [120 * 30])], 'LdlMenu': [('IntroAnimation', [2 * 30]), ('Default', [118 * 30])], 'TimeTemp': [('Default', [120 * 30])], 'Logo': [('Default', [120 * 30])]}

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


