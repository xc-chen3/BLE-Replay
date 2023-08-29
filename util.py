import json
import binascii
import random
# from bleSuite.bleConnectionManager import BLEConnectionManager
# from bleSuite.bleServiceManager import bleServiceWriteToHandle

from bluepy.btle import Scanner,Peripheral,DefaultDelegate


class NotifyDelegate(DefaultDelegate):
	def __init__(self,params):
		DefaultDelegate.__init__(self)
                
	def handleNotification(self,cHandle,data):
		print("Notification from Handle: 0x" + format(cHandle,"02X"))
		print(data)
                


def replay_file_write(rows, filename):
    with open(filename, "w") as f:
        for row in rows:
            f.write("%s\n" % json.dumps(row))


def gatt_writes(dev, addr, seclevel, addr_type, rows):
    '''Set up the BLE connection and write data'''
    
    # conn = BLEConnectionManager(addr, dev, addr_type,
    #                             seclevel, True)
    # conn.connect()

    conn = Peripheral(addr)

    print("[+]Try Connecting.....")
    if conn:
        print("[+]Connecting successfully!")
        conn.withDelegate(NotifyDelegate(conn))
    else:
        print("[+]Fail to connet")
        exit(1)

    for row in rows:
        handle, message, fuzz_positions, num_iterations = row
        conn.writeCharacteristic(handle,binascii.unhexlify(message))

        # gatt_write(conn, handle, message, fuzz_positions,
        #            num_iterations)
    # conn.disconnect()


# def gatt_write(conn, handle, message, fuzz_positions, num_iterations):
#     '''Make a single write to a handle using bleSuite'''
#     current_message = message
#     if fuzz_positions:
#         for position in fuzz_positions:
#             if position*2 >= len(current_message):
#                 print ("Fuzz position beyond length of message")
#                 return
#             current_message = current_message[0:position*2] + \
#                 binascii.hexlify(chr(random.randint(0, 255))) + \
#                 current_message[position*2:]
#     for _ in range(num_iterations):
#         print ("writing {} ({}) to handle {}".format(current_message,
#                                               repr(current_message.decode('hex')),
#                                               handle))
#         if not conn.isConnected:
#             print ("Connection lost, reconnecting")
#             conn.connect()
#         try:
#             bleServiceWriteToHandle(conn, int(handle, 16),
#                                     current_message.decode('hex'))
#         except Exception as e:
#             print (e)
#             conn.connect()
