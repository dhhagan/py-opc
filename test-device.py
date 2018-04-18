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

print ("Running manual OPC-N2 tests...")

sleep(1)

# turn on
print ("Turning ON: {}".format(alpha.on()))

sleep(1)

print ("Reading histogram")
print (alpha.histogram())
sleep(1)

print (alpha.histogram())
sleep(1)

print (alpha.histogram())
sleep(1)

print ("Turning off: {}".format(alpha.off()))
