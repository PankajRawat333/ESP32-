from machine import TouchPad, Pin
from time import sleep

t = TouchPad(Pin(14))
#t.read()              # Returns a smaller number when touched
while True:
    print(t.read())
    sleep(1)