#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Tests for the waveshare 800x600 4.3 inch e-Paper UART module classes

These tests are for the functions in the classes, not the actual display unit,
so no display needs to be hooked up.
'''

# The unit test base classes have too many public methods, so squash those
# errors:
# pylint: disable=too-many-public-methods
# doc strings for unit tests get cut off after the new line, so they're
# generally too long, so squash those errors:
# pylint: disable=line-too-long

import unittest
from waveshare import Handshake
from waveshare import SetBaudrate
from waveshare import ReadBaudrate
from waveshare import ReadStorageMode
from waveshare import SetStorageMode
from waveshare import SleepMode
from waveshare import RefreshAndUpdate
from waveshare import CurrentDisplayRotation
from waveshare import SetCurrentDisplayRotation
from waveshare import ImportFontLibrary
from waveshare import ImportImage
from waveshare import DrawCircle
from waveshare import FillCircle
from waveshare import DrawTriangle
from waveshare import FillTriangle
from waveshare import ClearScreen
from waveshare import DisplayText
from waveshare import DisplayImage

MISMATCH = u"Values didn't match: \nactual:   %s \nexpected: %s"

class TestCommandSerialization(unittest.TestCase):
    '''
    Tests that the various commands will serialize to what the wiki had for
    examples.
    '''

    def wrapper(self, expected, actual):
        '''
        A wrapper to simplify the other tests here.  Every test is basically a
        case insensitive comaprison and then expanding the input parameters
        into the output so that it's easier to see what caused the error, so
        that functionality is all here to shorten bodies elesewhere.

        @param expected A string with an expected value.
        @param actual The Actual value to compare.
        @throws AssertionError Raises and AssertionError if the test failed.
        '''
        expected = expected.lower()
        actual = ('%s' % actual).lower()
        self.assertEquals(expected, actual, MISMATCH % (actual, expected))


    def test_handshake_serializes(self):
        ''' The handshake should serialize to A5 00 09 00 CC 33 C3 3C AC. '''
        self.wrapper('A5 00 09 00 CC 33 C3 3C AC', Handshake())

    def test_setbaud_9600(self):
        ''' The set baud rate should serialize to A5 00 0D 01 00 00 25 80 CC 33 C3 3C 0C. '''
        self.wrapper(
            'A5 00 0D 01 00 00 25 80 CC 33 C3 3C 0C',
            SetBaudrate(9600))

    def test_readbaud(self):
        ''' The get baud rate should serialize to A5 00 09 02 CC 33 C3 3C AE. '''
        self.wrapper(
            'A5 00 09 02 CC 33 C3 3C AE',
            ReadBaudrate())

    def test_readstorage_mode(self):
        ''' The read storage mode should serialize to A5 00 09 06 CC 33 C3 3C AA. '''
        self.wrapper(
            'A5 00 09 06 CC 33 C3 3C AA',
            ReadStorageMode())

    def test_set_storagemode_nand(self):
        ''' The set storage mode should serialize to A5 00 0A 07 00 CC 33 C3 3C A8. '''
        self.wrapper(
            'A5 00 0A 07 00 CC 33 C3 3C A8',
            SetStorageMode(SetStorageMode.NAND_MODE))

    def test_set_storagemode_sd(self):
        ''' The set storage mode should serialize to A5 00 0A 07 01 CC 33 C3 3C A9. '''
        self.wrapper(
            'A5 00 0A 07 01 CC 33 C3 3C A9',
            SetStorageMode(SetStorageMode.TF_MODE))

    def test_sleep_mode(self):
        ''' The sleep mode should serialize to A5 00 09 08 CC 33 C3 3C A4. '''
        self.wrapper(
            'A5 00 09 08 CC 33 C3 3C A4',
            SleepMode())

    def test_refresh_and_update(self):
        ''' The refresh and update should serialize to A5 00 09 0A CC 33 C3 3C A6. '''
        self.wrapper(
            'A5 00 09 0A CC 33 C3 3C A6',
            RefreshAndUpdate())

    def test_get_display_direction(self):
        ''' The display direction should serialize to A5 00 09 0C CC 33 C3 3C A0. '''
        self.wrapper(
            'A5 00 09 0C CC 33 C3 3C A0',
            CurrentDisplayRotation())

    def test_set_display_rotation(self):
        ''' The display rotation set should serialize to A5 00 0A 0D 02 CC 33 C3 3C A0. '''
        self.wrapper(
            'A5 00 0A 0D 02 CC 33 C3 3C A0',
            SetCurrentDisplayRotation(SetCurrentDisplayRotation.FLIPB))

    def test_set_display_rotation_2(self):
        ''' The display rotation set should serialize to A5 00 0A 0D 01 CC 33 C3 3C A3'''
        self.wrapper(
            'A5 00 0A 0D 01 CC 33 C3 3C A3',
            SetCurrentDisplayRotation(SetCurrentDisplayRotation.FLIP))

    def test_importfont_library(self):
        ''' The font library import shoud serialize to A5 00 09 0E CC 33 C3 3C A2. '''
        self.wrapper(
            'A5 00 09 0E CC 33 C3 3C A2',
            ImportFontLibrary())
    def test_import_images(self):
        ''' Import images should serialize to A5 00 09 0F CC 33 C3 3C A3. '''
        self.wrapper(
            'A5 00 09 0F CC 33 C3 3C A3',
            ImportImage())
    def test_draw_circle(self):
        ''' Draw circle should serialize to A5 00 0F 26 00 FF 00 FF 00 80 CC 33 C3 3C 0C. '''
        self.wrapper(
            'A5 00 0F 26 00 FF 00 FF 00 80 CC 33 C3 3C 0C',
            DrawCircle(0xff, 0xff, 0x80))

    def test_fill_circle(self):
        ''' Draw circle should serialize to A5 00 0F 27 00 FF 00 FF 00 80 CC 33 C3 3C 0D. '''
        self.wrapper(
            'A5 00 0F 27 00 FF 00 FF 00 80 CC 33 C3 3C 0D',
            FillCircle(0xff, 0xff, 0x80))

    def test_draw_triangle(self):
        ''' Draw triangle should serialize to A5 00 15 28 00 0A 00 0A 00 20 00 80 00 80 00 FF CC 33 C3 3C 47. '''
        self.wrapper(
            'A5 00 15 28 00 0A 00 0A 00 20 00 80 00 80 00 FF CC 33 C3 3C 47',
            DrawTriangle(0x0a, 0x0a, 0x20, 0x80, 0x80, 0xff))

    def test_fill_triangle(self):
        ''' Draw triangle should serialize to A5 00 15 29 00 0A 00 0A 00 20 00 80 00 80 00 FF CC 33 C3 3C 46. '''
        self.wrapper(
            'A5 00 15 29 00 0A 00 0A 00 20 00 80 00 80 00 FF CC 33 C3 3C 46',
            FillTriangle(0x0a, 0x0a, 0x20, 0x80, 0x80, 0xff))

    def test_clear_screen(self):
        ''' Clear screen should serialize to A5 00 09 2E CC 33 C3 3C 82. '''
        self.wrapper(
            'A5 00 09 2E CC 33 C3 3C 82',
            ClearScreen())

    def test_display_text(self):
        ''' Drawing text with the provided example text should serialize to A5 00 17 30 00 0A 00 0A C4 E3 BA C3 57 6F 72 6C 64 00 CC 33 C3 3C 9E. '''
        self.wrapper(
            'A5 00 17 30 00 0A 00 0A C4 E3 BA C3 57 6F 72 6C 64 00 CC 33 C3 3C 9E',
            DisplayText(0xa, 0xa, u'你好World'.encode('gb2312')))

    def test_display_image(self):
        ''' Drawing an image should serialized to A5 00 16 70 00 00 00 00 50 49 43 37 2E 42 4D 50 00 CC 33 C3 3C DF. '''
        self.wrapper(
            'A5 00 16 70 00 00 00 00 50 49 43 37 2E 42 4D 50 00 CC 33 C3 3C DF',
            DisplayImage(0, 0, 'PIC7.BMP'))




def main():
    '''
    Convenient wrapper to invoke all the tests in here.
    '''
    unittest.main()

if __name__ == "__main__":
    main()
