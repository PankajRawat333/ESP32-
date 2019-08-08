from machine import Pin
from time import sleep

ldr = Pin(14, Pin.IN)
#t.read()              # Returns a smaller number when touched
while True:
    print(ldr.value())
    sleep(1)
