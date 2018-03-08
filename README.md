[![Build Status](https://travis-ci.org/dhhagan/py-opc.svg?branch=develop)](https://travis-ci.org/dhhagan/py-opc)
[![PyPI version](https://badge.fury.io/py/py-opc.svg)](https://badge.fury.io/py/py-opc)
[![Coverage Status](https://coveralls.io/repos/dhhagan/py-opc/badge.svg?branch=master&service=github)](https://coveralls.io/github/dhhagan/py-opc?branch=master)
[![DOI](https://zenodo.org/badge/30832320.svg)](https://zenodo.org/badge/latestdoi/30832320)

# py-opc

Python library for operating the Alphasense OPC-N2 Optical Particle Counter using a Raspberry Pi (or other linux device). Full documentation can be found [here](http://py-opc.readthedocs.org/en/latest/).


## Dependencies

One of the following, depending on whether you use GPIO pins or a SPI-USB adapter:

  1. [`py-spidev`](https://github.com/doceme/py-spidev) - for those using GPIO pins
  1. [`pyusbiss`](https://github.com/dancingquanta/pyusbiss) - for those using a SPI-USB adapter (python3+ only)


## Installation

For use on the Raspberry Pi (or any other linux device?), install via pip:

    $ pip install py-opc [--upgrade]

As `pyusbiss` is not yet available through a package manager, you must download from source (if you are using the SPI-USB adapter only). This can be done as follows:

    $ pip install git+https://github.com/DancingQuanta/pyusbiss.git

If you are using the GPIO pins to communicate with the OPC-N2, you must download the requirement `py-spidev` as follows:

    $ pip install git+https://github.com/doceme/py-spidev.git


## License

  This library is licensed under the MIT license. The full text of the license can be found in this repository at LICENSE.txt.

## Documentation

  Full documentation can be found [here](http://py-opc.readthedocs.org/en/latest/).

  You can also build the documentation by navigating to the `docs` directory and issuing the command:

    $ make html


## Sample Script / Getting Started

To quickly get up and running, follow one of the two examples:

### GPIO-connected OPC-N2

Use if you are using the GPIO pins in conjunction with `py-spidev`

    import spidev
    import opc
    from time import sleep

    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.mode = 1
    spi.max_speed_hz = 500000

    alphasense = opc.OPCN2(spi)

    # Turn the opc ON
    alphasense.on()

    # Read the information string
    print (alphasense.read_info_string())

    # Read the histogram
    print (alphasense.histogram())

    # Turn the opc OFF
    alphasense.off()

### SPI-USB Adapter with OPC-N2

Use this approach if you have connected your RPi to the OPC-N2 via a SPI-USB adapter.

**NOTE**: Currently, this method is only supported on python3+ due to limitations in the `pyusbiss` library.

    from usbiss.spi import SPI
    import opc

    # Build the connector
    spi = SPI("/dev/ttyACM0")

    # Set the SPI mode and clock speed
    spi.mode = 1
    spi.max_speed_hz = 500000

    alpha = opc.OPCN2(spi)

    # Turn on the device
    alpha.on()

    # Read the histogram
    alpha.histogram()

    # Turn the device off
    alpha.off()
