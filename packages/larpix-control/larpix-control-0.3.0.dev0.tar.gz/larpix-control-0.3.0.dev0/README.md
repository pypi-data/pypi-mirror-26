# larpix-control

Control the LArPix chip

## Setup and installation

This code is intended to work on both Python 2.7+ and Python 3.6+,
but it was designed in Python 3 and is not guaranteed to work in
Python 2.

Download this repository. Install the Python packages "pyserial" and
"bitstring" with the following commands:

```
pip install pyserial
pip install bitstring
```

### Tests

You can run tests to convince yourself that the software works as
expected. First install the "[pytest](https://pytest.org)" package with
`pip install pytest`. You can then run the tests from the `python`
directory with the simple command `pytest`.

You can read the tests to see examples of how to call all of the common
functions. I imagine they will also come in handy when you're confused
about the bit order. (Also see the section on endian-ness below.)

## Tutorial

This tutorial runs through how to use all of the main functionality of
larpix-control.

### Endian-ness

We use the convention that the LSB is sent out first and read in first.
The location of the LSB in arrays and lists changes from object to
object based on the conventions of the other packages we interact with.

In particular, pyserial sends out index 0 first, so for `bytes` objects,
index 0 will generally have the LSB. On the other hand, bitstrings
treats the _last_ index as the LSB, which is also how numbers are
usually displayed on screen, e.g. `0100` in binary means 4 not 2. So for
`BitArray` and `Bits` objects, the LSB will generally be last.

### Creating a LArPix Chip

The `Chip` object represents a single LArPix chip and knows about
everything happening on the chip regarding configuration, data sent in,
and data read out. To create a Chip, just provide the chip ID number
(hard-wired into the PCB) and the index for the IO Chain (daisy chain)
that the chip is part of:

```python
myChip = Chip(100, 0)
```

The Chip object uses these ID values when it creates data packets to
ensure that the packet reaches the correct chip. And other objects use
the ID values to ensure that received data from the physical chip makes
its way to the right Chip object.

### Configuring the Chip

To update the configuration register in the LArPix chip, first you must
set the appropriate values in the Chip object. These values are stored
in the `Chip.configuration` attribute. An assortment of helper
methods will make it much easier to set many options, especially those
operating per channel. For full access to the chip's configuration, read
the next section on the `Configuration` object, of which
`chip.configuration` is an instance.

### The Configuration object

The `Configuration` object represents all of the options in the LArPix
configuration register. Each row in the configuration table in the LArPix datasheet
has a corresponding attribute in the `Configuration` object. Per-channel
attributes are stored in a list, and all other attributes are stored as
a simple integer. (This includes everything from single bits to values
such as "reset cycles," which spans 3 bytes.) **Warning**: there is
currently no type checking or range checking on these values. Using
values outside the expected range will lead to undefined behavior,
including the possibility that Python will crash _or_ that LArPix will
be sent bad commands.

The machinery of the `Configuration` object ensures that each value is
converted to the appropriate set of bits when it comes time to send
actual commands to the physical chip. Although this is not transparent
to you as a user of this library, you might want to know that two sets of
configuration options are always sent together in the same configuration
packet:

 - `csa_gain`, `csa_bypass`, and `internal_bypass` are combined into a
   single byte, so even though they have their own attributes, they must
   be written to the physical chip together

 - `test_mode`, `cross_trigger_mode`, `periodic_reset`, and
   `fifo_diagnostic` work the same way

Similarly, all of the per-channel options (except for the pixel trim
thresholds) are sent in 4 groups of 8 channels.

Once the Chip object has been configured, the configuration must be sent
to the physical chip. This is accomplished with the `Controller` object,
which we'll discuss next.

### Communicating with the physical LArPix chip

Communication between the computer and the physical LArPix chip is
handled by the `Controller` object and uses a Serial interface. (The
interface specification is given in the fpga\_interface.txt file. It's
based on RS-232 8N1.) To initialize a Controller object, simply provide
the port you'd like to communicate over. For the envisioned normal
application (with an FTDI chip as USB-serial bridge), this will likely
be something like `/dev/ttyUSB0`.

```python
controller = Controller('/dev/ttyUSB0')
```

You might want to change the following
attributes at some point, but their defaults should work in most cases:

 - `baudrate`: default = 1000000 baud. Controls the number of bits per
   second, including RS-232 start and stop bits.
 - `timeout`: default = 1 second. Controls how long to wait before
   ending a read command
 - `max_write`: default = 8192 bytes. Controls the maximum number of
   bytes to send with a single write command. The limit is entirely due
   to the buffer capacity of the FTDI chip.

#### Sending data

The only data that LArPix can receive is configuration data. To send all
of the configuration packets in write mode, simply call

```python
myChip = Chip(chip_id, io_chain)
# Edit the configuration
# ...
myController = Controller('/dev/ttyUSB0')
myController.write_configuration(myChip)
```

To send only a particular configuration register or list of
configuration registers, pass the register or list of registers to the
function:

```python
register_to_update = 51
myController.write_configuration(myChip, register_to_update)
# or pass a list ...
registers_to_update = [0, 5, 42]
myController.write_configuration(myChip, registers_to_update)
```

There is currently not a way to specify which register to update by
passing a string or other way of identifying the register by name.

Similar functionality exists to read the configuration data. This
requires both sending data to and receiving data from the LArPix chip.
To send the "read configuration" commands, call `read_configuration`
exactly the same way you would call `write_configuration`.

#### Receiving data

There are 3 reasons to receive data from LArPix: because it's real data
(ADC counts, etc.), because it's configuration data that has been
requested, or because it's test data from either the UART test or the
FIFO test.
