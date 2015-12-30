''' Exceptions for the Alphasense OPC-N2 Library '''

class SPIError(Exception):
    """Raised when there is an error with your SPI connection
    as created using py-spidev. An instance of spidev.SpiDev is
    expected.
    """
    pass

class FirmwareError(Exception):
    """Raised under two circumstances:

      1. Your firmware version is not supported
      2. Your firmware version cannot be detected (usually due to a bad connection)
    """
    pass
