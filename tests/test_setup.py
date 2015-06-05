import unittest
import spidev
from time import sleep
from opc import OPCN2
from opc.exceptions import SPIError, FirmwareError

interval = 1

class SetupTestCase(unittest.TestCase):

    def setUp(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 1
        self.spi.max_speed_hz = 500000

        self.alpha = OPCN2(self.spi)
        #self.assertRaises(SPIError, OPCN2, None)

    def tearDown(self):
        pass

    def test_spi(self):
        sleep(interval)
        self.assertIsInstance(self.spi, spidev.SpiDev)

    def test_firmware(self):
        sleep(interval)
        self.assertTrue(self.alpha.firmware in [14, 15, 16, 17])

    def test_opc(self):
        # Turn on the opc
        sleep(interval)
        self.assertTrue(self.alpha.on())
        sleep(interval)
        self.assertTrue(self.alpha.off())

    def test_ping(self):
        sleep(interval)
        self.assertTrue(self.alpha.ping())

    def test_read_info_string(self):
        sleep(interval)
        infostring = self.alpha.read_info_string()

        self.assertTrue('OPC-N2' in infostring)

    def test_read_config_variables(self):
        sleep(interval)
        vars = self.alpha.read_config_variables()
        self.assertTrue(vars['Bin Boundary 0'] is not None)

    def test_write_config(self):
        sleep(interval)
        pass

    def test_read_histogram(self):
        sleep(interval)
        hist = self.alpha.read_histogram()

        self.assertTrue(hist is not None)
        self.assertTrue(hist['Temperature'] >= 0.0)

    def test_save_config(self):
        sleep(interval)
        pass

    def test_bootloader_mode(self):
        sleep(interval)
        pass

    def test_set_fan_power(self):
        sleep(interval)
        #self.assertRaise(ValueError, self.alpha.set_fan_power, 300)
        self.assertTrue(self.alpha.set_fan_power(255))


    def test_set_laser_power(self):
        #self.assertRaise(ValueError, self.alpha.set_laser_power(400))
        sleep(interval)
        self.assertTrue(self.alpha.set_laser_power(150))

    def test_laser_settings(self):
        sleep(interval)
        self.assertTrue(self.alpha.laser_on())
        sleep(interval)
        self.assertTrue(self.alpha.laser_off())

    def test_fan_settings(self):
        sleep(interval)
        self.assertTrue(self.alpha.fan_on())
        sleep(interval)
        self.assertTrue(self.alpha.fan_off())


if __name__ == '__main__':
    unittest.main()
