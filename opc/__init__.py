from pkg_resources import get_distribution
from .exceptions import SPIError

from time import sleep
import spidev
import struct

__all__ = ['OPCN2']
__version__ = get_distribution('opc').version

class OPCN2:
    '''
        Class instance for the Alphasense Optical Particle Counter (OPC-N2)
    '''
    def __init__(self, spi_connection, debug = False):
        self.cnxn = spi_connection
        self.debug = debug
        self.firmware = None

        # Check to make sure the connection is a valid SpiDev instance
        if not isinstance(spi_connection, spidev.SpiDev):
            raise SPIError("This is not an instance of SpiDev.")

    def __combine_bytes(self, LSB, MSB):
        ''' returns combined bytes '''
        return (MSB << 8) | LSB

    def __calculate_float(self, byte_array):
        ''' returns a float from array of 4 bytes '''
        return struct.unpack('>f', bytes(reversed(byte_array)))[0]

    def __calculate_mtof(self, mtof):
        '''
            calculates the average amount of time that particles in
            this bin took to cross the path of the OPC units -> [micro-seconds]
        '''
        return mtof / 3.0

    def __calculate_temp(self, vals):
        ''' calculates the temperature in degrees celcius '''
        if len(vals) < 4:
            return None

        return ((vals[3] << 24) | (vals[2] << 16) | (vals[1] << 8) | vals[0]) / 10.0

    def __calculate_pressure(self, vals):
        ''' calculate the pressure in pascals '''
        if len(vals) < 4:
            return None

        return ((vals[3] << 24) | (vals[2] << 16) | (vals[1] << 8) | vals[0])

    def __calculate_period(self, vals):
        ''' calculate the sampling period in seconds '''
        if len(vals) < 4:
            return None

        return ((vals[3] << 24) | (vals[2] << 16) | (vals[1] << 8) | vals[0]) / 12e6

    def on(self):
        ''' turns ON the OPC (fan and laser) '''
        b1 = self.cnxn.xfer([0x03])[0]          # send the command byte
        sleep(9e-3)                             # sleep for 9 ms
        b2, b3 = self.cnxn.xfer([0x00, 0x01])   # send the following two bytes

        return True if b1 == 0xF3 and b2 == 0x03 else False

    def off(self):
        ''' turns OFF the OPC (fan and laser)'''
        b1 = self.cnxn.xfer([0x03])[0]          # send the command byte
        sleep(9e-3)                             # sleep for 9 ms
        b2 = self.cnxn.xfer([0x01])[0]          # send the following two bytes

        return True if b1 == 0xF3 and b2 == 0x03 else False

    def check_status(self):
        ''' returns the status of the OPC-N2 as a boolean '''
        b = self.cnxn.xfer([0xCF])[0]           # send the command byte

        return True if b == 0xF3 else False

    def read_info_string(self):
        ''' returns the firmware information for the OPC as a string '''

        infostring = []
        command = 0x3F

        # Send the command byte and sleep for 9 ms
        self.cnxn.xfer([command])
        sleep(9e-3)

        # Read the info string by sending 60 empty bytes
        for i in range(60):
            resp = self.cnxn.xfer([0x00])[0]
            infostring.append(chr(resp))

        # Set the Firmware variable
        self.firmware = ''.join(infostring[23:27])

        return ''.join(infostring)

    def read_config_variables(self):
        '''
        reads the configuration variables and returns them as a dictionary

        Byte List:
         - [0:30]   -> LSB/MSB for 16 bit unsigned ints (bin boundaries)
         - [30:32]  -> spare bytes
         - [32:96]  -> 4 bytes for each bin particle volume (4 byte real number)
         - [96:160] -> 4 bytes for each bin particle density (4 byte real number)
         - [160:224]-> 4 bytes for each bin sample volume weighting
         - [224:228]-> 4 byte real number Gain Scaling Coef. (GSC)
         - [228:232]-> 4 byte real number sample flow rate
         - [232]    -> 1 byte Laser DAC
         - [233]    -> 1 byte Fan DAC
         - [234:256]-> spare bytes
        '''
        config  = []
        data    = {}
        command = 0x3C

        # Send the command byte and sleep for 10 ms
        self.cnxn.xfer([command])
        sleep(10e-3)

        # Read the config variables by sending 256 empty bytes
        for i in range(256):
            resp = self.cnxn.xfer([0x00])[0]
            config.append(resp)

        # Add the bin bounds to the dictionary of data
        for i in range(0, 15):
            data["Bin Boundary {0}".format(i)] = self.__combine_bytes(config[2*i], config[2*i + 1])

        # Add the Bin Particle Volumes (BVP)
        for i in range(0, 16):
            data["BPV {0}".format(i)] = self.__calculate_float(config[4*i + 32:4*i + 36])

        # Add the Bin Particle Densities (BPD)
        for i in range(0, 16):
            data["BPD {0}".format(i)] = self.__calculate_float(config[4*i + 96:4*i + 100])

        # Add the Bin Sample Volume Weight (BSVW)
        for i in range(0, 16):
            data["BSVW {0}".format(i)] = self.__calculate_float(config[4*i + 160: 4*i + 164])

        # Add the Gain Scaling Coefficient (GSC) and sample flow rate (SFR)
        data["GSC"] = self.__calculate_float(config[224:228])
        data["SFR"] = self.__calculate_float(config[228:232])

        # Add laser dac (LDAC) and Fan dac (FanDAC)
        data["LDAC"] = config[232]
        data["FanDAC"] = config[233]

        # Don't know what to do about all of the bytes yet!
        if self.debug:
            count = 0
            print ("Debugging the Config Variables")
            for each in config:
                print ("\t{0}: {1}".format(count, each))
                count += 1

        return data

    def write_config_variables(self):
        ''' Writes the configuration variables to memory '''
        return

    def read_histogram(self):
        ''' Reads and resets the histogram bins '''
        resp = []
        data = {}

        # command byte
        command = 0x30

        # Send the command byte
        self.cnxn.xfer([command])

        # Wait 10 ms
        sleep(10e-3)

        # read the histogram
        for i in range(62):
            r = self.cnxn.xfer([0x00])[0]
            resp.append(r)

        # convert to real things and store in dictionary!
        data['Bin 0']           = self.__combine_bytes(resp[0], resp[1])
        data['Bin 1']           = self.__combine_bytes(resp[2], resp[3])
        data['Bin 2']           = self.__combine_bytes(resp[4], resp[5])
        data['Bin 3']           = self.__combine_bytes(resp[6], resp[7])
        data['Bin 4']           = self.__combine_bytes(resp[8], resp[9])
        data['Bin 5']           = self.__combine_bytes(resp[10], resp[11])
        data['Bin 6']           = self.__combine_bytes(resp[12], resp[13])
        data['Bin 7']           = self.__combine_bytes(resp[14], resp[15])
        data['Bin 8']           = self.__combine_bytes(resp[16], resp[17])
        data['Bin 9']           = self.__combine_bytes(resp[18], resp[19])
        data['Bin 10']          = self.__combine_bytes(resp[20], resp[21])
        data['Bin 11']          = self.__combine_bytes(resp[22], resp[23])
        data['Bin 12']          = self.__combine_bytes(resp[24], resp[25])
        data['Bin 13']          = self.__combine_bytes(resp[26], resp[27])
        data['Bin 14']          = self.__combine_bytes(resp[28], resp[29])
        data['Bin 15']          = self.__combine_bytes(resp[30], resp[31])
        data['Bin1 MToF']       = self.__calculate_mtof(resp[32])
        data['Bin3 MToF']       = self.__calculate_mtof(resp[33])
        data['Bin5 MToF']       = self.__calculate_mtof(resp[34])
        data['Bin7 MToF']       = self.__calculate_mtof(resp[35])
        data['Temperature']     = self.__calculate_temp(resp[36:40])
        data['Pressure']        = self.__calculate_pressure(resp[40:44])
        data['Period Count']    = self.__calculate_period(resp[44:48])
        data['Checksum']        = self.__combine_bytes(resp[48], resp[49])
        data['PM1']             = self.__calculate_float(resp[50:54])
        data['PM2.5']           = self.__calculate_float(resp[54:58])
        data['PM10']            = self.__calculate_float(resp[58:])

        # Calculate the sum of the histogram bins
        data['histogram sum'] = data['Bin 0'] + data['Bin 1'] + data['Bin 2']   + \
                data['Bin 3'] + data['Bin 4'] + data['Bin 5'] + data['Bin 6']   + \
                data['Bin 7'] + data['Bin 8'] + data['Bin 9'] + data['Bin 10']  + \
                data['Bin 11'] + data['Bin 12'] + data['Bin 13'] + data['Bin 14'] + \
                data['Bin 15']

        # If debug is True, print out the bytes!
        if self.debug:
            count = 0
            print ("Debugging the Histogram")
            for each in resp:
                print ("\t{0}: {1}".format(count, each))
                count += 1

        return data

    def save_config_variables(self):
        ''' Save the config variables in non-volatile memory '''
        command = 0x43
        byte_list = [0x3F, 0x3C, 0x3F, 0x3C, 0x43]
        success = [0xF3, 0x43, 0x3F, 0x3C, 0x3F, 0x3C]
        resp = []

        # Send the command byte and then wait for 10 ms
        r = self.cnxn.xfer([command])[0]
        sleep(10e-3)

        # append the response of the command byte to the List
        resp.append(r)

        # Send the rest of the config bytes
        for each in byte_list:
            r = self.cnxn.xfer([each])[0]
            resp.append(r)

        return True if resp == success else False

    def enter_bootloader_mode(self):
        ''' Enter bootloader mode '''
        command = 0x41

        return True if self.cnxn.xfer(command)[0] == 0xF3 else False

    def set_fan_power(self, value):
        ''' Sets the fan power as a value between 0-255 '''
        command = 0x42

        # Check to make sure the value is a single byte
        if value >= 256:
            raise ValueError("Try a single byte (0-255).")

        # Send the command byte and wait 10 ms
        a = self.cnxn.xfer([command])[0]
        sleep(10e-3)

        # Send the next two bytes
        b = self.cnxn.xfer([0x00])[0]
        c = self.cnxn.xfer([value])[0]

        return True if a == 0xF3 and b == 0x42 and c == 0x00 else False

    def set_laser_power(self, value):
        ''' Sets the laser power as a value between 0-255'''
        command = 0x42

        # Check to make sure the value is a single byte
        if value >= 256:
            raise ValueError("Try a single byte (0-255).")

        # Send the command byte and wait 10 ms
        a = self.cnxn.xfer([command])[0]
        sleep(10e-3)

        # Send the next two bytes
        b = self.cnxn.xfer([0x01])[0]
        c = self.cnxn.xfer([value])[0]

        return True if a == 0xF3 and b == 0x42 and c == 0x01 else False

    def laser_on(self):
        ''' Turn on the laser only '''
        command = 0x03
        byte    = 0x02

        # Send the command byte, wait 10ms, and then send the byte
        a = self.cnxn.xfer([command])[0]
        sleep(10e-3)
        b = self.cnxn.xfer([byte])[0]

        return True if a == 0xF3 and b == 0x03 else False

    def laser_off(self):
        ''' Turn off the laser only '''
        command = 0x03
        byte    = 0x03

        # Send the command byte, wait 10ms, and then send the byte
        a = self.cnxn.xfer([command])[0]
        sleep(10e-3)
        b = self.cnxn.xfer([byte])[0]

        return True if a == 0xF3 and b == 0x03 else False

    def fan_on(self):
        ''' Turn on the fan only '''
        command = 0x03
        byte    = 0x04

        # Send the command byte, wait 10ms, and then send the byte
        a = self.cnxn.xfer([command])[0]
        sleep(10e-3)
        b = self.cnxn.xfer([byte])[0]

        return True if a == 0xF3 and b == 0x03 else False

    def fan_off(self):
        ''' Turn off the fan only '''
        command = 0x03
        byte    = 0x05

        # Send the command byte, wait 10ms, and then send the byte
        a = self.cnxn.xfer([command])[0]
        sleep(10e-3)
        b = self.cnxn.xfer([byte])[0]

        return True if a == 0xF3 and b == 0x03 else False

    def __repr__(self):
        return "Alphasense OPC: Firmware v{0}".format(self.firmware)
