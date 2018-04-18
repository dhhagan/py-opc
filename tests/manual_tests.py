"""Run these tests at the command line/terminal via

    $ python3 tests/manual_tests.py
"""
import usbiss
from usbiss.spi import SPI
import opc
from time import sleep

spi = SPI("/dev/ttyACM0")

spi.mode = 1
spi.max_speed_hz = 500000

alpha = opc.OPCN2(spi, debug=True)

# turn on
print ("Turning ON")
print (alpha.on())

print ("Reading histogram")
print (alpha.histogram())

sleep(5)

print ("Turning off")
print (alpha.off())
