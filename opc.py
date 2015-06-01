'''
    Owned and written by David H Hagan
    May 31, 2015

    This script runs the Alphasense OPC-N2
'''

from time import sleep
import spidev

class OPCN2:
    '''
        Class instance for the Alphasense Optical Particle Counter (OPC-N2)
    '''
    def __init__(self, spi_connection):
        self.cnxn = spi_connection

        # Check to make sure the connection is a valid SpiDev instance
        if not isinstance(spi_connection, spidev.SpiDev):
            print ("Not an instance of SpiDev")

        self.firmware = None

    def __calculateHist(MSB, LSB):
        ''' Internal function to calculate the histogram bin from the MSB and LSB '''
        return (MSB << 8) | LSB

    def __calculateMToF(mtof):
        '''
            Internal function to calculate the average amount of time that particles in
            this bin took to cross the path of the OPC units -> [micro-seconds]
        '''
        return mtof / 3.0

    def __calculateTemp(vals):
        ''' Calculates the temperature in degrees celcius '''
        return ((vals[3] << 24) | (vals[2] << 16) | (vals[1] << 8) | vals[0]) / 10.0

    def __calculatePressure(vals):
        ''' Calculate the pressure in Pascals '''
        return ((vals[3] << 24 | (vals[2] << 16) | (vals[1] << 8) | vals[0])

    def __calculatePeriod(vals):
        ''' Calculate the sampling period in seconds '''
        return ((vals[3] << 24) | (vals[2] << 16) | (vals[1] << 8) | vals[0]) / 12e6

    def __calculateChecksum(MSB, LSB):
        ''' Calculate the checksum '''
        return (MSB << 8) | LSB

    def __calculatePM(vals):
        ''' Calculate the PM value '''
        return True

    def on(self):
        ''' Turns ON the OPC '''
        b1 = self.cnxn.xfer([0x03])[0]
        sleep(9e-3)
        b2, b3 = self.cnxn.xfer([0x00, 0x01])

        # Check the outgoing bytes
        return True if b1 == 0xF3 and b2 == 0x03 else False

    def off(self):
        ''' Turns OFF the OPC '''
        b1 = self.cnxn.xfer([0x03])[0]
        sleep(9e-3)
        b2 = self.cnxn.xfer([0x01])[0]

        return True if b1 == 0xF3 and b2 == 0x03 else False

    def checkStatus(self):
        ''' Check the status of the OPC-N2 '''
        b = self.cnxn.xfer([0xCF])[0]

        return True if b == 0xF3 else False

    def readInfoString(self):
        ''' Read information string and store useful things places '''
        # Set up a list for the string to be stored in
        infostring = []

        # Read the info string
        command = 0x3F

        # Send the command byte
        self.cnxn.xfer([command])

        # Wait a bit
        sleep(9e-3)

        # Read the info string
        for i in range(60):
            resp = self.cnxn.xfer([0x00])[0]
            infostring.append(chr(resp))


        # Set the Firmware variable
        self.firmware = ''.join(infostring[23:27])

        return ''.join(infostring)

    def readConfigVariables(self):
        ''' Reads the configuration variables and returns them as a dictionary '''
        return

    def readHistogram(self):
        ''' Reads and resets the histogram bins '''
        # Set up a list to append histogram data to
        resp = []

        # command byte
        command = 0x30

        # Initialize a dictionary that will hold all the data
        data = {}

        # Send the command byte
        self.cnxn.xfer([command])

        # Wait a sec..
        sleep(10e-3)

        # read the histogram
        for i in range(62):
            r = self.cnxn.xfer([0x00])[0]
            resp.append(r)

        # convert to real things and store in dictionary!
        data['Bin 0']           = self.__calculateHist(resp[1], resp[0])
        data['Bin 1']           = self.__calculateHist(resp[3], resp[2])
        data['Bin 2']           = self.__calculateHist(resp[5], resp[4])
        data['Bin 3']           = self.__calculateHist(resp[7], resp[6])
        data['Bin 4']           = self.__calculateHist(resp[9], resp[8])
        data['Bin 5']           = self.__calculateHist(resp[11], resp[10])
        data['Bin 6']           = self.__calculateHist(resp[13], resp[12])
        data['Bin 7']           = self.__calculateHist(resp[15], resp[14])
        data['Bin 8']           = self.__calculateHist(resp[17], resp[16])
        data['Bin 9']           = self.__calculateHist(resp[19], resp[18])
        data['Bin 10']          = self.__calculateHist(resp[21], resp[20])
        data['Bin 11']          = self.__calculateHist(resp[23], resp[22])
        data['Bin 12']          = self.__calculateHist(resp[25], resp[24])
        data['Bin 13']          = self.__calculateHist(resp[27], resp[26])
        data['Bin 14']          = self.__calculateHist(resp[29], resp[28])
        data['Bin 15']          = self.__calculateHist(resp[31], resp[30])
        data['Bin1 MToF']       = self.__calculateMToF(resp[32])
        data['Bin3 MToF']       = self.__calculateMToF(resp[33])
        data['Bin5 MToF']       = self.__calculateMToF(resp[34])
        data['Bin7 MToF']       = self.__calculateMToF(resp[35])
        data['Temperature']     = self.__calculateTemp(resp[36:39])
        data['Pressure']        = self.__calculatePressure(resp[40:43])
        data['Period Count']    = self.__calculatePeriod(resp[44:47])
        data['Checksum']        = self.__calculateChecksum(resp[49], resp[48])
        data['PM1']             = self.__calculatePM(resp[50:53])
        data['PM2.5']           = self.__calculatePM(resp[54:57])
        data['PM10']            = self.__calculatePM(resp[58:61])

        return data

    def __repr__(self):
        return "Alphasense OPC: Firmware v{0}".format(self.firmware)
