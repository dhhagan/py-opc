[![Build Status](https://travis-ci.org/dhhagan/py-opc.svg?branch=develop)](https://travis-ci.org/dhhagan/py-opc)
[![PyPI version](https://badge.fury.io/py/py-opc.svg)](https://badge.fury.io/py/py-opc)
[![Coverage Status](https://coveralls.io/repos/dhhagan/py-opc/badge.svg?branch=master&service=github)](https://coveralls.io/github/dhhagan/py-opc?branch=master)
[![DOI](https://zenodo.org/badge/30832320.svg)](https://zenodo.org/badge/latestdoi/30832320)

# py-opc

Python library for operating the Alphasense OPC-N2 Optical Particle Counter using a Raspberry Pi (or other linux device). Full documentation can be found [here](http://py-opc.readthedocs.org/en/latest/).


## Dependencies

One of:

  1. [`py-spidev`](https://github.com/doceme/py-spidev)
  1. [`py-usbiss`](https://github.com/dancingquanta/py-usbiss)


## Installation

For use on the Raspberry Pi (or any other linux device?), install via pip:

    >>> pip install py-opc [--upgrade]

## License

  This library is licensed under the MIT license.

## Documentation

  Full documentation can be found [here](http://py-opc.readthedocs.org/en/latest/).

  You can also build the documentation by navigating to the `docs` directory and issuing the command:

    >>> make html


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
    print (alphasense.histogram())

    # Turn the opc OFF
    alphasense.off()
