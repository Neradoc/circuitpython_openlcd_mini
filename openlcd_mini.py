# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Neradoc
#
# SPDX-License-Identifier: MIT
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

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

from micropython import const

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/Neradoc/CircuitPython_openlcd_mini.git"

_DEFAULT_ADDRESS = const(0x72)

class OpenLCD:
    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self.address = address
        self.i2c = i2c
        self._color = (255,255,255)
        self._contrast = 0
        self.clear()

    def clear(self):
        while not self.i2c.try_lock():
            self.i2c.unlock()
        self.i2c.writeto(self.address, b"|-")
        self.i2c.unlock()

    def send(self, value):
        while not self.i2c.try_lock():
            self.i2c.unlock()
        self.i2c.writeto(self.address, value)
        self.i2c.unlock()

    def write(self, value):
        out = b"{}".format(value.replace("|","||"))
        self.send(out)

    def print(self, *values, end="\r", sep=" "):
        self.write(sep.join([str(x) for x in values])+end)

    @property
    def backlight(self):
        return self._color

    @backlight.setter
    def backlight(self, color):
        command = b"|+"
        if (type(color) == tuple or type(color) == list) and len(color) == 3:
            command += bytes(color)
            self._color = tuple(color)
        elif type(color) == int:
            cb = (color // 0x10000 & 0xFF, color // 0x100 & 0xFF, color & 0xFF)
            command += bytes(cb)
            self._color = cb
        else:
            raise ValueError("color format: (r,g,b) or 0xRRGGBB")
        self.send(command)

    @property
    def contrast(self):
        return self._contrast

    @contrast.setter
    def contrast(self, value):
        if int(value) < 0 or int(value) > 0xFF:
            raise ValueError("contrast is a value between 0 and 255")
        command = b"|" + bytes((24, int(value)))
        self._contrast = value
        self.send(command)

    def move(self, x, y):
        pos = 128 + min(16, max(0, x))
        if y > 1:
            pos += 64
        command = bytes([254, pos])
        self.send(command)
