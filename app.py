# import the necessary parts of the bluepy library
from bluepy.btle import Scanner, DefaultDelegate
import binascii
import struct
import time
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
scanner = Scanner().withDelegate(ScanDelegate())

# create a list of unique devices that the scanner discovered during a 10-second scan
devices = scanner.scan(1.0)

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
p = Peripheral(roehladdress, "public")
p.setMTU(100)
# ch = p.getCharacteristics(uuid=temp_uuid)[0]
print("-----")
# print(ch.read())
service = p.getServiceByUUID(service_uuid)
print(service)

name_UUID = UUID(0xff01)
result_UUID = UUID(0xff02)
write_UUID = UUID(0xff03)
ch_name = service.getCharacteristics(name_UUID)[0]
ch_result = service.getCharacteristics(result_UUID)[0]
ch_write = service.getCharacteristics(write_UUID)[0]

print(ch_name.read())
print(ch_result.read())
# ch_write.write(("\"TP-LINK_AA22\",\"12345678\",\"0+ddxPXizbflrKGCbbiiHg==\"").encode('utf8'))
# ch_write.write(("\"TP-Link_AA22\",\"1234\",\"Ql6AabU0TQ0O4atkXbux3Q==\"").encode('utf8'))
ch_write.write(("\"FreeWifi\",\"789789789\",\"\"").encode('utf8'))
#while(1):
#    print(ch_result.read())

# temp_uuid = UUID(0xff03)
#  0EcnwZVAHJXRcQDW2uhu4Q==
# ch = p.getCharacteristics(uuid=temp_uuid)[0]
# # p.writeCharacteristic(ch,("\"TP-LINK_AA22\",\"12345678\",\"0+ddxPXizbflrKGCbbiiHg==\"").encode('utf8'))
# ch.write(("\"TP-LINK_AA22\",\"12345678\",\"0+ddxPXizbflrKGCbbiiHg==\"").encode('utf8'))
