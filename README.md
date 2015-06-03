# py-opc

Python library for operating the Alphasense OPC-N2 Optical Particle Counter using a Raspberry Pi (or other linux device)

## Dependencies
  
  1. `py-spidev`

## Installation
  
  1. Download the .zip or clone the git repository to your local machine (raspberry pi)
  2. Unzip the folder if in .zip format
  3. `>>> sudo python3 setup.py install`
  
## License

  This library is licensed under the MIT license.

## Documentation

  Full documentation coming soon!

## Sample Script / Getting Started

    import spidev
    from py-opc import OPCN2
    from time import sleep
    
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.mode = 1
    spi.max_speed_hz = 500000
    
    opc = OPCN2(spi)
    
    # Turn the opc ON
    opc.on()
    
    # Read the information string
    print (opc.read_info_string())
    
    # Read the histogram
    print (opc.read_histogram())
    
    # Turn the opc OFF
    opc.off()
