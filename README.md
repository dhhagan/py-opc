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
    from opc import OPCN2
    from time import sleep
    
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.mode = 1
    spi.max_speed_hz = 500000
    
    alphasense = OPCN2(spi)
    
    # Turn the opc ON
    alphasense.on()
    
    # Read the information string
    print (alphasense.read_info_string())
    
    # Read the histogram
    print (alphasense.read_histogram())
    
    # Turn the opc OFF
    alphasense.off()
