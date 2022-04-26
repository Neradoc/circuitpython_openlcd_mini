# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Neradoc
#
# SPDX-License-Identifier: Unlicense

import time
import board
from rainbowio import colorwheel
import openlcd_mini

i2c = board.I2C()
lcd = openlcd_mini.OpenLCD(i2c)

lcd.write("Hello World !")

for x in range(0, 256, 8):
    lcd.backlight = colorwheel(x)
    time.sleep(0.04)

lcd.backlight = 0xFFFF00

for contrast in range(0, 128, 16):
    lcd.contrast = contrast
lcd.contrast = 0

for x in range(0, 13):
    lcd.move(x, 2)
    lcd.write("Hi")
    time.sleep(0.5)
