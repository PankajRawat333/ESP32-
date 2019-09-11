from machine import Pin
import network
import time
from umqtt.robust import MQTTClient
import os
import gc
import sys

led = Pin(2, Pin.OUT)

# the following function is the callback which is 
# called when subscribed data is received
def cb(topic, msg):
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    button_status = str(msg,'utf-8')
    if button_status == "ON":
        led.value(1)
    else:
        led.value(0)
    

# create a random MQTT clientID 
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

# connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
# 
# To use a secure connection (encrypted) with TLS: 
#   set MQTTClient initializer parameter to "ssl=True"
#   Caveat: a secure connection uses about 9k bytes of the heap
#         (about 1/4 of the micropython heap on the ESP8266 platform)
ADAFRUIT_IO_URL = b'io.adafruit.com'
ADAFRUIT_USERNAME = b'adafruit-username'
ADAFRUIT_IO_KEY = b'adafruit-keys'
ADAFRUIT_IO_FEEDNAME = b'ESP32 LED'

client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
    
try:      
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')    
client.set_callback(cb)                    
client.subscribe(mqtt_feedname)  

# following two lines is an Adafruit-specific implementation of the Publish "retain" feature 
# which allows a Subscription to immediately receive the last Published value for a feed,
# even if that value was Published two hours ago.
# Described in the Adafruit IO blog, April 22, 2018:  https://io.adafruit.com/blog/  
mqtt_feedname_get = bytes('{:s}/get'.format(mqtt_feedname), 'utf-8')    
client.publish(mqtt_feedname_get, '\0')  

# wait until data has been Published to the Adafruit IO feed
while True:
    try:
        client.wait_msg()
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()