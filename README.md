# py-opc

Python library for operating the Alphasense OPC-N2 Optical Particle Counter using a Raspberry Pi (or other linux device). Full documentation can be found [here](http://dhhagan.github.io/py-opc/).

## Dependencies
  
  1. [`py-spidev`](https://github.com/doceme/py-spidev)

## Installation

For use on the Raspberry Pi (or any other linux device?), there are two methods for easy installation:

### Using wget

  1. `>>> wget https://github.com/dhhagan/py-opc/archive/master.zip`
  2. `>>> unzip master.zip`
  3. `>>> cd py-opc/`
  4. `>>> sudo python3 setup.py install`

## Using git  

  1. `>>> git clone https://github.com/dhhagan/py-opc.git`
  2. `>>> cd py-opc/`
  3. `>>> sudo python3 setup.py install`
  
## License

  This library is licensed under the MIT license.

## Documentation

  Full documentation can be found [here](http://dhhagan.github.io/py-opc/).
  
## Unit Testing

  To run unit-tests, run the command:
  
    >>> python3 -m unittest discover tests/

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
