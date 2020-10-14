# import the necessary parts of the bluepy library
from bluepy.btle import Scanner, DefaultDelegate
import binascii
import struct
import time
import sys


from bluepy.btle import UUID, Peripheral

# create a delegate class to receive the BLE broadcast packets
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # when this python script discovers a BLE broadcast packet, print a message with the device's MAC address
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

# create a scanner object that sends BLE broadcast packets to the ScanDelegate



    # create a list of unique devices that the scanner discovered during a 10-second scan
while True:
    scanner = Scanner().withDelegate(ScanDelegate())
    scanner.clear()
    devices = scanner.scan(2.0)

    # for each device  in the list of devices
    roehladdress = ""
    for dev in devices:
        # print  the device's MAC address, its address type,
        # and Received Signal Strength Indication that shows how strong the signal was when the script received the broadcast.
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))

        for (adtype, desc, value) in dev.getScanData():
            if(value == "Roehl-M001"):
                roehladdress = dev.addr
                print("%s  %s = %s" % (roehladdress,desc, value))

    print("---hello---")
    # temp_uuid = UUID(0xff01)
    service_uuid = UUID(0x00ff)
    print(roehladdress)
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])

    
    if len(roehladdress)<5 :
        print("device not find")
        scanner = None
        p = None
        ch_name = None
        ch_result = None
        ch_write = None
        continue
        # sys.exit()
    print("line 58--waiting device to ble mode , just open blue light")
    try :
        p = Peripheral(roehladdress, "public")
    except Exception:
        print("--Peripheral-reset--")
        scanner = None
        p = None
        ch_name = None
        ch_result = None
        ch_write = None
        continue
    print("line 60-- going ")
    p.setMTU(100)
    # ch = p.getCharacteristics(uuid=temp_uuid)[0]
    print("-----")
    # print(ch.read())
    try:
        service = p.getServiceByUUID(service_uuid)
    except Exception:
        print("------")
        print("--getServiceByUUID reset---")
        p.disconnect()
        scanner = None
        p = None
        ch_name = None
        ch_result = None
        ch_write = None
        continue
    print(service)

    name_UUID = UUID(0xff01)
    result_UUID = UUID(0xff02)
    write_UUID = UUID(0xff03)
    try :
        ch_name = service.getCharacteristics(name_UUID)[0]
        ch_result = service.getCharacteristics(result_UUID)[0]
        ch_write = service.getCharacteristics(write_UUID)[0]
    
        print(ch_name.read())
        print(ch_result.read())
    except Exception:
        print("------")
        print("--read reset---")
        p.disconnect()
        scanner = None
        p = None
        ch_name = None
        ch_result = None
        ch_write = None
        continue

    sendstr = "\"{SSID}\",\"{PWD}\",\"{PSK}\"".format(SSID=sys.argv[1],PWD=sys.argv[2],PSK=sys.argv[3])
    #  ch_write.write(("\"ROEHL\",\"0000000000\",\"8aCuu1ZTB16bLE6gfAZuIA==\"").encode('utf8'))
    try:
        ch_write.write(sendstr.encode('utf8'))
    except Exception:
        print("------")
        print("--write reset---")
        p.disconnect()
        scanner = None
        p = None
        ch_name = None
        ch_result = None
        ch_write = None
        continue

    print("dissconnect")
    p.disconnect()
    scanner = None
    p = None
    ch_name = None
    ch_result = None
    ch_write = None
    # ch_write.write(("\"TP-LINK_AA22\",\"12345678\",\"0+ddxPXizbflrKGCbbiiHg==\"").encode('utf8'))
    # ch_write.write(("\"TP-Link_AA22\",\"1234\",\"Ql6AabU0TQ0O4atkXbux3Q==\"").encode('utf8'))
    #ch_write.write(("\"FreeWifi\",\"789789789\",\"eakzrTt+0qLGdl8UN8lNHw==\"").encode('utf8'))
    # ch_write.write(("\"ROEHL\",\"0000000000\",\"8aCuu1ZTB16bLE6gfAZuIA==\"").encode('utf8'))
    #while(1):
    #    print(ch_result.read())

    # temp_uuid = UUID(0xff03)
    #  0EcnwZVAHJXRcQDW2uhu4Q==
    # ch = p.getCharacteristics(uuid=temp_uuid)[0]
    # # p.writeCharacteristic(ch,("\"TP-LINK_AA22\",\"12345678\",\"0+ddxPXizbflrKGCbbiiHg==\"").encode('utf8'))
    # ch.write(("\"TP-LINK_AA22\",\"12345678\",\"0+ddxPXizbflrKGCbbiiHg==\"").encode('utf8'))
