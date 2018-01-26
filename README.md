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

    # apt-get install python-gtk2 python-cairo python-usb python-crypto python-serial python-dev libgcrypt-dev

    # hg clone https://bitbucket.org/secdev/scapy-com

    # cd scapy-com

    # python setup.py install

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
The hardware is open-source. It was developed by River Loop Security and can be purchased at https://github.com/riverloopsec/apimote.
It does not need to be flashed, because it comes pre-configured with the KillerBee firmware.
Currently, the device is supported for beta, and supports sniffing, injection, and jamming.

**Atmel RZ RAVEN USB Stick**:
The RZ RAVEN USB Stick is available from most electronic resellers for approximately $40/USD.
For more information on the hardware see http://www.microchip.com/Developmenttools/ProductDetails.aspx?PartNO=ATAVRRZUSBSTICK.

In order to get the full functionality included in KillerBee, the RZ RAVEN USB Stick must be flashed with the custom firmware. See https://github.com/riverloopsec/killerbee/blob/master/firmware/README.md for details.
This device can be flashed, using USB.
The KillerBee firmware for the RZ RAVEN, that can be downloaded with the River Loop Security's KillerBee distribution, is a modified version of the stock firmware distributed by Atmel to include attack functionality.

**Texas Instruments CC2530/1 EMK**:
This USB dongle is produced by Texas Instruments. It is sold as an evaluation kit for their CC2530 or CC2531 integrated circuit.
Currently, this hardware is supported for beta, and supports sniffing only.

**MoteIV Tmote Sky or TelosB mode**:
This device can be loaded with the KillerBee firmware via USB. 
To do that, follow the instructions below:
    
    1. Attach the device
    
    2. Within killerbee/firmware, run:
    
       $ ./flash_telosb.sh
 
Though, some vendors claim, that their clone of this hardware is compatible with KillerBee, it has not been tested by River Loop Security or me.


# Installation

To install IoTScanner, follow the list of steps below.

    1. Make sure, that all requirements are met
    
    2. Download and unzip IoTScanner
    
    3. Install IoTScanner, using setup.py
    
        # python3 setup.py install

# Usage

The example below demonstrates, how IoTScanner is used to scan TCP/IP networks, searching for the usage of standard credentials, and all nearby zigbee networks.


Example:
-
    #sudo python3 IoTScanner.py -cf /samples/test_all.pcap -i 192.168.170.0 -f /configs/devices.cfg -v

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
- -p : Number of packets, to be captured; Default 100
- -d : Delay of sent beacon requests; Default 2.0
- -l : Number of loops for network search





