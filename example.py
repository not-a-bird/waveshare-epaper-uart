#!/usr/bin/env python
# -*- encoding: utf-8 -*-

''' Demonstrates some basic functions for writing to the display.

These examples need to be run on a raspberry pi and GPIO needs to be installed
(hint: `pip install --user GPIO`).

Caveats:

The PI must have the serial GPIO pins enabled (enable_uart=1 in
/boot/config.txt) and the script assumes the serial device is `/dev/ttyAMA0`

'''

import random
from time import sleep

import RPi.GPIO as GPIO
from waveshare import DisplayText
from waveshare import EPaper
from waveshare import RefreshAndUpdate
from waveshare import SetEnFontSize
from waveshare import SetZhFontSize

def hello_world(paper):
    '''
    Displays text on the screen at random locations and sizes.
    '''
    x_pool = [_ for _ in xrange(0, 800, 32)]
    y_pool = [_ for _ in xrange(0, 800, 32)]
    greets = [_.encode('gb2312') for _ in [u'你好', u'hello', u'hi', u'salut', u'hola', u'Здравствуйте', u'Привет', u'Kamusta', u'こんにちは']] #pylint: disable=line-too-long
    e_sizes = [SetEnFontSize.THIRTYTWO, SetEnFontSize.FOURTYEIGHT, SetEnFontSize.SIXTYFOUR] #pylint: disable=line-too-long
    z_sizes = [SetZhFontSize.THIRTYTWO, SetZhFontSize.FOURTYEIGHT, SetZhFontSize.SIXTYFOUR] #pylint: disable=line-too-long
    for _ in xrange(0, 10):
        paper.send(SetEnFontSize(random.choice(e_sizes)))
        paper.send(SetZhFontSize(random.choice(z_sizes)))
        paper.send(DisplayText(random.choice(x_pool), random.choice(y_pool), random.choice(greets))) #pylint: disable=line-too-long
    paper.send(RefreshAndUpdate())
    sleep(2)

def main():
    '''
    Runs through a few example uses of the connected display.
    '''
    paper = EPaper('/dev/ttyAMA0')
    hello_world(paper)

if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
