#!/usr/bin/env python
# -*- encoding: utf-8 -*-

''' Display the various (local) addresses by calling the `ip` command.  '''

from __future__ import print_function

from subprocess import Popen, PIPE
import re

from waveshare import DisplayText
from waveshare import EPaper
from waveshare import Handshake
from waveshare import RefreshAndUpdate
from waveshare import SetEnFontSize
from waveshare import SetZhFontSize
from waveshare import SetPallet


IFACE_NUM_KEY = 'iface_num'
IFACE_NAME_KEY = 'iface_name'
IFACE_ADDR_KEY = 'iface_addr'

def get_ip_addresses():
    '''
    Calls `ip -o -4 a` to get interface addresses.
    Returns a dictionary of { 'iface_num': num, 'iface_name': name, 'iface_addr': address }
    '''

    command_string = 'ip -o -4 a'
    command_object = Popen(command_string.split(), stdout=PIPE)
    results = command_object.stdout.read()
    pattern = r'\W*([0-9]+)\W*:\W*([a-z0-9]+)\W*inet\W*(([0-9]+\.?){4}/[0-9]+)'
    iface_num = 0 # offset 0 into the pattern is the interface number
    iface_name = 1 # offset 1 into the pattern is the interface name
    ip = 2 # offset 2 into the pattern is the interface address
    output = []

    for line in results.split('\n'):
        #import pdb
        #pdb.set_trace()
        matches = re.match(pattern, line)
        if matches:
            groups = matches.groups()
            output.append(
                {
                    IFACE_NUM_KEY: groups[iface_num],
                    IFACE_NAME_KEY: groups[iface_name],
                    IFACE_ADDR_KEY: groups[ip]
                }
            )

    return output

LAST_LINE = 'last_line'

##
# The use of the default value is intentional on the next line to make use of a
# statically defined value for use in write_line.
def write_line(paper, line, static={}): #pylint: disable=dangerous-default-value
    '''
    Write a line of text to the epaper display.
    '''
    font_size = 32
    if not static:
        static[LAST_LINE] = 1
    line_count = static[LAST_LINE]
    static[LAST_LINE] += 1

    paper.send(DisplayText(0, line_count*font_size, line.encode('gb2312')))

def wait_for_paper(paper):
    '''
    Wait for the specified e-ink display to no longer have any waiting input.
    This is better than arbitrary sleeps, but there is probably a better way
    still to wait until the display is ready to receive more commands.
    '''
    while paper.read():
        pass

def main():
    '''
    Run the logic for getting local IP addresses, then write them to the EInk
    display (and stdout).
    '''
    with EPaper('/dev/ttyAMA0') as paper:
        paper.send(Handshake())
        wait_for_paper(paper)
        paper.send(SetPallet(SetPallet.BLACK, SetPallet.WHITE))
        paper.send(SetEnFontSize(SetEnFontSize.THIRTYTWO))
        paper.send(SetZhFontSize(SetZhFontSize.THIRTYTWO))
        print('Interfaces:')
        write_line(paper, 'Interfaces:')
        for entry in get_ip_addresses():
            print('  %s: %s' % (
                entry[IFACE_NAME_KEY], entry[IFACE_ADDR_KEY]))
            write_line(paper, '  %s: %s' % (
                entry[IFACE_NAME_KEY], entry[IFACE_ADDR_KEY]))
            write_line(paper, '')
        paper.send(RefreshAndUpdate())
        wait_for_paper(paper)

if __name__ == "__main__":
    main()
