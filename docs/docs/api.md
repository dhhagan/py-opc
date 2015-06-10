##OPCN2

*class* **opc.OPCN2(spi_connection, debug = False)**

The *OPCN2* class takes the **spidev.SpiDev** instance as a required argument, with the option to also set **debug** mode. If there is an issue with the spidev connection, an **opc.SPIError**  will be raised. If the firmware cannot be determined, an **opc.FirmwareError** will be raised.

#### Attributes

<div style="margin-left:25px; margin-bottom:10px">
  <h3>cnxn</h3>
  <p>
    cnxn is an instance of <bold><em>spidev.SpiDev</em></bold>.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>debug</h3>
  <p>
    debug is a <bold><em>boolean</em></bold>.
  </p>
  <p>
    if True, some useful information is printed out!
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>firmware</h3>
  <p>
    firmware is an <bold><em>integer</em></bold>.
  </p>
  <p>
    Firmware version of the Alphasense OPC-N2.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>on()</h3>
  <p>
    Returns <bold><em>True</em></bold> if the fan and laser are successfully turned ON.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>off()</h3>
  <p>
  Returns <bold><em>True</em></bold> if the fan and laser are successfully turned OFF.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>ping()</h3>
  <p>
    Returns <bold><em>True</em></bold> if the <bold><em>check_status</em></bold> command is executed correctly.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>read_info_string()</h3>
  <p>
    Returns a <bold><em>string</em></bold> containing the OPC Firmware version. This method also sets the firmware version attribute; if the firmware version is not supported, a <bold><em>FirmwareError</em></bold> is raised.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>read_config_variables()</h3>
  <p>
    Returns a dictionary containing all configuration variables as described below.
  </p>
  <table>
    <thead>
      <th>Key</th>
      <th>Value</th>
      <th>Description</th>
    </thead>

    <tbody>
      <tr>
        <td>Bin Boundary XX</td>
        <td>unsigned 16-bit integer</td>
        <td>Bin boundaries 0-14 are ADC values representing the bin boundary</td>
      </tr>
      <tr>
        <td>BPV XX</td>
        <td>Float</td>
        <td>Bin Particle Volumes 0-15</td>
      </tr>
      <tr>
        <td>BPD XX</td>
        <td>Float</td>
        <td>Bin Particle Densities 0-15</td>
      </tr>
      <tr>
        <td>BSVW XX</td>
        <td>Float</td>
        <td>Bin Sample Volume Weightings 0-15</td>
      </tr>
      <tr>
        <td>GSC</td>
        <td>Float</td>
        <td>Gain Scaling Coefficient</td>
      </tr>
      <tr>
        <td>SFR</td>
        <td>Float</td>
        <td>Sample Flow Rate in ml/s</td>
      </tr>
      <tr>
        <td>LaserDAC</td>
        <td>8 bit integer</td>
        <td>Laser power as an 8-bit integer (0-255)</td>
      </tr>
      <tr>
        <td>FanDAC</td>
        <td>8 bit integer</td>
        <td>Fan speed as an 8-bit integer (0-255)</td>
      </tr>
    </tbody>
  </table>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>write_config_variables()</h3>
  <p>
    This method is currently not implemented as of v0.1x
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>read_histogram()</h3>
  <p>
    Returns a dictionary containing the histogram as described in Alphasense' documentation.
  </p>
  <table>
    <thead>
      <th>Key</th>
      <th>Value</th>
      <th>Description</th>
    </thead>

    <tbody>
      <tr>
        <td>Bin XX</td>
        <td>unsigned 16-bit integer</td>
        <td>Bins 0-15 are integers representing the histogram count for a given bin.</td>
      </tr>
      <tr>
        <td>Bin1 MToF</td>
        <td>Float</td>
        <td>Returns the average amount of time that particles in Bin 1 took to cross the path of the OPC in microseconds</td>
      </tr>
      <tr>
        <td>Bin3 MToF</td>
        <td>Float</td>
        <td>Returns the average amount of time that particles in Bin 3 took to cross the path of the OPC in microseconds</td>
      </tr>
      <tr>
        <td>Bin5 MToF</td>
        <td>Float</td>
        <td>Returns the average amount of time that particles in Bin 5 took to cross the path of the OPC in microseconds</td>
      </tr>
      <tr>
        <td>Bin7 MToF</td>
        <td>Float</td>
        <td>Returns the average amount of time that particles in Bin 7 took to cross the path of the OPC in microseconds</td>
      </tr>
      <tr>
        <td>Temperature</td>
        <td>Float</td>
        <td>Returns the temperature in degrees celcius</td>
      </tr>
      <tr>
        <td>Pressure</td>
        <td>8 bit integer</td>
        <td>Returns the pressure in Pascals</td>
      </tr>
      <tr>
        <td>Sampling Period</td>
        <td>8 bit integer</td>
        <td>Returns the actual sampling period in seconds.</td>
      </tr>
      <tr>
        <td>Checksum</td>
        <td>16 bit unsigned integer</td>
        <td>Returns the total sum of histogram counts across all bins.</td>
      </tr>
      <tr>
        <td>PM1</td>
        <td>Float</td>
        <td>Returns the PM1 value in micrograms/m3</td>
      </tr>
      <tr>
        <td>PM2.5</td>
        <td>Float</td>
        <td>Returns the PM2.5 value in micrograms/m3</td>
      </tr>
      <tr>
        <td>PM10</td>
        <td>Float</td>
        <td>Returns the PM10 value in micrograms/m3</td>
      </tr>
    </tbody>
  </table>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>save_config_variables()</h3>
  <p>
    Saves the config variables to non-volatile memory.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>enter_bootloader_mode()</h3>
  <p>
    Enter bootloader mode.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>set_fan_power(fan_value)</h3>
  <p>
    Set the fan power as an 8-bit unsigned integer. If the value is out of range (>255), a ValueError is raised.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>set_laser_power(laser_value)</h3>
  <p>
    Set the laser power as an 8-bit unsigned integer. If the value is out of range (>255), a ValueError is raised.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>laser_on()</h3>
  <p>
    Returns True if the laser is successfully turned ON.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>laser_off()</h3>
  <p>
    Returns True if the laser is successfully turned OFF.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>fan_on()</h3>
  <p>
    Returns True if the fan is successfully turned ON.
  </p>
</div>

<div style="margin-left:25px; margin-bottom:10px">
  <h3>fan_off()</h3>
  <p>
    Returns True if the fan is successfully turned OFF.
  </p>
</div>


# Exceptions

There are two custom exceptions that can be raised from within the opc library.

#### SPIError

The SpiError is raised upon OPCN2 initialization if the spi connection is not valid.

#### FirmwareError

The FirmwareError is raised if the firmware version is either not valid or not supported.
