#!/usr/bin/env python

from curses import baudrate
import sys
import serial
import struct
from serial.tools.list_ports import comports

try:
    raw_input
except NameError:
    # pylint: disable=redefined-builtin,invalid-name
    raw_input = input   # in python3 it's "raw"
    unichr = chr


def ask_for_port():
    """\
    Show a list of ports and ask the user for a choice. To make selection
    easier on systems with long device names, also allow the input of an
    index.
    """
    sys.stderr.write('\n--- Available ports:\n')
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        sys.stderr.write('--- {:2}: {:20} {!r}\n'.format(n, port, desc))
        ports.append(port)
    while True:
        sys.stderr.write('--- Enter port index or full name: ')
        port = raw_input('')
        try:
            index = int(port) - 1
            if not 0 <= index < len(ports):
                sys.stderr.write('--- Invalid index!\n')
                continue
        except ValueError:
            pass
        else:
            return ports[index]
        return None

class RdsServer(object):
    def __init__(self, serial_instance):
        self.serial = serial_instance
    def testwrite(self, data):
        self.serial.write(data)

serialport = ask_for_port()
baudrate = 9600
print('serialport=%s, baud=%d' % (serialport, baudrate))

serial_instance = serial.serial_for_url(serialport, baudrate)
r = RdsServer(serial_instance)
r.testwrite('123'.encode('utf-8'))
