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
affiliations:
 - name: Massachusetts Institute of Technology
   index: 1
 - name: University of Leeds
   index: 2
 - name: National Physical Laboratory
   index: 3
date: 2017-12-21
bibliography: paper.bib
---

# Statement of Need

As shipped, the Alphasense OPC-N2 ships with a PC-ready GUI, but no acceptable drivers for using with popular microcontrollers. This library fixes that.

# Summary

The py-opc and opcn2 libraries enable the simple operation of the Alphasense OPC-N2 optical particle counter (OPC) from either a Raspberry Pi/Beagle Bone (written in python) or Arduino/Arduino-like devices (written in c++). The python version requires either the py-spidev (GPIO pins) or pyusbiss (USB-SPI converter) libraries. Complete SPI control is given to the user via the API, allowing complete control over settings and operation of the OPC.

# Mentions

  * Crilley, L. R., Shaw, M., Pound, R., Kramer, L. J., Price, R., Young, S., Lewis, A. C., and Pope, F. D.: Evaluation of a low-cost optical particle counter (Alphasense OPC-N2) for ambient air monitoring, Atmos. Meas. Tech. Discuss., https://doi.org/10.5194/amt-2017-308, in review, 2017.

# References
