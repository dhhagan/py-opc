[![Build Status](https://travis-ci.org/dhhagan/py-opc.svg?branch=develop)](https://travis-ci.org/dhhagan/py-opc)
[![Coverage Status](https://coveralls.io/repos/dhhagan/py-opc/badge.svg?branch=master&service=github)](https://coveralls.io/github/dhhagan/py-opc?branch=master)

# py-opc

Python library for operating the Alphasense OPC-N2 Optical Particle Counter using a Raspberry Pi (or other linux device). Full documentation can be found [here](http://py-opc.readthedocs.org/en/latest/).

## Dependencies

  1. [`py-spidev`](https://github.com/doceme/py-spidev)

## Installation

For use on the Raspberry Pi (or any other linux device?), there are two methods for easy installation:

### pip (preferred)

Install the py-opc package through PyPi:

    >>> pip install py-opc

Upgrade to the newest version:

    >>> pip install -U py-opc


## License

  This library is licensed under the MIT license.

## Documentation

  Full documentation can be found [here](http://py-opc.readthedocs.org/en/latest/).


## Sample Script / Getting Started

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
    print (alphasense.read_histogram())

    # Turn the opc OFF
    alphasense.off()
