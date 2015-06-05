import unittest
import spidev
from .opc import OPCN2

class SetupTestCase(unittest.TestCase):

    def setUp(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 1
        self.spi.max_speed_hz = 500000

        self.alpha = OPCN2(self.spi)

    def tearDown(self):
        pass

    def test_spi(self):
        assertIsInstance(self.spi, spidev.SpiDev)

    def test_opc(self):
        pass

    def test_ping(self):
        self.assertTrue(spi.ping())

class TestExceptions(unittest.TestCase):

    def test_OPCError(self):
        pass

if __name__ == '__main__':
    unittest.main()
