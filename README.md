This project provides python libraries for talking to the Waveshare E-Ink
Display from a Raspberry PI3.

For more information about this display, see the [waveshare site](https://www.waveshare.com/4.3inch-e-paper.htm).  There is also a product [wiki page](https://www.waveshare.com/wiki/4.3inch_e-Paper_UART_Module).

It requires the GPIO library that is typically available on the Raspberry PI.

<center>![hello world image](https://steemitimages.com/DQmZno6hiNcAAgiVx3mCZbhEbnEt3cakxC5mW6V3p9k1qWg/eink-2.png)</center>


This isn't compatible for Python 3+, but there is a relatively-faithful port of the module written for pure Python 3 [over here](https://github.com/jarret/raspi-uart-waveshare/blob/master/waveshare/epaper.py).

Wiring
------
This diagram is for the Pi3, other Pi may work, but the pinout could be
different.  Be sure to check before trying it if you're not using a Pi3.


| PI3 Pin  | E-Ink Pin |
|---------:|:----------|
| 3.3 v  1 | 6 3.3v    |
| GND    6 | 5 GND     |
|GPIO15 10 | 4 DOUT    |
|GPIO14  8 | 3 DIN     |
|GPIO04  7 | 2 WAKE_UP |
|GPIO02  3 | 1 RESET   |

Required Software
-----------------
The `libpython-dev` and `RPIO` libraries are needed.

    sudo apt-get install libpython-dev
    pip install --user RPIO


Tests
-----
There are a set of unit tests (which are executed by the Makefile) which
basically just make sure the code produces what was listed in the wiki as being
valid commands.

Using it
-------
Assuming everything is wired up according to the above diagram, you may still
need to disable the bluetooth serial connection (or use a different file path)
and enable the uart.

To disable the bluetooth serial connection, edit `/boot/cmdline.txt` and delete
`console=serial0,115200`.  Then edit `/boot/config.txt` and add
`dtoverlay=pi3-disable-bt` and `eanble_urar=1` and reboot.

Examples
--------

There are some examples, see `examples.py` and `ip.py`.

* `examples.py` - Displays various greetings at random locations around the
  screen
* `ip.py` - Displays ip addresses for the Pi


