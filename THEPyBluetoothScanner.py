import time
import bluetooth
import os
import sys
import logging
from bluepy.btle import Scanner, DefaultDelegate

if sys.argv[1] == "-V":
    LvlLog = logging.DEBUG
else:
    LvlLog = logging.WARNING

logging.basicConfig(level=LvlLog, filename='Logging.log',filemode='w',
                    format="%(asctime)s - %(levelname)s - %(message)s")

#I don't really know what this does, but it works.
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            logging.info("Discovered device", dev.addr)
        elif isNewData:
            logging.info("Received new data from", dev.addr)
            NEWDATA.append(dev)

#Notice this in an infinite loop
while True:
    logging.debug("Searching BT4...")
    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        logging.info('Found BT4: ', str(bdaddr))
        nearby_device_name = bluetooth.lookup_name(bdaddr)
        #its a file path might be different for yours
        filepath = ("./BlueToothScannedDevices/" + str(nearby_device_name) + ".txt")
        if os.path.exists(filepath) == False:
            nearby_device_services = bluetooth.find_service(address=bdaddr)
            nearby_device_services = '\n'.join(map(str, nearby_device_services))
            file = open(filepath, "a")
            file.write("Address: " + bdaddr + "\nServices: \n" + nearby_device_services)
            file.close
    logging.debug("Transferring to LE...")
    time.sleep(15)
    logging.debug("Searching LE...")
    NEWDATA = []
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(5.0)
    NumberOfDevices = 0
    for dev in devices:
        NumberOfDevices += 1
        LEDATA = ("Device,%s,(%s),RSSI=,%d dB," % (dev.addr, dev.addrType, dev.rssi))
        #its a file path might be different for yours
        filepath = ("./BlueToothLEDevices/" + str(dev.addr) + ".txt")
        if os.path.exists(filepath) == False:
            file = open(filepath, "a")
            file.write(LEDATA + "\n")
            for (adtype, desc, value) in dev.getScanData():
                datastuff = ("%s = %s," % (desc, value))
                file.write(datastuff)
            file.close
    for dev in NEWDATA:
        LEDATA = ("Device,%s," % (dev.addr))
        #its a file path might be different for yours
        filepath = ("./BlueToothLEDevices/_NewDataDevices.txt")
        file = open(filepath, "a")
        file.write(LEDATA + "\n")
        file.close
    logging.info("Number of devices found: " + str(NumberOfDevices))
    logging.debug("Transferring to BT4...")
    time.sleep(15)