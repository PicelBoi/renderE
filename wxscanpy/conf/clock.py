
import clockConfig
import twc.dsmarshal as dsm
import os

TWCDIR     = os.environ['TWCDIR']
TWCCLIDIR  = os.environ['TWCCLIDIR']
TWCPERSDIR = os.environ['TWCPERSDIR']

clockConfig.setProductDirectory('/usr/twc/wxscan/products')
clockConfig.setWorkDirectory('clocks')
clockConfig.setClimoDataDirectory(TWCPERSDIR + '/data/climatology')
clockConfig.setTempDirectory('temp/clock/rsc')
clockConfig.setDefaultClockFile('default.clock')

#configVersions for Clock and SevereClock are handled in src/bin/clock/main.py
clockConfig.setClockFileKey('Clock')
clockConfig.setSevereModeClockFileKey('SevereClock')

clockConfig.setPreroll(10)
clockConfig.setChannel('SystemEventChannel')
clockConfig.hideUserDefinedNames(0)
clockConfig.setPidFileDirectory(TWCPERSDIR + '/data/pid')
clockConfig.setAppName('clock')
