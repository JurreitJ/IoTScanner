from ZigBeeDeviceFinder import ZigBeeDeviceFinder
from killerbee import *

kb = getKillerBee(0)

zbfinder = ZigBeeDeviceFinder("2:3", 0.0, 0, kb, True)
zbdata = zbfinder.zbstumbler()

for key in zbdata:
    print(zbdata[key][0])
