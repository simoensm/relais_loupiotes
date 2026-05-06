import RPi.GPIO as GPIO
import time
import random
import datetime
from pythonosc.udp_client import SimpleUDPClient

# GPIO sensor
PIN = 27

# OSC client
OSC_IP = "127.0.0.1"
OSC_PORT = 7701
#OSC_ADDRESS = "/anything"  # address doesn’t matter in your QLC+ setup
OSC_ADDRESSES = [
    "/chaser/1",
    "/chaser/2",
    "/chaser/3",
    "/chaser/4",
    "/chaser/5"
]
OSC_VALUE = 255


client = SimpleUDPClient(OSC_IP, OSC_PORT)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last_state = 1

print("System ready, sensor -> QLC+")

try:
    prevNow = 0
    while True:
        current_state = GPIO.input(PIN)

        # Trigger only on falling edge
        if current_state == 0 and last_state == 1:


            address = random.choice(OSC_ADDRESSES)
            print("DETECTED! Sending "+ str(address))

            now = int(datetime.datetime.now().timestamp())
            delta = now - prevNow
            if( delta > 2):
                client.send_message(address, OSC_VALUE)
                #ime.sleep(0.3)  # debounce
                print("it works" + str(delta))
                print(address)
                prevNow = now
            else:
                print("NOPE" + str(delta))

        last_state = current_state
        #time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()