# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: loadSCMTconfig.py
# Compiled at: 2007-01-12 11:33:37
import os, sys
import patches
import rendereglobals as rg
import playmaninit
#import playmaninit
import twc
import twccommon.Log
import twc.dsmarshal
import twc.DataStoreInterface
import domestic.wxdata
Log = twccommon.Log
ds = twc.DataStoreInterface
dsm = twc.dsmarshal
wxdata = domestic.wxdata

def execfile(filename, globa=None, loca=None):
    with open(filename, "r", encoding="windows-1252") as f:
        exec(compile(f.read(), filename, 'exec'), globa, loca)

def do_absolutely_nothing(*args, **kwargs):
    print(args, kwargs)

def main():
    try:
        TWCPERSDIR = os.environ['TWCPERSDIR']
        TWCCLIDIR = os.environ['TWCCLIDIR']
    except:
        print('environment not setup: TWCCLIDIR and TWCPERSDIR must be defined.')
        sys.exit(1)

    if len(sys.argv) < 2:
        print('Usage: python3 %s {SCMT config script}' % sys.argv[0])
        print('       i.e. - python3 %s config.py' % sys.argv[0])
        sys.exit(1)
    configuration = sys.argv[1]
    if not os.path.exists(configuration):
        print('Error: Configuration file (%s) does not exist! Exiting.' % configuration)
        sys.exit(1)
    ds.init()
    print('Loading configuration: %s' % sys.argv[1])
    twccommon.Log.setIdent('loadSCMTconfig')
    twccommon.Log.info('Loading new configuration %s' % sys.argv[1])  
    execfile(sys.argv[1], {"abortMsg": do_absolutely_nothing, "Log": Log, "ds": ds, "dsm": dsm, "wxdata": wxdata, "twc": twc, "twccommon": twccommon})

    ds.commit()
    print('Configuration Complete.')
    ds.uninit()
    return 0
    return


if __name__ == '__main__':
    sys.exit(main())

