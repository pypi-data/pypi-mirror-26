'''
This module contains a set of bench test scripts for the LArPix chip.

'''
from __future__ import absolute_import

import logging
import larpix.larpix as larpix
import json
from bitstring import BitArray

def setup_logger(settings):
    logger = logging.getLogger(__name__)
    if settings['verbose']:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logger.setLevel(level)
    logfile = settings['logfile']
    handler = logging.FileHandler(logfile)
    handler.setLevel(level)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: '
            '%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def pcb_io_test(settings):
    '''
    Send commands to PCB.

    Probe to verify commands are received. Check for unwanted noise,
    ringing, and reflections.

    '''
    logger = logging.getLogger(__name__)
    logger.info('Performing pcb_io_test')
    port = settings['port']
    controller = larpix.Controller(port)
    packet = larpix.Packet()
    packet.bits = BitArray([1, 0] * 27)
    bytestream = [b's' + packet.bytes() + b'\x00q']
    controller.serial_write(bytestream)

def io_loopback_test(settings):
    '''
    Verify that packet with false chip ID returns to the control system.

    Send packet through daisy chain of LArPix chips but provide the
    wrong chip ID. Each chip should pass on the packet to the next one,
    so that the packet comes out at the end as output.

    '''
    logger = logging.getLogger(__name__)
    logger.info('Performing io_loopback_test')
    port = settings['port']
    controller = larpix.Controller(port)
    chipid = settings['chipset'][0][0]
    io_chain = settings['chipset'][0][1]
    chip = larpix.Chip(chipid, io_chain)
    controller.chips.append(chip)
    packet = larpix.Packet()
    packet.packet_type = larpix.Packet.CONFIG_READ_PACKET
    packet.chipid = chip.chip_id
    packet.register_address = 10
    packet.register_data = 25
    packet.assign_parity()
    bytestream = [controller.format_UART(chip, packet)]
    data = controller.serial_write_read(bytestream, 1)
    controller.parse_input(data)
    if len(chip.reads) > 0:
        returned_packet_str = str(chip.reads[0])
        logger.info(' - Received packet %s', returned_packet_str)
    else:
        logger.warning(' - Did not receive any packets')


def read_register_test(settings):
    '''
    Send "config read" packet and read back the configuration.

    Verify that the packet returns to the control system with the
    expected data. Repeat for every register on every chip.

    '''
    logger = logging.getLogger(__name__)
    logger.info('Performing read_register_test')
    port = settings['port']
    controller = larpix.Controller(port)
    chipset = settings['chipset']
    for chipargs in chipset:
        chip = larpix.Chip(*chipargs)
        controller.chips.append(chip)
    for chip in controller.chips:
        remainder = controller.read_configuration(chip)
        if remainder != b'':
            logger.warning(' - %s returned invalid bytes: %s',
                    str(chip), str(remainder))
        # The chip configuration should be default, so the config we
        # have recorded in software is the same as the expected
        # configuration of the actual chips
        expected_packets = chip.get_configuration_packets(
                larpix.Packet.CONFIG_READ_PACKET)
        actual_packets = chip.reads
        missing_packets = [p for p in expected_packets if p not in
                actual_packets]
        extra_packets = [p for p in actual_packets if p not in
                expected_packets]
        if missing_packets:
            logger.warning(' - %s is missing packets: \n    %s',
                    str(chip), '\n    '.join(map(str, missing_packets)))
        if extra_packets:
            logger.warning(' - %s has extra packets: \n    %s',
                    str(chip), '\n    '.join(map(str, extra_packets)))

def write_register_test(settings):
    '''
    Send "config write" packet, then read the new configuration.

    Verify that:
      - no "config write" packet is returned
      - the configuration on the chip is updated to the new value(s)

    Repeat for every register on every chip.

    Will produce warnings when:
      - a "config write" packet is returned
      - the expected "config read" packet was not returned

    '''
    logger = logging.getLogger(__name__)
    logger.info('Performing write_register_test')
    port = settings['port']
    controller = larpix.Controller(port)
    controller.timeout = 0.1
    chipset = settings['chipset']
    for chipargs in chipset:
        chip = larpix.Chip(*chipargs)
        controller.chips.append(chip)
    # This new config will be written one register at a time
    new_config = larpix.Configuration()
    new_config.load('benchtest-non-defaults.json')
    for chip in controller.chips:
        chip.reads = []
        old_config = chip.config
        chip.config = new_config
        new_config_write_packets = chip.get_configuration_packets(
                larpix.Packet.CONFIG_WRITE_PACKET)
        new_config_read_packets = chip.get_configuration_packets(
                larpix.Packet.CONFIG_READ_PACKET)
        for register in range(chip.config.num_registers):
            chip.config = new_config
            data = controller.write_configuration(chip, register, 0.1)
            controller.parse_input(data)
            new_packet = new_config_write_packets[register]
            if new_packet in chip.reads:
                logger.warning(' - %s returned a config write '
                        'packet:\n    %s', str(chip), str(new_packet))
            controller.read_configuration(chip, register)
            new_packet = new_config_read_packets[register]
            if new_packet not in chip.reads:
                logger.warning(' - %s did not return the expected '
                        'config read packet.\n    Expected packet: %s'
                        '\n    chip.reads: %s', str(chip),
                        str(new_packet), str(chip.reads))
            # Return the configuration back to the default
            chip.config = old_config
            controller.write_configuration(chip)

def uart_test(settings):
    '''
    Execute the UART test on the chip.

    Check to make sure the packets are returned with no dropped packets
    and no flipped bits.

    '''
    logger = logging.getLogger(__name__)
    logger.info('Performing uart_test')
    port = settings['port']
    controller = larpix.Controller(port)
    chipset = settings['chipset']
    test_register = 47
    for chipargs in chipset:
        chip = larpix.Chip(*chipargs)
        controller.chips.append(chip)
    for chip in controller.chips:
        chip.config.test_mode = larpix.Configuration.TEST_UART
        result = controller.write_configuration(chip, registers=47, write_read=2)
        unprocessed = controller.parse_input(result)
        if unprocessed:
            logger.warning(' - %s returned garbled output: %s',
                    str(chip), str(unprocessed))
        counter = 0
        first = True
        for packet in chip.reads:
            if packet.packet_type != larpix.Packet.TEST_PACKET:
                logger.warning(' - %s returned a packet of type %s:\n    %s',
                        str(chip), str(packet.packet_type), str(packet))
                continue
            if first:
                if packet.test_counter == counter:
                    pass
                else:
                    logger.warning(' - %s first packet has counter %d',
                            str(chip), packet.test_counter)
                    counter = packet.test_counter
                    first = False
                continue
            # This line skips every third counter as per spec
            counter = counter + 1 if counter % 3 != 1 else counter + 2
            if packet.test_counter != counter:
                logger.warning(' - %s packet has counter %d, expected %d',
                        str(chip), packet.test_counter, expected_counter)

def threshold_scan_test(settings):
    '''
    Execute the threshold scan as part of CSA noise level test.

    Steps through all of the global thresholds, with the trim
    thresholds set to 0x10 (default). Performs this scan for each
    channel individually. Saves the number of triggers per second to
    the filename specified in settings.

    '''
    logger = logging.getLogger(__name__)
    logger.info('Performing threshold_scan_test')
    controller = larpix.Controller(settings['port'])
    controller.timeout = 0.1
    scan_data = {}
    thresholds = list(range(250, -1, -5))
    try:
        for chip_description in settings['chipset']:
            chip = larpix.Chip(*chip_description)
            controller.chips.append(chip)
            chip.config.disable_channels()
            chip.config.periodic_reset = 1
            controller.write_configuration(chip, [47, 52, 53, 54, 55])
            scan_data[str(chip_description)] = {}
            scan_data['thresholds'] = thresholds
        for chip, description in zip(controller.chips, settings['chipset']):
            for channel in range(32):
                logger.info('Starting chip %s, channel %d' %
                        (str(chip), channel))
                scan_data[str(description)][channel] = []
                channel_thresholds = scan_data[str(description)][channel]
                chip.config.disable_channels()
                chip.config.enable_channels([channel])
                chip.config.global_threshold = 255
                controller.write_configuration(chip, range(52, 56))
                for threshold in thresholds:
                    chip.reads = []
                    chip.config.global_threshold = threshold
                    controller.write_configuration(chip, 32)
                    controller.serial_read(0.1)
                    controller.run(0.5)
                    nreads = len(chip.reads)
                    channel_thresholds.append(nreads)
                    logger.info(nreads)
                logger.info('Chip %s, channel %d: %s', str(chip),
                    channel, str(scan_data))
        with open(settings['filename'], 'w') as outfile:
            json.dump(scan_data, outfile, indent=4)
    except:
        logger.error('Unable to save threshold scan data. '
                'Dumping it here in the log so you can salvage it...')
        logger.error(str(scan_data))
        raise

def periodic_reset_test(settings):
    '''
    Iterate through different periods for the periodic reset, taking
    data with an external trigger.

    Saves all the readout to the specified file.

    '''
    logger = logging.getLogger(__name__)
    logger.info('Performing periodic_reset_test')
    controller = larpix.Controller(settings['port'])
    controller.timeout = 0.1
    data = {}
    reset_periods = list(map(int, [1, 1, 1, 1, 1, 10, 100,
            1000, 2000, 4000, 8000,
            1e4, 2e4, 4e4, 8e4,
            1e5, 2e5, 4e5, 8e5,
            1e6, 2e6, 4e6, 8e6, 16e6]))
    try:
        for chip_description in settings['chipset']:
            chip = larpix.Chip(*chip_description)
            controller.chips.append(chip)
            chip.config.disable_channels()
            chip.config.periodic_reset = 1
            chip.config.global_threshold = 255
            controller.write_configuration(chip)
            data[str(chip_description)] = {}
            data['reset_periods'] = reset_periods
        for chip, description in zip(controller.chips, settings['chipset']):
            for channel in range(32):
                logger.debug('Starting chip %s, channel %d' %
                        (str(chip), channel))
                data[str(description)][channel] = []
                adc_data = data[str(description)][channel]
                chip.config.disable_channels()
                chip.config.enable_channels([channel])
                chip.config.external_trigger_mask = [1] * 32
                chip.config.external_trigger_mask[channel] = 0
                controller.write_configuration(chip)
                for period in reset_periods:
                    chip.reads = []
                    chip.config.reset_cycles = period
                    controller.write_configuration(chip, [60, 61, 62])
                    controller.serial_read(1.5)
                    controller.run(0.5)
                    nreads = len(chip.reads)
                    if nreads == 0:
                        adc_data.append(0)
                    else:
                        adcs = list(map(lambda p:p.dataword,
                            chip.reads))
                        adc_data.append(float(sum(adcs))/nreads)
                    logger.debug(adc_data[-1])
                logger.debug('Chip %s, channel %d: %s', str(chip),
                    channel, str(data))
    except:
        logger.error('Unable to save threshold scan data. '
                'Dumping it here in the log so you can salvage it...')
        logger.error(str(data))
        raise
    finally:
        logger.info('Saving file to %s', settings['filename'])
        with open(settings['filename'], 'w') as outfile:
            json.dump(data, outfile, indent=4)


if __name__ == '__main__':
    import argparse
    import sys
    tests = {
            'pcb_io_test': pcb_io_test,
            'io_loopback_test': io_loopback_test,
            'read_register_test': read_register_test,
            'write_register_test': write_register_test,
            'uart_test': uart_test,
            'threshold_scan_test': threshold_scan_test,
            'periodic_reset_test': periodic_reset_test,
            }
    parser = argparse.ArgumentParser()
    parser.add_argument('--logfile', default='benchtest.log',
            help='the logfile to save')
    parser.add_argument('-p', '--port', default='/dev/ttyUSB1',
            help='the serial port')
    parser.add_argument('-l', '--list', action='store_true',
            help='list available tests')
    parser.add_argument('-t', '--test', nargs='+', default=tests.keys(),
            help='specify test(s) to run')
    parser.add_argument('--chipid', nargs='*', type=int,
            help='list of chip IDs to test')
    parser.add_argument('--iochain', nargs='*', type=int,
            help='list of IO chain IDs (corresponding to chipids')
    parser.add_argument('-f', '--filename', default='out.txt',
            help='filename to save data to')
    parser.add_argument('-m', '--message', default='',
            help='message to save to the logfile')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='print debug messages as well')
    args = parser.parse_args()
    if args.list:
        print('\n'.join(tests.keys()))
        sys.exit(0)
    if args.chipid and args.iochain:
        chipset = list(zip(args.chipid, args.iochain))
    else:
        chipset = None
    settings = {
            'port': args.port,
            'chipset': chipset,
            'logfile': args.logfile,
            'filename': args.filename,
            'verbose': args.verbose
            }
    setup_logger(settings)
    logger = logging.getLogger(__name__)
    logger.info('-'*60)
    logger.info(args.message)
    try:
        for test in args.test:
            tests[test](settings)
    except Exception as e:
        logger.error('Error during test', exc_info=True)
