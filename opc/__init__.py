from pkg_resources import get_distribution
from .exceptions import FirmwareVersionError, SpiConnectionError
from .decorators import requires_firmware
from .lookup_table import OPC_LOOKUP

from time import sleep
import struct
import warnings
import re

from .exceptions import firmware_error_msg


__all__ = ['OPCN2', 'OPCN1']
__version__ = get_distribution('py-opc').version

class OPC(object):
    """Generic class for any Alphasense OPC. Provides the common methods and calculations
    for each OPC.

    :param spi_connection: spidev.SpiDev or usbiss.USBISS connection
    :param debug: Set true to print data to console while running
    :param model: Model number of the OPC ('N1' or 'N2') set by the parent class

    :raises: opc.exceptions.SpiConnectionError

    :type spi_connection: spidev.SpiDev or usbiss.USBISS
    :type debug: boolean
    :type model: string

    :rtype: opc.OPC

    :Example:

     >>> import opc
     >>> import spidev
     >>>
     >>> spi = spidev.SpiDev()
     >>> spi.open(0, 0)
     >>> spi.mode = 1
     >>> spi.max_speed_hz = 500000
     >>>
     >>> alpha = opc.OPC(spi)
    """
    def __init__(self, spi_connection, **kwargs):
        self.cnxn       = spi_connection
        self.debug      = kwargs.get('debug', False)
        self.firmware   = {'major': None, 'minor': None, 'version': None}
        self.model      = kwargs.get('model', 'N2')

        # Check to make sure the connection has the xfer attribute
        msg = ("The SPI connection must be a valid SPI master with "
               "transfer function 'xfer'")
        assert hasattr(spi_connection, 'xfer'), msg
        assert self.cnxn.mode == 1, "SPI mode must be 1"
        # Set the firmware version upon initialization
        try:
            self.firmware['version']    = int(re.findall("\d{3}", self.read_info_string())[-1])
        except:
            # Try again for the early (v7) firmwares
            try:
                self.firmware['version'] = int(re.findall("\d{1}", self.read_info_string())[-1])
            except:
                msg =   """
                        Your firmware version could not be automatically detected. This is usually caused
                        by a bad wiring or poor power supply. If niether of these are likely candidates, please
                        open an issue on the GitHub repository at https://github.com/dhhagan/py-opc/issues/new
                        """
                raise FirmwareVersionError(msg)

        # If firmware version is >= 18, set the major and minor versions..
        try:
            if self.firmware['version'] >= 18.:
                self.read_firmware()
            else:
                self.firmware['major'] = self.firmware['version']
        except:
            pass

    def _16bit_unsigned(self, LSB, MSB):
        """Returns the combined LSB and MSB

        :param LSB: Least Significant Byte
        :param MSB: Most Significant Byte

        :type LSB: byte
        :type MSB: byte

        :rtype: 16-bit unsigned int
        """
        return (MSB << 8) | LSB

    def _calculate_float(self, byte_array):
        """Returns an IEEE 754 float from an array of 4 bytes

        :param byte_array: Expects an array of 4 bytes

        :type byte_array: array

        :rtype: float
        """
        if len(byte_array) != 4:
            return None

        return struct.unpack('f', struct.pack('4B', *byte_array))[0]

    def _calculate_mtof(self, mtof):
        """Returns the average amount of time that particles in a bin
        took to cross the path of the laser [units -> microseconds]

        :param mtof: mass time-of-flight

        :type mtof: float

        :rtype: float
        """
        return mtof / 3.0

    def _calculate_temp(self, vals):
        """Calculates the temperature in degrees celcius

        :param vals: array of bytes

        :type vals: array

        :rtype: float
        """
        if len(vals) < 4:
            return None

        return ((vals[3] << 24) | (vals[2] << 16) | (vals[1] << 8) | vals[0]) / 10.0

    def _calculate_pressure(self, vals):
        """Calculates the pressure in pascals

        :param vals: array of bytes

        :type vals: array

        :rtype: float
        """
        if len(vals) < 4:
            return None

        return ((vals[3] << 24) | (vals[2] << 16) | (vals[1] << 8) | vals[0])

    def _calculate_period(self, vals):
        ''' calculate the sampling period in seconds '''
        if len(vals) < 4:
            return None

        if self.firmware < 16:
            return ((vals[3] << 24) | (vals[2] << 16) | (vals[1] << 8) | vals[0]) / 12e6
        else:
            return self._calculate_float(vals)

    def lookup_bin_boundary(self, adc_value):
        """Looks up the bin boundary value in microns based on the lookup table provided by Alphasense.

            :param adc_value: ADC Value (0 - 4095)

            :type adc_value: int

            :rtype: float
        """
        if adc_value < 0:
            adc_value = 0

        if adc_value > 4095:
            adc_value = 4095

        return OPC_LOOKUP[adc_value]

    def calculate_bin_boundary(self, bb):
        """Calculate the adc value that corresponds to a specific bin boundary diameter in microns.

            :param bb: Bin Boundary in microns

            :type bb: float

            :rtype: int
        """

        return min(enumerate(OPC_LOOKUP), key = lambda x: abs(x[1] - bb))[0]

    def read_info_string(self):
        """Reads the information string for the OPC

        :rtype: string

        :Example:

        >>> alpha.read_info_string()
        'OPC-N2 FirmwareVer=OPC-018.2....................BD'
        """
        infostring = []

        # Send the command byte and sleep for 9 ms
        self.cnxn.xfer([0x3F])
        sleep(9e-3)

        # Read the info string by sending 60 empty bytes
        for i in range(60):
            resp = self.cnxn.xfer([0x00])[0]
            infostring.append(chr(resp))

        return ''.join(infostring)

    def ping(self):
        """Checks the connection between the Raspberry Pi and the OPC

        :rtype: Boolean
        """
        b = self.cnxn.xfer([0xCF])[0]           # send the command byte

        return True if b == 0xF3 else False

    def __repr__(self):
        return "Alphasense OPC-{}v{}".format(self.model, self.firmware['version'])

class OPCN2(OPC):
    """Create an instance of the Alphasene OPC-N2. Currently supported by firmware
    versions 14-18. opc.OPCN2 inherits from the opc.OPC parent class.

    :param spi_connection: The spidev instance for the SPI connection.

    :type spi_connection: spidev.SpiDev

    :rtype: opc.OPCN2

    :raises: opc.exceptions.FirmwareVersionError

    :Example:

    >>> alpha = opc.OPCN2(spi)
    >>> alpha
    Alphasense OPC-N2v18.2
    """
    def __init__(self, spi_connection, **kwargs):
        super(OPCN2, self).__init__(spi_connection, model = 'N2', **kwargs)

        firmware_min = 14.   # Minimum firmware version supported
        firmware_max = 18.   # Maximum firmware version supported

        if self.firmware['major'] < firmware_min or self.firmware['major'] > firmware_max:
            raise FirmwareVersionError("Your firmware is not yet supported. Only versions 14-18 are currently supported.")

    def on(self):
        """Turn ON the OPC (fan and laser)

        :rtype: boolean

        :Example:

        >>> alpha.on()
        True
        """
        b1 = self.cnxn.xfer([0x03])[0]          # send the command byte
        sleep(9e-3)                             # sleep for 9 ms
        b2, b3 = self.cnxn.xfer([0x00, 0x01])   # send the following byte

        return True if b1 == 0xF3 and b2 == 0x03 else False

    def off(self):
        """Turn OFF the OPC (fan and laser)

        :rtype: boolean

        :Example:

        >>> alpha.off()
        True
        """
        b1 = self.cnxn.xfer([0x03])[0]          # send the command byte
        sleep(9e-3)                             # sleep for 9 ms
        b2 = self.cnxn.xfer([0x01])[0]          # send the following two bytes

        return True if b1 == 0xF3 and b2 == 0x03 else False

    def config(self):
        """Read the configuration variables and returns them as a dictionary

        :rtype: dictionary

        :Example:

        >>> alpha.config()
        {
            'BPD 13': 1.6499,
            'BPD 12': 1.6499,
            'BPD 11': 1.6499,
            'BPD 10': 1.6499,
            'BPD 15': 1.6499,
            'BPD 14': 1.6499,
            'BSVW 15': 1.0,
            ...
        }
        """
        config  = []
        data    = {}

        # Send the command byte and sleep for 10 ms
        self.cnxn.xfer([0x3C])
        sleep(10e-3)

        # Read the config variables by sending 256 empty bytes
        for i in range(256):
            resp = self.cnxn.xfer([0x00])[0]
            config.append(resp)

        # Add the bin bounds to the dictionary of data [bytes 0-29]
        for i in range(0, 15):
            data["Bin Boundary {0}".format(i)] = self._16bit_unsigned(config[2*i], config[2*i + 1])

        # Add the Bin Particle Volumes (BPV) [bytes 32-95]
        for i in range(0, 16):
            data["BPV {0}".format(i)] = self._calculate_float(config[4*i + 32:4*i + 36])

        # Add the Bin Particle Densities (BPD) [bytes 96-159]
        for i in range(0, 16):
            data["BPD {0}".format(i)] = self._calculate_float(config[4*i + 96:4*i + 100])

        # Add the Bin Sample Volume Weight (BSVW) [bytes 160-223]
        for i in range(0, 16):
            data["BSVW {0}".format(i)] = self._calculate_float(config[4*i + 160: 4*i + 164])

        # Add the Gain Scaling Coefficient (GSC) and sample flow rate (SFR)
        data["GSC"] = self._calculate_float(config[224:228])
        data["SFR"] = self._calculate_float(config[228:232])

        # Add laser dac (LDAC) and Fan dac (FanDAC)
        data["LaserDAC"]    = config[232]
        data["FanDAC"]      = config[233]

        # If past firmware 15, add other things
        if self.firmware['major'] > 15.:
            data['TOF_SFR'] = config[234]

        return data

    @requires_firmware(18.)
    def config2(self):
        """Read the second set of configuration variables and return as a dictionary.

        **NOTE: This method is supported by firmware v18+.**

        :rtype: dictionary

        :Example:

        >>> a.config2()
        {
            'AMFanOnIdle': 0,
            'AMIdleIntervalCount': 0,
            'AMMaxDataArraysInFile': 61798,
            'AMSamplingInterval': 1,
            'AMOnlySavePMData': 0,
            'AMLaserOnIdle': 0
        }
        """
        config  = []
        data    = {}

        # Send the command byte and sleep for 10 ms
        self.cnxn.xfer([0x3D])
        sleep(10e-3)

        # Read the config variables by sending 256 empty bytes
        for i in range(9):
            resp = self.cnxn.xfer([0x00])[0]
            config.append(resp)

        data["AMSamplingInterval"]      = self._16bit_unsigned(config[0], config[1])
        data["AMIdleIntervalCount"]     = self._16bit_unsigned(config[2], config[3])
        data['AMFanOnIdle']             = config[4]
        data['AMLaserOnIdle']           = config[5]
        data['AMMaxDataArraysInFile']   = self._16bit_unsigned(config[6], config[7])
        data['AMOnlySavePMData']        = config[8]

        return data

    def write_config_variables(self, config_vars):
        """ Write configuration variables to non-volatile memory.

        **NOTE: This method is currently a placeholder and is not implemented.**

        :param config_vars: dictionary containing the configuration variables

        :type config_vars: dictionary
        """

        warnings.warn("This method has not yet been implemented.")

        return

    @requires_firmware(18.)
    def write_config_variables2(self, config_vars):
        """ Write configuration variables 2 to non-volatile memory.

        **NOTE: This method is currently a placeholder and is not implemented.**
        **NOTE: This method is supported by firmware v18+.**

        :param config_vars: dictionary containing the configuration variables

        :type config_vars: dictionary
        """

        warnings.warn("This method has not yet been implemented.")

        return

    def histogram(self, number_concentration = True):
        """Read and reset the histogram. As of v1.3.0, histogram
        values are reported in particle number concentration (#/cc) by default.

        :param number_concentration: If true, histogram bins are reported in number concentration vs. raw values.

        :type number_concentration: boolean

        :rtype: dictionary

        :Example:

        >>> alpha.histogram()
        {
            'Temperature': None,
            'Pressure': None,
            'Bin 0': 0,
            'Bin 1': 0,
            'Bin 2': 0,
            ...
            'Bin 15': 0,
            'SFR': 3.700,
            'Bin1MToF': 0,
            'Bin3MToF': 0,
            'Bin5MToF': 0,
            'Bin7MToF': 0,
            'PM1': 0.0,
            'PM2.5': 0.0,
            'PM10': 0.0,
            'Sampling Period': 2.345,
            'Checksum': 0
        }
        """
        resp = []
        data = {}

        # Send the command byte
        self.cnxn.xfer([0x30])

        # Wait 10 ms
        sleep(10e-3)

        # read the histogram
        for i in range(62):
            r = self.cnxn.xfer([0x00])[0]
            resp.append(r)

        # convert to real things and store in dictionary!
        data['Bin 0']           = self._16bit_unsigned(resp[0], resp[1])
        data['Bin 1']           = self._16bit_unsigned(resp[2], resp[3])
        data['Bin 2']           = self._16bit_unsigned(resp[4], resp[5])
        data['Bin 3']           = self._16bit_unsigned(resp[6], resp[7])
        data['Bin 4']           = self._16bit_unsigned(resp[8], resp[9])
        data['Bin 5']           = self._16bit_unsigned(resp[10], resp[11])
        data['Bin 6']           = self._16bit_unsigned(resp[12], resp[13])
        data['Bin 7']           = self._16bit_unsigned(resp[14], resp[15])
        data['Bin 8']           = self._16bit_unsigned(resp[16], resp[17])
        data['Bin 9']           = self._16bit_unsigned(resp[18], resp[19])
        data['Bin 10']          = self._16bit_unsigned(resp[20], resp[21])
        data['Bin 11']          = self._16bit_unsigned(resp[22], resp[23])
        data['Bin 12']          = self._16bit_unsigned(resp[24], resp[25])
        data['Bin 13']          = self._16bit_unsigned(resp[26], resp[27])
        data['Bin 14']          = self._16bit_unsigned(resp[28], resp[29])
        data['Bin 15']          = self._16bit_unsigned(resp[30], resp[31])
        data['Bin1 MToF']       = self._calculate_mtof(resp[32])
        data['Bin3 MToF']       = self._calculate_mtof(resp[33])
        data['Bin5 MToF']       = self._calculate_mtof(resp[34])
        data['Bin7 MToF']       = self._calculate_mtof(resp[35])

        # Bins associated with firmware versions 14 and 15(?)
        if self.firmware['version'] < 16.:
            data['Temperature']     = self._calculate_temp(resp[36:40])
            data['Pressure']        = self._calculate_pressure(resp[40:44])
            data['Sampling Period'] = self._calculate_period(resp[44:48])
            data['Checksum']        = self._16bit_unsigned(resp[48], resp[49])
            data['PM1']             = self._calculate_float(resp[50:54])
            data['PM2.5']           = self._calculate_float(resp[54:58])
            data['PM10']            = self._calculate_float(resp[58:])

        else:
            data['SFR']             = self._calculate_float(resp[36:40])

            # Alright, we don't know whether it is temp or pressure since it switches..
            tmp = self._calculate_pressure(resp[40:44])
            if tmp > 98000:
                data['Temperature'] = None
                data['Pressure']    = tmp
            else:
                tmp = self._calculate_temp(resp[40:44])
                if tmp < 500:
                    data['Temperature'] = tmp
                    data['Pressure']    = None
                else:
                    data['Temperature'] = None
                    data['Pressure']    = None

            data['Sampling Period'] = self._calculate_float(resp[44:48])
            data['Checksum']        = self._16bit_unsigned(resp[48], resp[49])
            data['PM1']             = self._calculate_float(resp[50:54])
            data['PM2.5']           = self._calculate_float(resp[54:58])
            data['PM10']            = self._calculate_float(resp[58:])

        # Calculate the sum of the histogram bins
        histogram_sum = data['Bin 0'] + data['Bin 1'] + data['Bin 2']   + \
                data['Bin 3'] + data['Bin 4'] + data['Bin 5'] + data['Bin 6']   + \
                data['Bin 7'] + data['Bin 8'] + data['Bin 9'] + data['Bin 10']  + \
                data['Bin 11'] + data['Bin 12'] + data['Bin 13'] + data['Bin 14'] + \
                data['Bin 15']

        # Check that checksum and the least significant bits of the sum of histogram bins
        # are equivilant
        if (histogram_sum & 0x0000FFFF) != data['Checksum']:
            warnings.warn("Data transfer was incomplete.")
            return None

        # If histogram is true, convert histogram values to number concentration
        if number_concentration is True:
            _conv_ = data['SFR'] * data['Sampling Period'] # Divider in units of ml (cc)

            data['Bin 0']   = data['Bin 0'] / _conv_
            data['Bin 1']   = data['Bin 1'] / _conv_
            data['Bin 2']   = data['Bin 2'] / _conv_
            data['Bin 3']   = data['Bin 3'] / _conv_
            data['Bin 4']   = data['Bin 4'] / _conv_
            data['Bin 5']   = data['Bin 5'] / _conv_
            data['Bin 6']   = data['Bin 6'] / _conv_
            data['Bin 7']   = data['Bin 7'] / _conv_
            data['Bin 8']   = data['Bin 8'] / _conv_
            data['Bin 9']   = data['Bin 9'] / _conv_
            data['Bin 10']  = data['Bin 10'] / _conv_
            data['Bin 11']  = data['Bin 11'] / _conv_
            data['Bin 12']  = data['Bin 12'] / _conv_
            data['Bin 13']  = data['Bin 13'] / _conv_
            data['Bin 14']  = data['Bin 14'] / _conv_
            data['Bin 15']  = data['Bin 15'] / _conv_

        return data

    def save_config_variables(self):
        """Save the configuration variables in non-volatile memory. This method
        should be used in conjuction with *write_config_variables*.

        :rtype: boolean

        :Example:

        >>> alpha.save_config_variables()
        True
        """
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

    def _enter_bootloader_mode(self):
        """Enter bootloader mode. Must be issued prior to writing
        configuration variables to non-volatile memory.

        :rtype: boolean

        :Example:

        >>> alpha._enter_bootloader_mode()
        True
        """

        return True if self.cnxn.xfer(0x41)[0] == 0xF3 else False

    def set_fan_power(self, power):
        """Set only the Fan power.

        :param power: Fan power value as an integer between 0-255.

        :type power: int

        :rtype: boolean

        :Example:

        >>> alpha.set_fan_power(255)
        True
        """
        # Check to make sure the value is a single byte
        if value > 255:
            raise ValueError("The fan power should be a single byte (0-255).")

        # Send the command byte and wait 10 ms
        a = self.cnxn.xfer([0x42])[0]
        sleep(10e-3)

        # Send the next two bytes
        b = self.cnxn.xfer([0x00])[0]
        c = self.cnxn.xfer([power])[0]

        return True if a == 0xF3 and b == 0x42 and c == 0x00 else False

    def set_laser_power(self, power):
        """Set the laser power only.

        :param power: Laser power as a value between 0-255.

        :type power: int

        :rtype: boolean

        :Example:

        >>> alpha.set_laser_power(230)
        True
        """

        # Check to make sure the value is a single byte
        if value > 255:
            raise ValueError("Laser Power should be a single byte (0-255).")

        # Send the command byte and wait 10 ms
        a = self.cnxn.xfer([0x42])[0]
        sleep(10e-3)

        # Send the next two bytes
        b = self.cnxn.xfer([0x01])[0]
        c = self.cnxn.xfer([power])[0]

        return True if a == 0xF3 and b == 0x42 and c == 0x01 else False

    def toggle_laser(self, state):
        """Toggle the power state of the laser.

        :param state: Boolean state of the laser

        :type state: boolean

        :rtype: boolean

        :Example:

        >>> alpha.toggle_laser(True)
        True
        """

        # Send the command byte and wait 10 ms
        a = self.cnxn.xfer([0x03])[0]

        sleep(10e-3)

        # If state is true, turn the laser ON, else OFF
        if state:
            b = self.cnxn.xfer([0x02])[0]
        else:
            b = self.cnxn.xfer([0x03])[0]

        return True if a == 0xF3 and b == 0x03 else False

    def toggle_fan(self, state):
        """Toggle the power state of the fan.

        :param state: Boolean state of the fan

        :type state: boolean

        :rtype: boolean

        :Example:

        >>> alpha.toggle_fan(False)
        True
        """

        # Send the command byte and wait 10 ms
        a = self.cnxn.xfer([0x03])[0]

        sleep(10e-3)

        # If state is true, turn the fan ON, else OFF
        if state:
            b = self.cnxn.xfer([0x04])[0]
        else:
            b = self.cnxn.xfer([0x05])[0]

        return True if a == 0xF3 and b == 0x03 else False

    @requires_firmware(18.)
    def read_pot_status(self):
        """Read the status of the digital pot. Firmware v18+ only.
        The return value is a dictionary containing the following as
        unsigned 8-bit integers: FanON, LaserON, FanDACVal, LaserDACVal.

        :rtype: dict

        :Example:

        >>> alpha.read_pot_status()
        {
            'LaserDACVal': 230,
            'FanDACVal': 255,
            'FanON': 0,
            'LaserON': 0
        }
        """
        # Send the command byte and wait 10 ms
        a = self.cnxn.xfer([0x13])[0]

        sleep(10e-3)

        # Build an array of the results
        res = []
        for i in range(4):
            res.append(self.cnxn.xfer([0x00])[0])

        return {
            'FanON':        res[0],
            'LaserON':      res[1],
            'FanDACVal':    res[2],
            'LaserDACVal':  res[3]
            }

    @requires_firmware(18.)
    def sn(self):
        """Read the Serial Number string. This method is only available on OPC-N2
        firmware versions 18+.

        :rtype: string

        :Example:

        >>> alpha.sn()
        'OPC-N2 123456789'
        """
        string = []

        # Send the command byte and sleep for 9 ms
        self.cnxn.xfer([0x10])
        sleep(9e-3)

        # Read the info string by sending 60 empty bytes
        for i in range(60):
            resp = self.cnxn.xfer([0x00])[0]
            string.append(chr(resp))

        return ''.join(string)

    @requires_firmware(18.)
    def write_sn(self):
        """Write the Serial Number string. This method is available for Firmware versions 18+.

        **NOTE: This method is currently a placeholder and is not implemented.**

        :param sn: string containing the serial number to write

        :type sn: string
        """

        return

    @requires_firmware(18.)
    def read_firmware(self):
        """Read the firmware version of the OPC-N2. Firmware v18+ only.

        :rtype: dict

        :Example:

        >>> alpha.read_firmware()
        {
            'major': 18,
            'minor': 2,
            'version': 18.2
        }
        """
        # Send the command byte and sleep for 9 ms
        self.cnxn.xfer([0x12])
        sleep(10e-3)

        self.firmware['major'] = self.cnxn.xfer([0x00])[0]
        self.firmware['minor'] = self.cnxn.xfer([0x00])[0]

        # Build the firmware version
        self.firmware['version'] = float('{}.{}'.format(self.firmware['major'], self.firmware['minor']))

        return self.firmware

    @requires_firmware(18.)
    def pm(self):
        """Read the PM data and reset the histogram

        **NOTE: This method is supported by firmware v18+.**

        :rtype: dictionary

        :Example:

        >>> alpha.pm()
        {
            'PM1': 0.12,
            'PM2.5': 0.24,
            'PM10': 1.42
        }
        """

        resp = []
        data = {}

        # Send the command byte
        self.cnxn.xfer([0x32])

        # Wait 10 ms
        sleep(10e-3)

        # read the histogram
        for i in range(12):
            r = self.cnxn.xfer([0x00])[0]
            resp.append(r)

        # convert to real things and store in dictionary!
        data['PM1']     = self._calculate_float(resp[0:4])
        data['PM2.5']   = self._calculate_float(resp[4:8])
        data['PM10']    = self._calculate_float(resp[8:])

        return data

class OPCN1(OPC):
    """Create an instance of the Alphasene OPC-N1. opc.OPCN1 inherits from
    the opc.OPC parent class.

    :param spi_connection: The spidev instance for the SPI connection.

    :type spi_connection: spidev.SpiDev

    :rtype: opc.OPCN1

    :raises: FirmwareVersionError
    """
    def __init(self, spi_connection, **kwargs):
        super(OPCN1, self).__init__(spi_connection, model = 'N1', **kwargs)

    def on(self):
        """Turn ON the OPC (fan and laser)

        :returns: boolean success state
        """
        b1 = self.cnxn.xfer([0x0C])[0]          # send the command byte
        sleep(9e-3)                             # sleep for 9 ms

        return True if b1 == 0xF3 else False

    def off(self):
        """Turn OFF the OPC (fan and laser)

        :returns: boolean success state
        """
        b1 = self.cnxn.xfer([0x03])[0]          # send the command byte
        sleep(9e-3)                             # sleep for 9 ms

        return True if b1 == 0xF3 else False

    def read_gsc_sfr(self):
        """Read the gain-scaling-coefficient and sample flow rate.

        :returns: dictionary containing GSC and SFR
        """
        config  = []
        data    = {}

        # Send the command byte and sleep for 10 ms
        self.cnxn.xfer([0x33])
        sleep(10e-3)

        # Read the config variables by sending 256 empty bytes
        for i in range(8):
            resp = self.cnxn.xfer([0x00])[0]
            config.append(resp)

        data["GSC"] = self._calculate_float(config[0:4])
        data["SFR"] = self._calculate_float(config[4:])

        return data

    def read_bin_boundaries(self):
        """Return the bin boundaries.

        :returns: dictionary with 17 bin boundaries.
        """
        config  = []
        data    = {}

        # Send the command byte and sleep for 10 ms
        self.cnxn.xfer([0x33])
        sleep(10e-3)

        # Read the config variables by sending 256 empty bytes
        for i in range(30):
            resp = self.cnxn.xfer([0x00])[0]
            config.append(resp)

        # Add the bin bounds to the dictionary of data [bytes 0-29]
        for i in range(0, 14):
            data["Bin Boundary {0}".format(i)] = self._16bit_unsigned(config[2*i], config[2*i + 1])

        return data

    def write_gsc_sfr(self):
        """Write the gsc and sfr values

        **NOTE**: This method is currently a placeholder.
        """
        return

    def read_bin_particle_density(self):
        """Read the bin particle density

        :returns: float
        """
        config = []

        # Send the command byte and sleep for 10 ms
        self.cnxn.xfer([0x33])
        sleep(10e-3)

        # Read the config variables by sending 256 empty bytes
        for i in range(4):
            resp = self.cnxn.xfer([0x00])[0]
            config.append(resp)

        bpd = self._calculate_float(config)

        return bpd

    def write_bin_particle_density(self):
        """Write the bin particle density values to memory. This method is currently a
        placeholder.

        :returns: None
        """
        return

    def read_histogram(self):
        """Read and reset the histogram. The expected return is a dictionary
        containing the counts per bin, MToF for bins 1, 3, 5, and 7, temperature,
        pressure, the sampling period, the checksum, PM1, PM2.5, and PM10.

        **NOTE:** The sampling period for the OPCN1 seems to be incorrect.

        :returns: dictionary
        """
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
        data['Bin 0']           = self._16bit_unsigned(resp[0], resp[1])
        data['Bin 1']           = self._16bit_unsigned(resp[2], resp[3])
        data['Bin 2']           = self._16bit_unsigned(resp[4], resp[5])
        data['Bin 3']           = self._16bit_unsigned(resp[6], resp[7])
        data['Bin 4']           = self._16bit_unsigned(resp[8], resp[9])
        data['Bin 5']           = self._16bit_unsigned(resp[10], resp[11])
        data['Bin 6']           = self._16bit_unsigned(resp[12], resp[13])
        data['Bin 7']           = self._16bit_unsigned(resp[14], resp[15])
        data['Bin 8']           = self._16bit_unsigned(resp[16], resp[17])
        data['Bin 9']           = self._16bit_unsigned(resp[18], resp[19])
        data['Bin 10']          = self._16bit_unsigned(resp[20], resp[21])
        data['Bin 11']          = self._16bit_unsigned(resp[22], resp[23])
        data['Bin 12']          = self._16bit_unsigned(resp[24], resp[25])
        data['Bin 13']          = self._16bit_unsigned(resp[26], resp[27])
        data['Bin 14']          = self._16bit_unsigned(resp[28], resp[29])
        data['Bin 15']          = self._16bit_unsigned(resp[30], resp[31])
        data['Bin1 MToF']       = self._calculate_mtof(resp[32])
        data['Bin3 MToF']       = self._calculate_mtof(resp[33])
        data['Bin5 MToF']       = self._calculate_mtof(resp[34])
        data['Bin7 MToF']       = self._calculate_mtof(resp[35])
        data['Temperature']     = self._calculate_temp(resp[36:40])
        data['Pressure']        = self._calculate_pressure(resp[40:44])
        data['Sampling Period'] = self._calculate_period(resp[44:48])
        data['Checksum']        = self._16bit_unsigned(resp[48], resp[49])
        data['PM1']             = self._calculate_float(resp[50:54])
        data['PM2.5']           = self._calculate_float(resp[54:58])
        data['PM10']            = self._calculate_float(resp[58:])

        # Calculate the sum of the histogram bins
        histogram_sum = data['Bin 0'] + data['Bin 1'] + data['Bin 2']   + \
                data['Bin 3'] + data['Bin 4'] + data['Bin 5'] + data['Bin 6']   + \
                data['Bin 7'] + data['Bin 8'] + data['Bin 9'] + data['Bin 10']  + \
                data['Bin 11'] + data['Bin 12'] + data['Bin 13'] + data['Bin 14'] + \
                data['Bin 15']

        return data
