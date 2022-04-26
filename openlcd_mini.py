# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Neradoc
# SPDX-License-Identifier: MIT
#
# pylint:disable=consider-using-f-string
"""
`openlcd_mini`
================================================================================

Small driver for Sparkfun OpenLCD/SerLCD for Circuitpython


* Author(s): Neradoc

Implementation Notes
--------------------

**Hardware:**

* `SparkFun 16x2 SerLCD - RGB Backlight (Qwiic) <https://www.sparkfun.com/products/16396>`_
* `SparkFun 20x4 SerLCD - RGB Backlight (Qwiic) <https://www.sparkfun.com/products/16398>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

from micropython import const

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/Neradoc/CircuitPython_openlcd_mini.git"

_DEFAULT_ADDRESS = const(0x72)


class OpenLCD:
    """
    Driver for the Saprkfun OpenLCD firmware.

    :param i2c_bus: The `busio.I2C` object to use.
    :param int address: Device I2C address.
    """

    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self.address = address
        self.i2c = i2c
        self._color = (255, 255, 255)
        self._contrast = 0
        self.clear()

    def clear(self):
        """Clear the display."""
        while not self.i2c.try_lock():
            self.i2c.unlock()
        self.i2c.writeto(self.address, b"|-")
        self.i2c.unlock()

    def send(self, value):
        """
        Send raw data to the LCD.

        :param bytes value: Bytes to send to the LCD.
        """
        while not self.i2c.try_lock():
            self.i2c.unlock()
        self.i2c.writeto(self.address, value)
        self.i2c.unlock()

    def write(self, value):
        """
        Write text to the LCD from the current cursor position.

        :param chr value: Text to write to the LCD.
        """
        out = "{}".format(value.replace("|", "||")).encode("ascii")
        self.send(out)

    def print(self, *values, end="\r", sep=" "):
        """
        Write text to the LCD from the current cursor position, like python's print.

        :param chr values: Values to write to the LCD.
        :param chr end: Final character added to the line. Default: carrier return.
        :param chr sep: Separator between the values, default: space.
        """
        self.write(sep.join([str(x) for x in values]) + end)

    @property
    def backlight(self):
        """The color of the backlight, tuple (r, g, b) or int #RRGGBB."""
        return self._color

    @backlight.setter
    def backlight(self, color):
        command = b"|+"
        if isinstance(color, (tuple, list)) and len(color) == 3:
            command += bytes(color)
            self._color = tuple(color)
        elif isinstance(color, int):
            color_tuple = (color // 0x10000 & 0xFF, color // 0x100 & 0xFF, color & 0xFF)
            command += bytes(color_tuple)
            self._color = color_tuple
        else:
            raise ValueError("color format: (r,g,b) or 0xRRGGBB")
        self.send(command)

    @property
    def contrast(self):
        """The contrast, an int between 0 and 128."""
        return self._contrast

    @contrast.setter
    def contrast(self, value):
        if int(value) < 0 or int(value) > 0xFF:
            raise ValueError("contrast is a value between 0 and 255")
        command = b"|" + bytes((24, int(value)))
        self._contrast = value
        self.send(command)

    def move(self, x, y):
        """Move the cursor to the designated position."""
        pos = 128 + min(16, max(0, x))
        if y > 1:
            pos += 64
        command = bytes([254, pos])
        self.send(command)
