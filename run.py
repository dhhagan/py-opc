'''
    Test script to run the OPC!
'''

from opc import OPCN2

import spidev
from time import sleep
import sys

# Define some things for the OPC-N2
SPI_MODE        = 1
SPI_CLK         = 500000
SPI_MSBFIRST    = True

# Setup the Spidev connection
spi = spidev.SpiDev()

# Open the spi connection at port 0
spi.open(0, 0)

# Set some things
spi.mode            = SPI_MODE
spi.max_speed_hz    = SPI_CLK
spi.lsbfirst        = not SPI_MSBFIRST

opc = OPCN2(spi)

# Turn the OPC ON
print ("Turning on the OPC")
print ("ON: {0}".format(opc.on()))

sleep(1)

# Read the info
print ("Reading the information string")
print (opc.read_info_string())

sleep(1)

# Read the histogram
i = 0
try:
    while True:
        print ("Reading the histogram: Run {0}".format(i))
        hist = opc.read_histogram()
        print (hist)
        sleep(10)
        i += 1
except KeyboardInterrupt:
    opc.off()

# Turn the OPC OFF
print ("Turning off the OPC")
print ("OFF: {0}".format(opc.off()))
