# DISPLAY_ADDRESS1 = 0x72

# Wire.write('|'); //Put LCD into setting mode
# Wire.write('-'); //Send clear display command


class OpenLCD:
    def __init__(self, i2c, address):
        self.address = address
        self.i2c = i2c
        self._color = (255,255,255)
        self._contrast = 0

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
