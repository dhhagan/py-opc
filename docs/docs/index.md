# py-opc

py-opc is a python library for interacting with the Alphasense OPC-N2 through
the Serial Peripheral Interface (SPI) bus. The objective is to make it easy to run
the OPC-N2 from a Raspberry Pi. The library is designed to run on a Raspberry Pi 2, with Python 3.x.

Versions are incremented according to [semver][1]

Current OPC firmware versions that are supported include:

  * v14
  * v15
  * v17

Other firmware versions may work, but have not yet been tested. If you would like to test the library on a different firmware version and report back, it would be greatly appreciated.

## Requirements

  * [py-spidev][3]

## Installation

### Git

    >>> git clone https://github.com/dhhagan/py-opc.git
    >>> sudo python3 setup.py install

### Zip

    >>> wget https://github.com/dhhagan/py-opc/archive/master.zip
    >>> unzip master.zip
    >>> cd py-opc/
    >>> sudo python3 setup.py install



### Testing your installation

Testing is completed using the unittesting python module. Once the Raspberry Pi is connected to the OPC and the opc library is installed, you can run unittests as follows:

    >>> python3 -m unittest discover tests/

## Using the Module

Check out the [quickstart manual]() for an easy to use example!

### Setting up the Raspberry Pi

If you are not familiar with setting up a Raspberry Pi to be used with a SPI device, a couple of great tutorials can be found [here][5], [here][6], and [here][7]. A few important things to note:

  1. The Alphasense OPC-N2 is a 3v3 logic SPI mode 1 device
  2. The OPC requires up to 250 mA, so powering through the Raspberry Pi is not an option

To connect the Raspberry Pi to the OPC-N2, there are a total of four connections that need to be made, plus ground and power. The power source must be 5V, and should power both the Raspberry Pi and the OPC. The connections that need to be made are layed out below.

| Pin | Function | OPC-N2 | Raspberry Pi |
|-|-|-|-|
| 1 | Ground | GND | - |
| 2 | Chip Select | /SS | CE0 or CE1 |
| 3 | Master Out Slave In | SDI | MOSI |
| 4 | Clock | SCK | CLK |
| 5 | Master In Slave Out | SDO | MISO |
| 6 | Power | Vcc | - |

Some day there may even be some nice looking diagrams, but I don't have an Illustrator license as of now (booo Adobe!).

## Handling Exceptions

If the SPI connection you feed to the **OPCN2** class is not an instance of the **spidev.SpiDev** class, the **py-opc**
library will throw an **SPIError**. Likewise, if the firmware cannot be determined when initiating the **OPCN2** class, a **FirmwareError** will be raised. Both exceptions can be handled gracefully as follows:

    import opc
    import spidev

    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.mode = 1

    try:
      alpha = OPCN2(spi)
    except Exception as e:
      print ("OPC Exception: {0}".format(e))

## Getting Help

Still running into problems?

  * To report a problem with this documentation, <a href="mailto:david@davidhhagan.com">contact the author</a>.
  * [Report an issue][4] with the py-opc library on Github
  * [Submit a feature request][4] for py-opc on Github


[1]: http://semver.org/
[3]: https://github.com/doceme/py-spidev
[4]: https://github.com/dhhagan/py-opc/issues/new
[5]: https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/
[6]: https://projects.drogon.net/understanding-spi-on-the-raspberry-pi/
[7]: http://www.brianhensley.net/2012/07/getting-spi-working-on-raspberry-pi.html
