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

        # Let's print out the histogram nicely
        print ("\tBin 0:\t{0}".format(hist['Bin 0']))
        print ("\tBin 1:\t{0}".format(hist['Bin 1']))
        print ("\tBin 2:\t{0}".format(hist['Bin 2']))
        print ("\tBin 3:\t{0}".format(hist['Bin 3']))
        print ("\tBin 4:\t{0}".format(hist['Bin 4']))
        print ("\tBin 5:\t{0}".format(hist['Bin 5']))
        print ("\tBin 6:\t{0}".format(hist['Bin 6']))
        print ("\tBin 7:\t{0}".format(hist['Bin 7']))
        print ("\tBin 8:\t{0}".format(hist['Bin 8']))
        print ("\tBin 9:\t{0}".format(hist['Bin 9']))
        print ("\tBin 10:\t{0}".format(hist['Bin 10']))
        print ("\tBin 11:\t{0}".format(hist['Bin 11']))
        print ("\tBin 12:\t{0}".format(hist['Bin 12']))
        print ("\tBin 13:\t{0}".format(hist['Bin 13']))
        print ("\tBin 14:\t{0}".format(hist['Bin 14']))
        print ("\tBin 15:\t{0}".format(hist['Bin 15']))

        print ("\tTemp:\t{0}".format(hist['Temperature']))
        print ("\tPressure:\t{0}".format(hist['Pressure']))

        print ("\tPM1:\t{0}".format(hist['PM1']))
        print ("\tPM2.5:\t{0}".format(hist['PM2.5']))
        print ("\tPM10:\t{0}".format(hist['PM10']))

        print ("\tMToF Bin 1:\t{0}".format(hist['Bin1 MToF']))
        print ("\tMToF Bin 3:\t{0}".format(hist['Bin3 MToF ']))
        print ("\tMToF Bin 5:\t{0}".format(hist['Bin5 MToF']))
        print ("\tMToF Bin 7:\t{0}".format(hist['Bin7 MToF']))

        print ("\tPeriod Count:\t{0}".format(hist['Period Count']))
        print ("\tChecksum:\t{0}".format(hist['Checksum']))

        sleep(10)
        i += 1
except KeyboardInterrupt:
    opc.off()

# Turn the OPC OFF
print ("Turning off the OPC")
print ("OFF: {0}".format(opc.off()))
