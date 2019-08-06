import iothub
import socket
import ussl
import utime as time
import network
from machine import TouchPad, Pin
import config
import gc

led = Pin(2, Pin.OUT)
cfg = config.Config('config.json')

display = None
builtinLed = None

hub = iothub.IotHub(cfg.host, cfg.deviceId, cfg.key)

wlan = network.WLAN(network.STA_IF)

lastUpdated = 0
updateSas = True


def newSasToken():
    global lastUpdated, updateSas, SAS
    if time.ticks_diff(time.time(), lastUpdated) > 60 * 15:
        lastUpdated = time.time()
        updateSas = True

    if updateSas:
        SAS = hub.generate_sas_token()
        print('Updating Sas')
        updateSas = False

def wlan_connect(ssid='MYSSID', password='MYPASS'):
    if not wlan.active() or not wlan.isconnected():
        wlan.active(True)
        print('connecting to:', ssid)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def checkwifi():
    blinkcnt = 0
    while not wlan.isconnected():
        time.sleep_ms(500)


def main(use_stream=True):

    s = socket.socket()
    ai = socket.getaddrinfo(cfg.host, 443)
    addr = ai[0][-1]
    s.close()

    count = 0
    errorCount = 0
    t = TouchPad(Pin(14))
    while True:
        checkwifi()
        newSasToken()
        count = count + 1
        freeMemory = gc.mem_free()
        val = t.read()
        print(val)
        data = b'{"DeviceId":"%s","Value":%u}' % (cfg.deviceId, val)

        try:
            s = socket.socket()
            s.connect(addr)
            s = ussl.wrap_socket(s)  # SSL wrap

            # Send POST request to Azure IoT Hub
            # s.write("POST /devices/" + cfg.deviceId +
            #         "/messages/events?api-version=2016-02-03 HTTP/1.0\r\n")

            s.write("POST " + hub.endpoint + " HTTP/1.1\r\n")
            # HTTP Headers
            s.write("Host: " + cfg.host + "\r\n")
            s.write("Authorization: " + SAS + "\r\n")
            s.write("Content-Type: application/json\r\n")
            s.write("Connection: close\r\n")
            s.write("Content-Length: " + str(len(data)) + "\r\n\r\n")
            # Data
            s.write(data)

            # Print 128 bytes of response
            print(s.read(128)[:12])

            s.close()
        except:
            led.on()
            print('Problem posting data')
            errorCount = errorCount + 1
            time.sleep(cfg.sampleRate*2)
        finally:
            led.off()
            print('messages sent: %d, errors: %d' % (count, errorCount))
            time.sleep(cfg.sampleRate)


wlan_connect(cfg.ssid, cfg.password)

time.sleep(2)  # allow for a little settle time
main()
