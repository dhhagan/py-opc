''' Exceptions for the Alphasense OPC-N2 Library '''

class SpiConnectionError(Exception):
    """Raised when the argument sent to opc.OPCN2() is not a valid spidev.SpiDev instance.
    """
    pass

class FirmwareVersionError(Exception):
    """Raised if the firmware version of your OPC is not supported with this
    version of the py-opc module. Please check the GitHub repository for updates.

    This is usually raised under two circumstances:

      1. Your firmware version is not supported
      2. Your firmware version cannot be detected (usually due to a bad wiring)
    """
    pass

firmware_error_msg = """This is the incorrect firmware version."""
