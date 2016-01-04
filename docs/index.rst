.. py-opc documentation master file, created by
   sphinx-quickstart on Mon Dec 28 22:14:54 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to py-opc's documentation!
==================================

**py-opc** is a python module that enables one to use easily operate the Alphasense
OPC-N2 optical particle counter through a Raspberry Pi over the SPI bus. It was originally
designed using a Rapsberry Pi 2 Model B and Python3.5; however, it should work on other versions
as well.

There are a variety of OPC Models and firmware versions from Alphasense; a table documenting which ones
are supported will be added. If you own an OPC-N2 with a firmware version that has not been tested, please
do so and submit as an issue on the GitHub repository.

Installation
------------

You can install this package using ``pip``::

      pip install py-opc

Requirements
------------

The following packages are required:

  * py-spidev_

.. _py-spidev: https://github.com/doceme/py-spidev

Setting Up the Raspberry Pi
---------------------------

If you are not familiar with setting up a Raspberry Pi to be used as a SPI device,
here are a couple of great tutorials: RPi_, Drogon_, and Hensley_. A few important things
to note:

  * The Alphsense OPC-N2 is a 3v3 logic SPI Mode 1 device
  * The OPC requires at least 250 mA, so powering directly through the RPi is not an option

To connect the RPi to the OPC-N2, there are four connections that must be made, plus ground and power. The
power source must be 5 VDC, and should power both the OPC and the RPi to avoid ground issues. The connections
are stated below:

=====  ====================  ===== ==========
 Pin   Function              OPC   RPi
=====  ====================  ===== ==========
1      5 VDC                 VCC    -
2      Serial Clock          SCK   CLK
3      Master In Slave Out   SDO   MISO
4      Master Out Slave In   SDI   MOSI
5      Chip Select           /SS   CE0 or CE1
6      Ground                GND    -
=====  ====================  ===== ==========

.. _RPi: https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/
.. _Drogon: https://projects.drogon.net/understanding-spi-on-the-raspberry-pi/
.. _Hensley: http://www.brianhensley.net/2012/07/getting-spi-working-on-raspberry-pi.html

Getting Help
------------

Still running into problems?

  * To report a problem with this documentation, contact the author.
  * Report an issue_ with the py-opc library on GitHub
  * Submit a feature_ request for py-opc on GitHub.

.. _issue: https://github.com/dhhagan/py-opc/issues/new
.. _feature: https://github.com/dhhagan/py-opc/issues/new

Examples
========

Setting up the SPI Connection
-----------------------------
::

      import spidev
      import opc

      # Open a SPI connection on CE0
      spi = spidev.Spidev()
      spi.open(0, 0)

      # Set the SPI mode and clock speed
      spi.mode = 1
      spi.max_speed_hz = 500000


Initiating the OPCN2
--------------------
::

      try:
          alpha = opc.OPCN2(spi)
      except Exception as e:
          print ("Startup Error: {}".format(e))

Reading a Histogram
-------------------
::

      # Turn on the OPC
      alpha.on()

      # Read the histogram and print to console
      hist = alpha.read_histogram()

      for key, value in hist.items():
          print ("Key: {}\tValue: {}".format(key, value))

      # Shut down the opc
      alpha.off()

API Reference
=============

.. module:: opc
.. autoclass:: OPC
   :members: _combine_bytes, _calculate_float, read_info_string, ping, _calculate_mtof,
            _calculate_temp, _calculate_pressure, _calculate_bin_boundary
.. autoclass:: OPCN1
   :members: on, off, read_gsc_sfr, read_bin_boundaries, write_gsc_sfr, read_bin_particle_density,
            write_bin_particle_density, read_histogram
.. autoclass:: OPCN2
   :members: on, off, read_config_variables, write_config_variables, read_histogram, save_config_variables,
                enter_bootloader_mode, set_fan_power, set_laser_power, laser_on, laser_off, fan_on, fan_off

Exceptions
----------

.. autoexception:: opc.FirmwareError
.. autoexception:: opc.SPIError
