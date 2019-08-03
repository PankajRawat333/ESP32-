To setup ESP32 micro controller, follow below link

https://circuitdigest.com/microcontroller-projects/how-to-program-esp32-in-micropython-using-thonny-ide

To erase and flash micropython on esp32 run following command 

1. To erase esp32
esptool.py --chip esp32 erase_flash

2. To flash micropython on esp32 (press boot button before run this command)
esptool.py --chip esp32 --port COM16 write_flash -z 0x1000 esp32-20190730-v1.11-180-g8f55a8fab.bin
