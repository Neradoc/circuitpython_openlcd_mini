"""
 OpenLCD is an LCD with Serial/I2C/SPI interfaces.

Command cheat sheet:
 ASCII / DEC / HEX
 '|'    / 124 / 0x7C - Put into setting mode
 Ctrl+c / 3 / 0x03 - Change width to 20
 Ctrl+d / 4 / 0x04 - Change width to 16
 Ctrl+e / 5 / 0x05 - Change lines to 4
 Ctrl+f / 6 / 0x06 - Change lines to 2
 Ctrl+g / 7 / 0x07 - Change lines to 1
 Ctrl+h / 8 / 0x08 - Software reset of the system
 Ctrl+i / 9 / 0x09 - Enable/disable splash screen
 Ctrl+j / 10 / 0x0A - Save currently displayed text as splash
 Ctrl+k / 11 / 0x0B - Change baud to 2400bps
 Ctrl+l / 12 / 0x0C - Change baud to 4800bps
 Ctrl+m / 13 / 0x0D - Change baud to 9600bps
 Ctrl+n / 14 / 0x0E - Change baud to 14400bps
 Ctrl+o / 15 / 0x0F - Change baud to 19200bps
 Ctrl+p / 16 / 0x10 - Change baud to 38400bps
 Ctrl+q / 17 / 0x11 - Change baud to 57600bps
 Ctrl+r / 18 / 0x12 - Change baud to 115200bps
 Ctrl+s / 19 / 0x13 - Change baud to 230400bps
 Ctrl+t / 20 / 0x14 - Change baud to 460800bps
 Ctrl+u / 21 / 0x15 - Change baud to 921600bps
 Ctrl+v / 22 / 0x16 - Change baud to 1000000bps
 Ctrl+w / 23 / 0x17 - Change baud to 1200bps
 Ctrl+x / 24 / 0x18 - Change the contrast. Follow Ctrl+x with number 0 to 255. 120 is default.
 Ctrl+y / 25 / 0x19 - Change the TWI address. Follow Ctrl+x with number 0 to 255. 114 (0x72) is default.
 Ctrl+z / 26 / 0x1A - Enable/disable ignore RX pin on startup (ignore emergency reset)
 '-'    / 45 / 0x2D - Clear display. Move cursor to home position.
        / 128-157 / 0x80-0x9D - Set the primary backlight brightness. 128 = Off, 157 = 100%.
        / 158-187 / 0x9E-0xBB - Set the green backlight brightness. 158 = Off, 187 = 100%.
        / 188-217 / 0xBC-0xD9 - Set the blue backlight brightness. 188 = Off, 217 = 100%.
         For example, to change the baud rate to 115200 send 124 followed by 18.
 '+'    / 43 / 0x2B - Set Backlight to RGB value, follow + by 3 numbers 0 to 255, for the r, g and b values.
         For example, to change the backlight to yellow send + followed by 255, 255 and 0.
"""

# DISPLAY_ADDRESS1 = 0x72

# Wire.write('|'); //Put LCD into setting mode
# Wire.write('-'); //Send clear display command

class OpenLCD:
	def __init__(self,i2c,address):
		self.address = address
		self.i2c = i2c
		
	def clear(self):
		while not self.i2c.try_lock(): self.i2c.unlock()
		self.i2c.writeto(self.address,b"|-")
		self.i2c.unlock()

	def send(self,value):
		while not self.i2c.try_lock(): self.i2c.unlock()
		self.i2c.writeto(self.address,value)
		self.i2c.unlock()

	def write(self,value):
		# TODO: replace | with ||
		self.send(b"{}".format(value))
	
	# lcd.send(b"|+\x00\xff\xff")
	def backlight(self,color):
		command = b"|+"
		if (type(color) == tuple or type(color) == list) and len(color) == 3:
			command += bytes(color)
		elif type(color) == int:
			cb = (color//0x10000 & 0xFF, color//0x100 & 0xFF, color & 0xFF)
			command += bytes(cb)
		self.send(command)
	
 	def contrast(self,value):
 		command = b"|"+bytes((24,value & 0xFF))
 		self.send(command)
 	
 	def move(self,x,y):
 		pos = 128 + min(16,max(0,x))
 		if y > 1:
 			pos += 64
 		command = bytes([254,pos])
 		self.send(command)
