import signal
import time

import urllib.request
import urllib.parse
import RPi.GPIO as GPIO



from pirc522 import RFID


run = True
rdr = RFID()
util = rdr.util()
util.debug = True

LED = 40
#GPIO.setmode(GPIO.BOARD)

GPIO.setup(LED,GPIO.OUT)
GPIO.output(LED, False)



def sender(rf_no,rf_id):

     data = urllib.parse.urlencode({'rf_no': str(rf_no), 'rf_id': rf_id})
     data = data.encode('utf-8')
     request = urllib.request.Request("http://himamohan.esy.es/rfid.php")

     # adding charset parameter to the Content-Type header.
     request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")

     f = urllib.request.urlopen(request, data)
     # print(f.read().decode('utf-8'))
       




def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()




signal.signal(signal.SIGINT, end_read)

print("Starting")
while run:
    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
        s_uid = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
        print(s_uid)
        GPIO.output(LED, True)

        sender(2,s_uid)
        #print("Setting tag")
        # util.set_tag(uid)
        # print("\nAuthorizing")
        #util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
        #util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
        #print("\nReading")
        # util.read_out(4)
       # print("\nDeauthorizing")
       # util.deauth()

        time.sleep(1)
        print('ok!!!!')
        GPIO.output(LED, False)
