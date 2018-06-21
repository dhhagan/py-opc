---
title: 'py-opc: operate the Alphasense OPC-N2 from a raspberry pi or other popular microcontrollers/microcomputers'
tags:
 - python
 - c++
 - aerosols
 - atmospheric chemistry
 - raspberry pi
 - particle photon
 - arduino
authors:
 - name: David H Hagan
   orcid: 0000-0001-5111-4671
   affiliation: 1
 - name: Andrew Tolmie
   affiliation: "2, 3"
 - name: Jakub Trochim
   affiliation: "4"
affiliations:
 - name: Massachusetts Institute of Technology
   index: 1
 - name: University of Leeds
   index: 2
 - name: National Physical Laboratory
   index: 3
 - name: Sensonar
   index: 4
date: 2017-12-21
bibliography: paper.bib
---

# Statement of Need

As shipped by Alphasense Ltd., the OPC-N2 optical particle counter is operable either via a PC-based GUI or running the device in standalone mode (logging to an on-board SD card). However, most people use the device in a remote fashion by building it into a more complete air quality monitoring device. While SPI control is possible, there is no library available to do so, thus requiring individuals to roll out their own software solution each time.

# Summary

py-opc is a python library for operating the Alphasense OPC-N2 via a raspberry pi or arduino/arduino-like microcontroller. The OPC-N2 is one of the more popular OEM particle counters used by researchers and other interested parties, as it provides reasonably accurate data (see references) across a wide range of particle diameters (PM1, PM2.5, PM10) at high time resolution (~1Hz). In addition to particle mass loadings, the device also provides access to the underlying histogram/bin counts, allowing researchers to further probe the source of aerosols.

As mentioned in the statement of need above, the manufacturer does not provide their own software that can be used to control the device, with the exception of a PC-based GUI (with drivers for Windows machines only). py-opc provides a python library with a simple API for operating the device via the SPI interface, which means it is completely cross-platform. The value-add is large, as it reduces the time to get started using this device with distributed sensors. The python library is built on top of the py-spidev library (GPIO pins) and/or pyusbiss library (USB) to operate with a Raspberry Pi or Beaglebone. Full control is given to the user via the API including functionality to set configuration settings, read configuration settings, sample the histogram, and much more (see full API documentation for complete list of functionality).

Overall, the goal of this work is to make it easier for other scientists to get started with this device without the need for writing their own SPI wrapper.

# Mentions

  * Crilley, L. R., Shaw, M., Pound, R., Kramer, L. J., Price, R., Young, S., Lewis, A. C., and Pope, F. D.: Evaluation of a low-cost optical particle counter (Alphasense OPC-N2) for ambient air monitoring, Atmos. Meas. Tech. Discuss., https://doi.org/10.5194/amt-2017-308, in review, 2017.

# References
