# IoTScanner
Python scripts to scan IoT devices for vulnerabilities.


# REQUIREMENTS
For Zigbee analysis the following requirements are needed. 
The IoTScanner uses KillerBee to scan zigbee networks.
For this, it is necessary to install the following Python modules before installation:

- serial
- usb
- crypto (for some functions)
- pygtk (for use of tools that have GUIs)
- cairo (for use of tools that have GUIs)
-  scapy-com (for some tools which utilize 802.15.4 Scapy extensions)

On Ubuntu systems, you can install the needed dependencies with the following commands:

\# apt-get install python-gtk2 python-cairo python-usb python-crypto python-serial python-dev libgcrypt-dev

\# hg clone https://bitbucket.org/secdev/scapy-com

\# cd scapy-com

\# python setup.py install

The python-dev and libgcrypt are required for the Scapy Extension Patch.

The IoTScanner also uses:

- Nmap - to search for open ports

- BeautifulSoup - to analyse http-responses

- urllib - to establish http connections

- paramiko - to establish ssh connections

- netaddr - to handle ip adresses

These dependencies are being installed via PyPi, while installing IoTScanner.


# REQUIRED HARDWARE
The following hardware is needed to analyze zigbee devices.
Currently, the KillerBee framework supports the River Loop ApiMote, Atmel RZ RAVEN USB Stick, MoteIV Tmote Sky, TelosB mote, and Sewino Sniffer.
IoTScanner should work fine with all of these. It was, however, only tested with Atmel RZ RAVEN USB Stick. 

**ApiMote v4beta (and v3)**:
The devices typically come preloaded and do not need to be reflashed for basic use.

The hardware is open-source at https://github.com/riverloopsec/apimote. It is available assembled by contacting team at riverloopsecurity dot com.

This is currently supported for beta, and supports sniffing, injection, and jamming.

**Texas Instruments CC2530/1 EMK**:
This USB dongle is produced by Texas Instruments and is sold as an evaluation kit for their CC2530 or CC2531 integrated circuit.

It can be purchased from electronics distributors, or directly from them here.

This is currently supported for beta, and supports sniffing only.

**MoteIV Tmote Sky or TelosB mode**:
This device can be loaded with firmware via USB. Attach the device, and then within killerbee/firmware, run:

$ ./flash_telosb.sh
These boards can be obtained via multiple distributors, however this vendor has stated that their "clone" of the original hardware is compatible. We have not tested nor do we endorse any specific "clone".

**Atmel RZ RAVEN USB Stick**:
See http://www.atmel.com/tools/RZUSBSTICK.aspx. This hardware is convenient as the base firmware is open source with a freely-available IDE. The KillerBee firmware for the RZ RAVEN included in the firmware/ directory is a modified version of the stock firmware distributed by Atmel to include attack functionality.

The RZ RAVEN USB Stick is available from common electronics resellers for approximately $40/USD:

Mouser: http://bit.ly/vZ2pt
Digi-Key: http://bit.ly/3T8MaK
The stock firmware shipped with this hardware allows you to leverage the passive functionality included in the KillerBee tools and framework (such as receiving frames), but does not allow you to do packet injection, or to impersonate devices on the network.

In order to get the full functionality included in KillerBee, the RZ RAVEN USB Stick must be flashed with the custom firmware included in the firmware/ directory. See https://github.com/riverloopsec/killerbee/blob/master/firmware/README.md for details.

# Installation

To install IoTScanner, follow the list of steps below.

1. Make sure, that all requirements are met
2. Download and unzip IoTScanner
3. Install IoTScanner, using setup.py
    
    \# python3 setup.py install

# Usage

The example below demonstrates, how IoTScanner is used to scan TCP/IP networks, searching for the usage of standard credentials, and all nearby zigbee networks.


Example:
-
\#sudo python3 IoTScanner.py -cf /samples/test_all.pcap -i 192.168.170.0 -f /configs/devices.cfg -v

Required parameters for network scans:
-
- -c : Path to configuration file, containing device data
- -i : IP addresses to scan (format: "192.168.170.0-192.168.170.255" or "192.168.170.0" or "192.168.170.0, 192.168.170.101")

Required parameters for zigbee scanning:
-
- -cf : Path to file, where packages should be captured

Optional parameters for zigbee scanning:
-
- -c : Channel to sniff; If nothing is specified, IoTScanner searches for aöö nearby zigbee devices and uses their channels
- -d : Delay of sent beacon requests; Default 2.0
- -p : Number of packets, to be captured; Default 100




