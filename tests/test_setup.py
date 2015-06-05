import unittest
import spidev
from time import sleep
from opc import OPCN2
from opc.exceptions import SPIError, FirmwareError

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
        self.assertIsInstance(self.spi, spidev.SpiDev)

    def test_firmware(self):
        self.assertTrue(self.alpha.firmware in [14, 15, 16, 17])

    def test_opc(self):
        # Turn on the opc
        self.assertTrue(self.alpha.on())
        sleep(2)
        self.assertTrue(self.alpha.off())

    def test_ping(self):
        self.assertTrue(self.alpha.ping())

    def test_read_info_string(self):
        infostring = self.alpha.read_info_string()

        self.assertTrue('OPC-N2' in infostring)

    def test_read_config_variables(self):
        vars = self.alpha.read_config_variables()
        self.assertTrue(vars['Bin Boundary 0'] is not None)

    def test_write_config(self):
        pass

    def test_read_histogram(self):
        hist = self.alpha.read_histogram()

        self.assertTrue(hist is not None)
        self.assertTrue(hist['Temperature'] >= 0.0)

    def test_save_config(self):
        pass

    def test_bootloader_mode(self):
        pass

    def test_set_fan_power(self):
        self.assertFalse(self.alpha.set_fan_power(300))
        self.assertTrue(self.alpha.set_fan_power(255))

    def test_set_laser_power(self):
        self.assertFalse(self.alpha.set_laser_power(400))
        self.assertTrue(self.alpha.set_laser_power(150))

    def test_laser_settings(self):
        self.assertTrue(self.alpha.laser_on())
        self.assertTrue(self.alpha.laser_off())

    def test_fan_settings(self):
        self.assertTrue(self.alpha.fan_on())
        self.assertTrue(self.alpha.fan_off())


if __name__ == '__main__':
    unittest.main()
