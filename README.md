# IoTScanning
Python scripts to scan IoT devices for vulnerabilities.


# REQUIREMENTS
For Zigbee analysis the following requirements are needed. 
The IoTScanner uses KillerBee to scan zigbee networks.
For this, it is necessary to install the following Python modules before installation:

serial
usb
crypto (for some functions)
pygtk (for use of tools that have GUIs)
cairo (for use of tools that have GUIs)
scapy-com (for some tools which utilize 802.15.4 Scapy extensions)
On Ubuntu systems, you can install the needed dependencies with the following commands:

# apt-get install python-gtk2 python-cairo python-usb python-crypto python-serial python-dev libgcrypt-dev
# hg clone https://bitbucket.org/secdev/scapy-com
# cd scapy-com
# python setup.py install
The python-dev and libgcrypt are required for the Scapy Extension Patch.

# REQUIRED HARDWARE
The following hardware is needed to analyze zigbee devices.
Currently, the KillerBee framework supports the River Loop ApiMote, Atmel RZ RAVEN USB Stick, MoteIV Tmote Sky, TelosB mote, and Sewino Sniffer.
IoTScanner should work fine with all of these. It was, however, only tested with Atmel RZ RAVEN USB Stick. 

ApiMote v4beta (and v3):
The devices typically come preloaded and do not need to be reflashed for basic use.

The hardware is open-source at https://github.com/riverloopsec/apimote. It is available assembled by contacting team at riverloopsecurity dot com.

This is currently supported for beta, and supports sniffing, injection, and jamming.

Texas Instruments CC2530/1 EMK:
This USB dongle is produced by Texas Instruments and is sold as an evaluation kit for their CC2530 or CC2531 integrated circuit.

It can be purchased from electronics distributors, or directly from them here.

This is currently supported for beta, and supports sniffing only.

MoteIV Tmote Sky or TelosB mode:
This device can be loaded with firmware via USB. Attach the device, and then within killerbee/firmware, run:

$ ./flash_telosb.sh
These boards can be obtained via multiple distributors, however this vendor has stated that their "clone" of the original hardware is compatible. We have not tested nor do we endorse any specific "clone".

Atmel RZ RAVEN USB Stick:
See http://www.atmel.com/tools/RZUSBSTICK.aspx. This hardware is convenient as the base firmware is open source with a freely-available IDE. The KillerBee firmware for the RZ RAVEN included in the firmware/ directory is a modified version of the stock firmware distributed by Atmel to include attack functionality.

The RZ RAVEN USB Stick is available from common electronics resellers for approximately $40/USD:

Mouser: http://bit.ly/vZ2pt
Digi-Key: http://bit.ly/3T8MaK
The stock firmware shipped with this hardware allows you to leverage the passive functionality included in the KillerBee tools and framework (such as receiving frames), but does not allow you to do packet injection, or to impersonate devices on the network.

In order to get the full functionality included in KillerBee, the RZ RAVEN USB Stick must be flashed with the custom firmware included in the firmware/ directory. See https://github.com/riverloopsec/killerbee/blob/master/firmware/README.md for details.
