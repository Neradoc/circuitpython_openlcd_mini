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
