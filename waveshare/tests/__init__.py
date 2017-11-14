#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Tests for the waveshare 800x600 4.3 inch e-Paper UART module classes
'''

# The unit test base classes have too many public methods, so squash those
# errors:
# pylint: disable=too-many-public-methods

import unittest
from waveshare import Handshake

class TestCommandSerialization(unittest.TestCase):
    '''
    Tests that the various commands will serialize to what the wiki had for
    examples.
    '''

    def test_handshake_serializes(self):
        ''' The handshake should serialize to A5 00 09 00 CC 33 C3 3C AC. '''

        expected = 'A5 00 09 00 CC 33 C3 3C AC'.lower()
        actual = ('%s' % Handshake()).lower()
        self.assertEquals(expected, actual,
                "Values didn't match expected value! actual: %s expected: %s"
                % (actual, expected))

def main():
    '''
    Convenient wrapper to invoke all the tests in here.
    '''
    unittest.main()

if __name__ == "__main__":
    main()
