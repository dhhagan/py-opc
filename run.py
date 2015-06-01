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
opc.on()

sleep(1)

# Read the info
print ("Reading the information string")
print (opc.readInfoString())

sleep(1)

# Read the histogram
print ("Reading the histogram")
hist = opc.readHistogram()
for key, value in hist:
    print ("Key: {0} -> {1}".format(key, value))

# Turn the OPC OFF
print ("Turning off the OPC")
opc.off()
