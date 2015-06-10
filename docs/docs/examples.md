# Examples

## Quickstart

### Setting up the SPI connection

    import spidev
    from opc import OPCN2

    # Open a spidev connection on CE0
    spi = spidev.SpiDev()
    spi.open(0, 0)

    # Set the SPI mode and clock speed
    spi.mode = 1
    spi.max_speed_hz = 500000

### Initiating the OPCN2 class

    try:
      alpha = OPCN2(spi)
    except Exception as e:
      print ("Startup Error: {0}".format(e))

    # Check connection
    print ("Connection OK? {0}".format(alpha.ping()))

### Using the OPC-N2 to read a single histogram

    # Turn on the OPC
    alpha.on()

    # Read the histogram and print out
    histogram = alpha.read_histogram()

    for key, value in histogram.items():
        print ("Key: {0}\t Value: {1}".format(key, value))

    # Shutdown the OPC
    alpha.off()
